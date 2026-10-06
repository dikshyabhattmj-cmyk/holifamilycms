import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-a0mk*8kj(p8i_=hsz-w3qbz9%dvio%emr478sra-g1scmvcu&k')

DEBUG = True

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    'https://*.ngrok-free.app',
    'https://*.ngrok-free.dev',
    'https://*.ngrok.io',
    'https://*.ngrok.app',
    'https://*.ngrok.dev',
    'http://127.0.0.1',
    'http://localhost',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party
    'crispy_forms',
    'crispy_bootstrap5',

    # Local Apps
    'school',
    'portal',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'holifamily_core.middleware.NgrokBypassMiddleware',
]

ROOT_URLCONF = 'holifamily_core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'school.context_processors.school_global_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'holifamily_core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kathmandu'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'portal:login'
LOGIN_REDIRECT_URL = 'portal:dashboard'
LOGOUT_REDIRECT_URL = 'home'

# File upload security limits (15 MB max)
DATA_UPLOAD_MAX_MEMORY_SIZE = 15728640
FILE_UPLOAD_MAX_MEMORY_SIZE = 15728640

# Security Headers (Configured ready for production)
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# Web Push Notifications (VAPID Configuration)
WEBPUSH_VAPID_PUBLIC_KEY = os.environ.get(
    'WEBPUSH_VAPID_PUBLIC_KEY',
    'BJAu_rtTSBTvkDxM39I8aDbcIAxxwAGQ_OE_f_oXDqxifNW26L7VRiiKzltwDdIo28Jeg5R_Hq3N7CFt5zY8H0U'
)
WEBPUSH_VAPID_PRIVATE_KEY = os.environ.get(
    'WEBPUSH_VAPID_PRIVATE_KEY',
    str(BASE_DIR / 'private_key.pem')
)
WEBPUSH_ADMIN_EMAIL = os.environ.get('WEBPUSH_ADMIN_EMAIL', 'mailto:admin@holifamily.edu.np')

