from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/certificates/', include('certificates.urls')),
    path('api/internships/', include('internships.urls')),
    path('api/projects/', include('projects.urls')),
    path('api/', include('chatbot.urls')),
    path('api/webinar/', include('webinar.urls')),
    path('api/unlock-engine/', include('unlock_engine.api.urls')),
    path("api/users/", include("users.urls")),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)