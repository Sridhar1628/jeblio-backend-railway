from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import ApplicationCounter
from .utils import initialize_application_counter


@receiver(post_migrate)
def create_counter(sender, **kwargs):
    # Only run for our app
    if sender.name != "internships":
        return

    try:
        initialize_application_counter()
        print("✅ Counter initialized after migration")
    except Exception as e:
        print("Error initializing counter:", e)