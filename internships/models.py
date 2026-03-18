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
    cgpa = models.CharField(max_length=20, blank=True)

    # Technical
    skills = models.TextField()
    experience = models.TextField(blank=True)
    portfolio = models.URLField(blank=True)

    # Additional
    motivation = models.TextField()
    availability = models.CharField(max_length=50)
    resume = models.URLField(blank=True)

    terms = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.internship_type}"