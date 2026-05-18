from django.urls import path
from .views import CreateSuperUserView, test_db

urlpatterns = [
    path(
        "create-superuser/",
        CreateSuperUserView.as_view(),
        name="create-superuser",
    ),
    path("test-db/", test_db),
]