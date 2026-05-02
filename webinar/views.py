from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import TermsAndConditions

@api_view(['GET'])
def get_terms(request):
    terms = TermsAndConditions.objects.filter(is_active=True).last()

    if terms:
        return Response({
            "title": terms.title,
            "content": terms.content
        })

    return Response({"message": "No terms found"})

import razorpay
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@api_view(['POST'])
def create_order(request):
    amount = 4900  # ₹49 in paise

    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    return Response(order)


from .models import WebinarRegistration
from jeblioweb_backend.utils.email import send_email
import threading

@api_view(['POST'])
def verify_payment(request):
    data = request.data

    try:
        client.utility.verify_payment_signature({
            'razorpay_order_id': data['razorpay_order_id'],
            'razorpay_payment_id': data['razorpay_payment_id'],
            'razorpay_signature': data['razorpay_signature']
        })

        # ✅ SAVE DATA
        registration = WebinarRegistration.objects.create(
            name=data.get("name"),
            email=data.get("email"),
            phone=data.get("phone"),
            payment_id=data.get("razorpay_payment_id"),
            order_id=data.get("razorpay_order_id"),
        )

        # ======================
        # 📩 EMAIL TO USER
        # ======================
        def send_user_email():
            try:
                message = f"""
                <h2>🎉 Registration Successful!</h2>

                <p>Hi <b>{registration.name}</b>,</p>

                <p>You have successfully registered for the <b>Jeblio Webinar</b>.</p>

                <p>📅 April 26 | ⏰ 6 PM IST</p>

                <hr>

                <p><b>👉 Join WhatsApp Group:</b></p>
                <a href="YOUR_WHATSAPP_LINK">Click Here to Join</a>

                <br><br>

                <p>See you in the session 🚀</p>

                <p>— Jeblio Team</p>
                """

                send_email(
                    to_email=registration.email,
                    subject="Webinar Registration Confirmed 🚀",
                    message=message
                )
            except Exception as e:
                print("User email error:", e)

        # ======================
        # 📩 EMAIL TO ADMIN
        # ======================
        def send_admin_email():
            try:
                message = f"""
                <h3>New Webinar Registration</h3>

                <p><b>Name:</b> {registration.name}</p>
                <p><b>Email:</b> {registration.email}</p>
                <p><b>Phone:</b> {registration.phone}</p>
                <p><b>Payment_id:</b> {registration.payment_id}</p>
                <p><b>Order_id:</b> {registration.order_id}</p>

                """

                send_email(
                    to_email="jeblioinfo@gmail.com",
                    subject="New Webinar Registration",
                    message=message
                )
            except Exception as e:
                print("Admin email error:", e)

        threading.Thread(target=send_user_email).start()
        threading.Thread(target=send_admin_email).start()

        return Response({"status": "success"})

    except:
        return Response({"status": "failed"}, status=400)