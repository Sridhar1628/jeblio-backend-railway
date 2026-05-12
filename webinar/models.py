from django.db import models

class TermsAndConditions(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class WebinarRegistration(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    payment_id = models.CharField(max_length=255)
    order_id = models.CharField(max_length=255)

    payment_status = models.CharField(max_length=50, default="PENDING")
    payment_method = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
    
class WebinarLead(models.Model):

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    order_id = models.CharField(max_length=255, unique=True)

    payment_status = models.CharField(
        max_length=50,
        default="PENDING"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
