from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from urllib.parse import urlencode
from django.db import transaction

from cashfree_pg.api_client import Cashfree
from cashfree_pg.models.create_order_request import CreateOrderRequest
from cashfree_pg.models.customer_details import CustomerDetails
from cashfree_pg.models.order_meta import OrderMeta

from .models import WebinarLead

import uuid
import logging

logger = logging.getLogger(__name__)


@api_view(["POST"])
def create_order(request):

    try:

        data = request.data

        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")

        # =========================
        # VALIDATION
        # =========================

        if not name or not email or not phone:
            return Response({
                "error": "All fields are required"
            }, status=400)

        # =========================
        # PREVENT DUPLICATE PAID USERS
        # =========================

        already_paid = WebinarLead.objects.filter(
            email=email,
            payment_status="PAID"
        ).exists()

        if already_paid:
            return Response({
                "error": "You are already registered"
            }, status=400)

        order_id = str(uuid.uuid4())

        # =========================
        # SAVE LEAD BEFORE PAYMENT
        # =========================

        with transaction.atomic():

            WebinarLead.objects.create(
                name=name,
                email=email,
                phone=phone,
                order_id=order_id,
                payment_status="PENDING"
            )

        # =========================
        # CASHFREE CUSTOMER
        # =========================

        customer_details = CustomerDetails(
            customer_id=order_id,
            customer_name=name,
            customer_email=email,
            customer_phone=phone,
        )

        query_params = urlencode({
            "order_id": order_id
        })

        order_meta = OrderMeta(
            return_url=f"{settings.FRONTEND_URL}/success?{query_params}"
        )

        create_order_request = CreateOrderRequest(
            order_amount=49.0,
            order_currency="INR",
            customer_details=customer_details,
            order_id=order_id,
            order_meta=order_meta
        )

        # =========================
        # CASHFREE ENVIRONMENT
        # =========================

        environment = (
            Cashfree.PRODUCTION
            if settings.CASHFREE_ENV == "PRODUCTION"
            else Cashfree.SANDBOX
        )

        cashfree = Cashfree(
            XClientId=settings.CASHFREE_APP_ID,
            XClientSecret=settings.CASHFREE_SECRET_KEY,
            XEnvironment=environment
        )

        response = cashfree.PGCreateOrder(
            "2023-08-01",
            create_order_request
        )

        return Response({
            "payment_session_id": response.data.payment_session_id,
            "order_id": order_id
        })

    except Exception as e:

        logger.exception("CREATE ORDER ERROR")

        return Response({
            "error": "Unable to create order"
        }, status=500)    

from .models import WebinarRegistration
from jeblioweb_backend.utils.email import send_email


from django.db import transaction
from .models import WebinarRegistration
from jeblioweb_backend.utils.email import send_email
import threading


@api_view(["POST"])
def verify_payment(request):

    try:

        order_id = request.data.get("order_id")

        if not order_id:
            return Response({
                "error": "Order ID is required"
            }, status=400)

        # =========================
        # GET LEAD
        # =========================

        lead = WebinarLead.objects.filter(
            order_id=order_id
        ).first()

        if not lead:
            return Response({
                "error": "Invalid order"
            }, status=404)

        # =========================
        # CASHFREE ENVIRONMENT
        # =========================

        environment = (
            Cashfree.PRODUCTION
            if settings.CASHFREE_ENV == "PRODUCTION"
            else Cashfree.SANDBOX
        )

        cashfree = Cashfree(
            XClientId=settings.CASHFREE_APP_ID,
            XClientSecret=settings.CASHFREE_SECRET_KEY,
            XEnvironment=environment
        )

        response = cashfree.PGFetchOrder(
            "2023-08-01",
            order_id
        )

        order_data = response.data

        # =========================
        # PAYMENT SUCCESS
        # =========================

        if order_data.order_status == "PAID":

            with transaction.atomic():

                # UPDATE LEAD STATUS
                lead.payment_status = "PAID"
                lead.save()

                # PREVENT DUPLICATES
                existing_registration = WebinarRegistration.objects.filter(
                    order_id=order_id
                ).first()

                if existing_registration:
                    return Response({
                        "status": "already_saved"
                    })

                registration = WebinarRegistration.objects.create(
                    name=lead.name,
                    email=lead.email,
                    phone=lead.phone,
                    payment_id=order_data.cf_order_id,
                    order_id=order_id,
                    payment_status=order_data.order_status,
                    payment_method="cashfree"
                )

            # =========================
            # SEND EMAIL
            # =========================

            def send_user_email():

                message = f"""
                <h2>🎉 Registration Successful!</h2>

                <p>Hi <b>{registration.name}</b>,</p>

                <p>Your webinar registration is confirmed.</p>

                <p>📅 April 26 | ⏰ 6 PM IST</p>

                <br>

                <a href="https://chat.whatsapp.com/DuBbqW4KiBRJYARS64x57K">
                    Join WhatsApp Group
                </a>

                <br><br>

                <p>— Jeblio Team</p>
                """

                send_email(
                    to_email=registration.email,
                    subject="Webinar Registration Confirmed 🚀",
                    message=message
                )

            threading.Thread(
                target=send_user_email,
                daemon=True
            ).start()

            return Response({
                "status": "success"
            })

        # =========================
        # PAYMENT FAILED
        # =========================

        lead.payment_status = "FAILED"
        lead.save()

        return Response({
            "status": "failed"
        }, status=400)

    except Exception as e:

        logger.exception("VERIFY PAYMENT ERROR")

        return Response({
            "error": "Payment verification failed"
        }, status=500)