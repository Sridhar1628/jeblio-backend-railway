from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import InternshipApplication
from .serializers import InternshipApplicationSerializer


from django.core.mail import send_mail
from django.conf import settings

# ✅ CREATE APPLICATION
class InternshipApplicationView(APIView):

    def post(self, request):
        serializer = InternshipApplicationSerializer(data=request.data)

        if serializer.is_valid():
            application = serializer.save()

            # 📩 1. EMAIL TO COMPANY (ADMIN)
            send_mail(
                subject=f"New Internship Application - {application.full_name}",
                message=f"""
New Internship Application Received

-------------------------------------

👤 Name: {application.full_name}
📧 Email: {application.email}
📱 Phone: {application.phone}

🎯 Internship: {application.internship_type}

-------------------------------------

Please review the application in the admin panel.

- Jeblio System
""",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            # 📩 2. AUTO-REPLY TO USER
            send_mail(
                subject="Application Received – Jeblio Corporation 🚀",
                message=f"""
Dear {application.full_name},

Thank you for applying to Jeblio Corporation!

We have successfully received your application for the 
"{application.internship_type}" internship.

📌 What happens next?
-------------------------------------
• Our team will review your application
• Shortlisted candidates will be contacted
• Process usually takes 24–48 hours

We appreciate your interest in joining us and wish you the best!

Best Regards,  
Jeblio Corporation Pvt Ltd  
📧 jeblioinfo@gmail.com  
📞 +91 9952877911
""",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[application.email],
                fail_silently=False,
            )

            return Response(
                {"message": "Application submitted successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail

from .models import InternshipApplication


# ✅ UPDATE STATUS (APPROVE / REJECT)
class UpdateApplicationStatusView(APIView):

    def post(self, request, pk):
        try:
            application = InternshipApplication.objects.get(pk=pk)
        except InternshipApplication.DoesNotExist:
            return Response({"error": "Application not found"}, status=404)

        new_status = request.data.get("status")

        if new_status not in ['approved', 'rejected']:
            return Response({"error": "Invalid status"}, status=400)

        # Update status
        application.status = new_status
        application.save()

        # 📩 EMAIL BASED ON STATUS
        if new_status == 'approved':
            send_mail(
                subject="🎉 Congratulations! You're Selected – Jeblio",
                message=f"""
Dear {application.full_name},

Congratulations! 🎉

We are pleased to inform you that you have been selected for the 
"{application.internship_type}" internship at Jeblio Corporation.

📌 Next Steps:
-------------------------------------
• Our team will contact you shortly
• You will receive onboarding details
• Prepare to begin your internship journey 🚀

We are excited to have you onboard!

Best Regards,  
Jeblio Corporation Pvt Ltd  
📧 jeblioinfo@gmail.com  
📞 +91 9952877911
""",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[application.email],
                fail_silently=False,
            )

        elif new_status == 'rejected':
            send_mail(
                subject="Application Update – Jeblio Corporation",
                message=f"""
Dear {application.full_name},

Thank you for your interest in the 
"{application.internship_type}" internship at Jeblio Corporation.

After careful consideration, we regret to inform you that you have not been selected at this time.

📌 Note:
-------------------------------------
We encourage you to apply again in the future as new opportunities arise.

We truly appreciate your time and effort.

Best Regards,  
Jeblio Corporation Pvt Ltd  
📧 jeblioinfo@gmail.com  
📞 +91 9952877911
""",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[application.email],
                fail_silently=False,
            )

        return Response(
            {"message": "Status updated successfully"},
            status=status.HTTP_200_OK
        )    
from rest_framework.generics import ListAPIView
from .serializers import InternshipApplicationSerializer


from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models import InternshipApplication
from .serializers import InternshipApplicationSerializer

class InternshipApplicationListView(ListAPIView):
    queryset = InternshipApplication.objects.all().order_by('-created_at')
    serializer_class = InternshipApplicationSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        response = Response(serializer.data)

        # ✅ FORCE CORS HEADERS
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"

        return response

    def options(self, request, *args, **kwargs):
        response = Response()
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        return response