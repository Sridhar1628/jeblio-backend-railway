from django.db import models


class ProjectInquiry(models.Model):

    SERVICE_CHOICES = [
        ('software', 'Software Development'),
        ('marketing', 'Digital Marketing'),
        ('business', 'Business Development'),
        ('internship', 'Internship'),
        ('consultation', 'Consultation'),
        ('other', 'Other'),
    ]

    BUDGET_CHOICES = [
        ('under-50k', 'Under 50K'),
        ('50k-1l', '50K-1L'),
        ('1l-5l', '1L-5L'),
        ('5l-10l', '5L-10L'),
        ('above-10l', 'Above 10L'),
    ]

    URGENCY_CHOICES = [
        ('asap', 'ASAP'),
        ('1-month', '1 Month'),
        ('3-months', '3 Months'),
        ('6-months', '6 Months'),
        ('flexible', 'Flexible'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('contacted', 'Contacted'),
        ('closed', 'Closed'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=255, blank=True)

    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    project_budget = models.CharField(max_length=50, choices=BUDGET_CHOICES, blank=True)
    urgency = models.CharField(max_length=50, choices=URGENCY_CHOICES, blank=True)

    message = models.TextField()
    newsletter = models.BooleanField(default=False)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name