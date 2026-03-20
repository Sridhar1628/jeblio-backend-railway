from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import ProjectInquiry
from .serializers import ProjectInquirySerializer

# ✅ SENDGRID FUNCTION
from jeblioweb_backend.utils.email import send_email

import threading


# ======================
# CREATE PROJECT INQUIRY
# ======================
class ProjectInquiryCreateView(APIView):

    def post(self, request):
        serializer = ProjectInquirySerializer(data=request.data)

        if serializer.is_valid():
            inquiry = serializer.save()

            # ======================
            # 📩 EMAIL TO ADMIN
            # ======================
            def send_admin_email():
                try:
                    message = f"""
                    <h3>New Project Inquiry</h3>

                    <p><b>Name:</b> {inquiry.name}</p>
                    <p><b>Email:</b> {inquiry.email}</p>
                    <p><b>Phone:</b> {inquiry.phone}</p>
                    <p><b>Company:</b> {inquiry.company}</p>

                    <hr>

                    <p><b>Service:</b> {inquiry.service_type}</p>
                    <p><b>Budget:</b> {inquiry.project_budget}</p>
                    <p><b>Timeline:</b> {inquiry.urgency}</p>

                    <hr>

                    <p><b>Message:</b><br>{inquiry.message}</p>
                    """

                    send_email(
                        to_email="jeblioinfo@gmail.com",
                        subject=f"New Project Inquiry - {inquiry.name}",
                        message=message
                    )

                except Exception as e:
                    print("Admin email error:", e)

            # ======================
            # 📩 AUTO REPLY TO USER
            # ======================
            def send_user_email():
                try:
                    message = f"""
                    <h2>Thank You for Contacting Jeblio 🚀</h2>

                    <p>Dear <b>{inquiry.name}</b>,</p>

                    <p>We have received your project inquiry successfully.</p>

                    <p>Our team will review your requirements and contact you within <b>24 hours</b>.</p>

                    <hr>

                    <h4>Your Request Summary:</h4>
                    <ul>
                        <li><b>Service:</b> {inquiry.service_type}</li>
                        <li><b>Budget:</b> {inquiry.project_budget}</li>
                        <li><b>Timeline:</b> {inquiry.urgency}</li>
                    </ul>

                    <br>

                    <p>We’re excited to work with you! 🚀</p>

                    <p>
                    Best Regards,<br>
                    <b>Jeblio Corporation Pvt Ltd</b><br>
                    📧 jeblioinfo@gmail.com<br>
                    📞 +91 9952877911
                    </p>
                    """

                    send_email(
                        to_email=inquiry.email,
                        subject="Thank you for contacting Jeblio Corporation 🚀",
                        message=message
                    )

                except Exception as e:
                    print("User email error:", e)

            # ✅ RUN ASYNC
            threading.Thread(target=send_admin_email).start()
            threading.Thread(target=send_user_email).start()

            return Response(
                {"message": "Submitted successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ======================
# UPDATE STATUS
# ======================
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

        # ======================
        # 📧 SEND STATUS EMAIL
        # ======================
        def send_status_email():
            try:
                if new_status == 'contacted':
                    message = f"""
                    <h2>📞 We’ve Reviewed Your Project</h2>

                    <p>Dear <b>{inquiry.name}</b>,</p>

                    <p>Our team has reviewed your project requirements.</p>

                    <p>📞 We will contact you shortly to discuss further details.</p>

                    <br>

                    <p>We’re excited to work with you!</p>

                    <p>
                    Best Regards,<br>
                    Jeblio Corporation Pvt Ltd
                    </p>
                    """

                    subject = "📞 We’ve Reviewed Your Project – Jeblio"

                else:
                    message = f"""
                    <h2>Project Inquiry Closed</h2>

                    <p>Dear <b>{inquiry.name}</b>,</p>

                    <p>Your inquiry has been marked as closed.</p>

                    <p>If you have new requirements in the future, feel free to contact us again.</p>

                    <br>

                    <p>
                    Best Regards,<br>
                    Jeblio Corporation Pvt Ltd
                    </p>
                    """

                    subject = "Project Inquiry Closed – Jeblio"

                send_email(
                    to_email=inquiry.email,
                    subject=subject,
                    message=message
                )

            except Exception as e:
                print("Status email error:", e)

        # ✅ ASYNC
        threading.Thread(target=send_status_email).start()

        return Response(
            {"message": "Status updated successfully"},
            status=status.HTTP_200_OK
        )


# ======================
# LIST INQUIRIES
# ======================
class ProjectInquiryListView(APIView):

    def get(self, request):

        status_filter = request.GET.get('status')

        if status_filter:
            inquiries = ProjectInquiry.objects.filter(status=status_filter).order_by('-created_at')
        else:
            inquiries = ProjectInquiry.objects.all().order_by('-created_at')

        serializer = ProjectInquirySerializer(inquiries, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)