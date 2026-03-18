from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail

from django.conf import settings

from .models import ProjectInquiry
from .serializers import ProjectInquirySerializer


class ProjectInquiryCreateView(APIView):

    def post(self, request):
        serializer = ProjectInquirySerializer(data=request.data)

        if serializer.is_valid():
            inquiry = serializer.save()

            # 📩 1. EMAIL TO ADMIN
            send_mail(
                subject=f"New Project Inquiry - {inquiry.name}",
                message=f"""
New Project Inquiry Received:

Name: {inquiry.name}
Email: {inquiry.email}
Phone: {inquiry.phone}
Company: {inquiry.company}

Service: {inquiry.service_type}
Budget: {inquiry.project_budget}
Timeline: {inquiry.urgency}

Message:
{inquiry.message}
""",
                from_email=settings.EMAIL_HOST_USER,  # ✅ company email
                recipient_list=[settings.EMAIL_HOST_USER],
            )

            # 📩 2. AUTO-REPLY TO USER
            send_mail(
                subject="Thank you for contacting Jeblio Corporation 🚀",
                message=f"""
Dear {inquiry.name},

Thank you for reaching out to Jeblio Corporation!

We have received your project inquiry and our team will review it shortly.

📌 Our team will contact you within 24 hours.

Here’s a quick summary of your request:
---------------------------------------
Service: {inquiry.service_type}
Budget: {inquiry.project_budget}
Timeline: {inquiry.urgency}

We’re excited to work with you! 🚀

Best Regards,  
Jeblio Corporation Pvt Ltd  
📧 jeblioinfo@gmail.com  
📞 +91 9952877911
""",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[inquiry.email],  # ✅ send to user
            )

            return Response(
                {"message": "Submitted successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings

from .models import ProjectInquiry


class UpdateProjectStatusView(APIView):

    def post(self, request, pk):
        try:
            inquiry = ProjectInquiry.objects.get(pk=pk)
        except ProjectInquiry.DoesNotExist:
            return Response({"error": "Inquiry not found"}, status=404)

        new_status = request.data.get("status")

        if new_status not in ['contacted', 'closed']:
            return Response({"error": "Invalid status"}, status=400)

        inquiry.status = new_status
        inquiry.save()

        # 📧 SEND EMAIL BASED ON STATUS
        if new_status == 'contacted':
            send_mail(
                subject="📞 We’ve Reviewed Your Project – Jeblio",
                message=f"""
Dear {inquiry.name},

Thank you for reaching out to Jeblio Corporation.

✅ Our team has reviewed your project requirements.
📞 We will contact you shortly to discuss further details.

We’re excited to work with you!

Best Regards,  
Jeblio Corporation Pvt Ltd  
📧 jeblioinfo@gmail.com  
📞 +91 9952877911
""",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[inquiry.email],
                fail_silently=False,
            )

        elif new_status == 'closed':
            send_mail(
                subject="Project Inquiry Closed – Jeblio",
                message=f"""
Dear {inquiry.name},

Thank you for contacting Jeblio Corporation.

Your inquiry has been marked as closed.

If you have any new requirements in the future, feel free to reach out again.

Best Regards,  
Jeblio Corporation Pvt Ltd  
📧 jeblioinfo@gmail.com  
📞 +91 9952877911
""",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[inquiry.email],
                fail_silently=False,
            )

        return Response({"message": "Status updated successfully"}, status=status.HTTP_200_OK)
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import ProjectInquiry
from .serializers import ProjectInquirySerializer


class ProjectInquiryListView(APIView):

    def get(self, request):

        # 🔍 Optional filter: ?status=pending / contacted / closed
        status_filter = request.GET.get('status')

        if status_filter:
            inquiries = ProjectInquiry.objects.filter(status=status_filter).order_by('-created_at')
        else:
            inquiries = ProjectInquiry.objects.all().order_by('-created_at')

        serializer = ProjectInquirySerializer(inquiries, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)