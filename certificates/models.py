from django.db import models

class Certificate(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    domain = models.CharField(max_length=255)
    project = models.CharField(max_length=255)

    start_date = models.DateField()
    end_date = models.DateField()
    issue_date = models.DateField()

    cert_id = models.CharField(max_length=100, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.cert_id}"