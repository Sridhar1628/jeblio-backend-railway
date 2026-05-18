from pathlib import Path
import os
import dj_database_url
from corsheaders.defaults import default_headers
from dotenv import load_dotenv
import os



load_dotenv()

FRONTEND_URL = os.getenv("FRONTEND_URL")
# ======================
# BASE
# ======================
BASE_DIR = Path(__file__).resolve().parent.parent

# ======================
# SECURITY
# ======================
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-fallback-key-for-railway"
)

DEBUG = True
ALLOWED_HOSTS = [
    "api.jeblio.com",
    "jeblio.com",
    "www.jeblio.com",
    "127.0.0.1",
    "localhost",
]

CSRF_TRUSTED_ORIGINS = [
    "https://api.jeblio.com",
    "https://jeblio.com",
    "https://www.jeblio.com",
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

USE_X_FORWARDED_HOST = True
SECURE_SSL_REDIRECT = False

# ======================
# APPLICATIONS
# ======================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',

    'corsheaders',

    'certificates',
    'users',
    'internships.apps.InternshipsConfig',
    'services',
    'projects',
    'chatbot',
    'webinar',
    'unlock_engine',
]

# ======================
# MIDDLEWARE
# ======================
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # MUST BE FIRST
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ======================
# URL / WSGI
# ======================
ROOT_URLCONF = 'jeblioweb_backend.urls'

WSGI_APPLICATION = 'jeblioweb_backend.wsgi.application'

# ======================
# TEMPLATES
# ======================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ======================
# DATABASE
# ======================

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# ======================
# PASSWORD VALIDATION
# ======================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ======================
# INTERNATIONALIZATION
# ======================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ======================
# STATIC / MEDIA
# ======================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ======================
# SENDGRID EMAIL
# ======================

EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")

SENDGRID_SANDBOX_MODE_IN_DEBUG = False

DEFAULT_FROM_EMAIL = "noreply@jeblio.com"

print("SENDGRID LOADED:", bool(SENDGRID_API_KEY))


# ======================
# CORS SETTINGS
# ======================
CORS_ALLOWED_ORIGINS = [
    "https://jeblio.com",
    "https://www.jeblio.com",
    "https://jeblio-website.onrender.com",
    "http://localhost:3000"
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = list(default_headers) + [
    "content-type",
    "authorization"
]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CORS_EXPOSE_HEADERS = ["Content-Type"]

# ======================
# CSRF
# ======================


# ======================
# DRF
# ======================
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ]
}

RAZORPAY_KEY_ID = "rzp_test_xxxxx"
RAZORPAY_KEY_SECRET = "xxxxxxxx"

# ======================
# CASHFREE
# ======================

CASHFREE_ENV = os.environ.get("CASHFREE_ENV", "SANDBOX")

CASHFREE_APP_ID = os.environ.get("CASHFREE_APP_ID")
CASHFREE_SECRET_KEY = os.environ.get("CASHFREE_SECRET_KEY")

CASHFREE_ENVIRONMENT = "SANDBOX"


ADMIN_EMAIL = "jeblioinfo@gmail.com"