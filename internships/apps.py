from django.apps import AppConfig


class InternshipsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'internships'

    def ready(self):
        try:
            from .utils import initialize_application_counter
            initialize_application_counter()
        except Exception as e:
            print("Initialization error:", e)