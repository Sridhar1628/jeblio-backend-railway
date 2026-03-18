from django.contrib import admin
from django.core.mail import send_mail
from .models import InternshipApplication


@admin.register(InternshipApplication)
class InternshipApplicationAdmin(admin.ModelAdmin):

    list_display = (
        'full_name',
        'email',
        'internship_type',
        'status',
        'created_at'
    )

    list_filter = (
        'internship_type',
        'status',
        'created_at'
    )

    search_fields = (
        'full_name',
        'email',
        'phone'
    )

    def save_model(self, request, obj, form, change):

        # Get previous status
        if obj.pk:
            old_obj = InternshipApplication.objects.get(pk=obj.pk)

            # If status changed
            if old_obj.status != obj.status:

                # ✅ Approved Email
                if obj.status == 'approved':
                    send_mail(
                        subject="Congratulations! You are Selected 🎉",
                        message=f"""
Hi {obj.full_name},

Congratulations! 🎉

You have been selected for the {obj.internship_type} internship at Jeblio Corporation.

Our team will contact you with further details soon.

Best regards,  
Jeblio Team
""",
                        from_email='your_email@gmail.com',
                        recipient_list=[obj.email],
                        fail_silently=True,
                    )

                # ❌ Rejected Email
                elif obj.status == 'rejected':
                    send_mail(
                        subject="Internship Application Update",
                        message=f"""
Hi {obj.full_name},

Thank you for applying for the {obj.internship_type} internship.

We regret to inform you that you were not selected at this time.

We encourage you to apply again in the future.

Best regards,  
Jeblio Team
""",
                        from_email='your_email@gmail.com',
                        recipient_list=[obj.email],
                        fail_silently=True,
                    )

        super().save_model(request, obj, form, change)