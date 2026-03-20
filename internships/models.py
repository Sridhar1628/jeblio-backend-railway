from django.db import models

class InternshipApplication(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    internship_type = models.CharField(max_length=100)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # Personal Info
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    # Education
    college = models.CharField(max_length=150)
    course = models.CharField(max_length=100)
    year = models.CharField(max_length=20)

    terms = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.internship_type}"

    class Meta:
        unique_together = ['email', 'internship_type']

# models.py
from django.db import models
from django.utils import timezone


class ApplicationCounter(models.Model):
    base_count = models.IntegerField(default=100)

    # When counting starts
    start_time = models.DateTimeField(default=timezone.now)

    # Fixed deadline (March 29, 2026, 6:30 PM IST)
    end_time = models.DateTimeField()

    # Stores per 30-min interval totals (pre-generated)
    increments = models.JSONField(default=list, blank=True)

    # Optional: for tracking/debugging
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Application Counter (Base: {self.base_count})"