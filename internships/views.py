from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView

from .models import InternshipApplication
from .serializers import InternshipApplicationSerializer

# ✅ IMPORT SENDGRID FUNCTION
from jeblioweb_backend.utils.email import send_email

import threading


# ======================
# CREATE APPLICATION
# ======================
class InternshipApplicationView(APIView):

    def post(self, request):
        serializer = InternshipApplicationSerializer(data=request.data)

        if serializer.is_valid():
            application = serializer.save()

            # ======================
            # 📩 EMAIL TO ADMIN
            # ======================
            def send_admin_email():
                try:
                    message = f"""
                    <h3>New Internship Application</h3>
                    <p><b>Name:</b> {application.full_name}</p>
                    <p><b>Email:</b> {application.email}</p>
                    <p><b>Phone:</b> {application.phone}</p>
                    <p><b>Internship:</b> {application.internship_type}</p>
                    """

                    send_email(
                        to_email="jeblioinfo@gmail.com",
                        subject=f"New Internship Application - {application.full_name}",
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
                    <h2>Application Received 🚀</h2>

                    <p>Dear <b>{application.full_name}</b>,</p>

                    <p>Thank you for applying to <b>Jeblio Corporation</b>.</p>

                    <p>Your application for <b>{application.internship_type}</b> has been received successfully.</p>

                    <hr>

                    <h4>What happens next?</h4>
                    <ul>
                        <li>Our team will review your application</li>
                        <li>Shortlisted candidates will be contacted</li>
                        <li>Process usually takes 24–48 hours</li>
                    </ul>

                    <br>

                    <p>Best Regards,<br>
                    <b>Jeblio Corporation Pvt Ltd</b><br>
                    📧 jeblioinfo@gmail.com<br>
                    📞 +91 9952877911</p>
                    """

                    send_email(
                        to_email=application.email,
                        subject="Application Received – Jeblio Corporation 🚀",
                        message=message
                    )
                except Exception as e:
                    print("User email error:", e)

            # ✅ RUN EMAILS IN BACKGROUND
            threading.Thread(target=send_admin_email).start()
            threading.Thread(target=send_user_email).start()

            return Response(
                {"message": "Application submitted successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ======================
# UPDATE STATUS
# ======================
class UpdateApplicationStatusView(APIView):

    def post(self, request, pk):
        try:
            application = InternshipApplication.objects.get(pk=pk)
        except InternshipApplication.DoesNotExist:
            return Response({"error": "Application not found"}, status=404)

        new_status = request.data.get("status")

        if new_status not in ['approved', 'rejected']:
            return Response({"error": "Invalid status"}, status=400)

        application.status = new_status
        application.save()

        # ======================
        # EMAIL BASED ON STATUS
        # ======================
        def send_status_email():
            try:
                if new_status == 'approved':
                    message = f"""
                    <h2>🎉 Congratulations!</h2>

                    <p>Dear <b>{application.full_name}</b>,</p>

                    <p>You have been selected for the <b>{application.internship_type}</b> internship at Jeblio.</p>

                    <hr>

                    <h4>Next Steps:</h4>
                    <ul>
                        <li>Our team will contact you shortly</li>
                        <li>You will receive onboarding details</li>
                        <li>Get ready to start 🚀</li>
                    </ul>

                    <br>

                    <p><b>Welcome aboard!</b></p>

                    <p>Jeblio Corporation Pvt Ltd</p>
                    """

                    subject = "🎉 You're Selected – Jeblio"

                else:
                    message = f"""
                    <h2>Application Update</h2>

                    <p>Dear <b>{application.full_name}</b>,</p>

                    <p>Thank you for applying for the <b>{application.internship_type}</b> internship.</p>

                    <p>We regret to inform you that you were not selected this time.</p>

                    <hr>

                    <p>We encourage you to apply again in the future.</p>

                    <br>

                    <p>Best Regards,<br>
                    Jeblio Corporation Pvt Ltd</p>
                    """

                    subject = "Application Update – Jeblio"

                send_email(
                    to_email=application.email,
                    subject=subject,
                    message=message
                )

            except Exception as e:
                print("Status email error:", e)

        # ✅ RUN IN BACKGROUND
        threading.Thread(target=send_status_email).start()

        return Response(
            {"message": "Status updated successfully"},
            status=status.HTTP_200_OK
        )


# ======================
# LIST APPLICATIONS
# ======================
class InternshipApplicationListView(ListAPIView):
    queryset = InternshipApplication.objects.all().order_by('-created_at')
    serializer_class = InternshipApplicationSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import InternshipApplication


# ======================
# DELETE APPLICATION
# ======================
class DeleteApplicationView(APIView):

    def delete(self, request, pk):
        try:
            application = InternshipApplication.objects.get(pk=pk)
        except InternshipApplication.DoesNotExist:
            return Response(
                {"error": "Application not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        application.delete()

        return Response(
            {"message": "Application deleted successfully"},
            status=status.HTTP_200_OK
        )
    
# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from .models import ApplicationCounter


@api_view(['GET'])
def get_application_count(request):
    try:
        counter = ApplicationCounter.objects.get(id=1)
    except ApplicationCounter.DoesNotExist:
        return Response({"count": 100})

    now = timezone.now()

    # ✅ STOP at deadline
    if now > counter.end_time:
        now = counter.end_time

    # Total time passed
    time_diff = (now - counter.start_time).total_seconds()

    # Which interval (30 mins = 1800 sec)
    interval_index = int(time_diff // 1800)

    total = counter.base_count

    # ✅ Add completed intervals
    for i in range(interval_index):
        if i < len(counter.increments):
            total += counter.increments[i]

    # ✅ Add current interval (smooth growth)
    if interval_index < len(counter.increments):
        current_total = counter.increments[interval_index]

        seconds_in_current = time_diff % 1800

        # progress ratio (0 → 1)
        progress = seconds_in_current / 1800

        partial_growth = current_total * progress

        total += int(partial_growth)

    return Response({
        "count": int(total)
    })

from django.http import FileResponse, Http404
from django.conf import settings
import os


def download_syllabus(request, domain):
    # ===== FILE MAP =====
    file_map = {
        "web-development": "web_dev.pdf",
        "mobile-development": "mobile_dev.pdf",
        "data-science": "data_science.pdf",
        "digital-marketing": "digital_marketing.pdf",
        "ui-ux": "uiux.pdf",
        "business-development": "business.pdf",
        "cloud-computing": "cloud.pdf",
        "ai-machine-learning": "ai_ml.pdf",
        "cyber-security": "cyber_security.pdf",
    }

    # ===== GET FILE NAME =====
    filename = file_map.get(domain)

    if not filename:
        raise Http404("Invalid domain")

    # ===== BUILD FILE PATH =====
    file_path = os.path.join(settings.MEDIA_ROOT, "syllabus", filename)

    # ===== DEBUG (REMOVE LATER) =====
    print("Requested Domain:", domain)
    print("Resolved Filename:", filename)
    print("MEDIA_ROOT:", settings.MEDIA_ROOT)
    print("Final File Path:", file_path)
    print("File Exists:", os.path.exists(file_path))

    # ===== CHECK FILE EXISTS =====
    if not os.path.exists(file_path):
        raise Http404(f"File not found: {filename}")

    # ===== RETURN FILE RESPONSE =====
    try:
        response = FileResponse(open(file_path, 'rb'), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    except Exception as e:
        print("ERROR:", str(e))
        raise Http404("Error while opening file")