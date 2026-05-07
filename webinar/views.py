from rest_framework.decorators import api_view
from rest_framework.response import Response
import threading
from .models import TermsAndConditions
from django.conf import settings
from urllib.parse import urlencode


from cashfree_pg.api_client import Cashfree
from cashfree_pg.models.create_order_request import CreateOrderRequest
from cashfree_pg.models.customer_details import CustomerDetails
from cashfree_pg.models.order_meta import OrderMeta

import uuid
from django.conf import settings


@api_view(['POST'])
def create_order(request):

    data = request.data

    order_id = str(uuid.uuid4())

    customer_details = CustomerDetails(
        customer_id=order_id,
        customer_name=data.get("name"),
        customer_email=data.get("email"),
        customer_phone=data.get("phone"),
    )

    query_params = urlencode({
        "order_id": order_id,
        "name": data.get("name"),
        "email": data.get("email"),
        "phone": data.get("phone"),
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

    try:

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

        print("CASHFREE ERROR:", str(e))

        return Response({
            "error": str(e)
        }, status=400)
    

from .models import WebinarRegistration
from jeblioweb_backend.utils.email import send_email


@api_view(['POST'])
def verify_payment(request):

    order_id = request.data.get("order_id")

    try:

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

        # ✅ CHECK PAYMENT STATUS
        if order_data.order_status == "PAID":

            # Prevent duplicate save
            existing = WebinarRegistration.objects.filter(
                order_id=order_id
            ).first()

            if existing:
                return Response({
                    "status": "already_saved"
                })

            registration = WebinarRegistration.objects.create(
                name=request.data.get("name"),
                email=request.data.get("email"),
                phone=request.data.get("phone"),
                payment_id=order_data.cf_order_id,
                order_id=order_id,
                payment_status=order_data.order_status,
                payment_method="cashfree"
            )

            # ======================
            # USER EMAIL
            # ======================

            def send_user_email():

                message = f"""
                <h2>🎉 Registration Successful!</h2>

                <p>Hi <b>{registration.name}</b>,</p>

                <p>Your webinar registration is confirmed.</p>

                <p>📅 April 26 | ⏰ 6 PM IST</p>

                <br>

                <a href="YOUR_WHATSAPP_LINK">
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

            threading.Thread(target=send_user_email).start()

            return Response({
                "status": "success"
            })

        return Response({
            "status": "failed"
        }, status=400)

    except Exception as e:

        print("VERIFY ERROR:", str(e))

        return Response({
            "error": str(e)
        }, status=400)
    
    # views.py

