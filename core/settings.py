import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-your-secret-key-here')

# 1. Correct logic for evaluating DEBUG from Environment
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# 2. Unified ALLOWED_HOSTS & Security Settings
ALLOWED_HOSTS = [
    'agenticdoctorassistant.onrender.com',
    'localhost',
    '127.0.0.1',
    '.onrender.com'
]

# Support for custom hostnames in env
env_hosts = os.getenv("ALLOWED_HOSTS")
if env_hosts:
    ALLOWED_HOSTS.extend(env_hosts.split(","))

# Mandatory for Render to trust HTTPS requests
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_TRUSTED_ORIGINS = [
    'https://agenticdoctorassistant.onrender.com',
    'https://*.onrender.com'
]

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# 3. Application Definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django.contrib.sites',
    
    # Third party apps
    'rest_framework',
    'corsheaders',
    'channels',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'widget_tweaks',
    
    # Local apps
    'apps.users',
    'apps.consultations',
    'apps.agents',
    'apps.blackboard',
    'apps.rag',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Static files
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'

# 4. Databases & Redis (FIXES CONNECTION ERROR 111)
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}

# Pull Redis URL from environment or default to local (for development)
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': REDIS_URL,
    }
}

try:
    import channels_redis
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {'hosts': [REDIS_URL]},
        },
    }
except ImportError:
    CHANNEL_LAYERS = {'default': {'BACKEND': 'channels.layers.InMemoryChannelLayer'}}

# Celery
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# 5. Rest Framework & CORS
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://localhost:8000',
]

# 6. Static & Media
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 7. Auth Settings
AUTH_USER_MODEL = 'users.User'
LOGIN_URL = 'account_login'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'
SITE_ID = 1

# 8. Email & Integrations
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'no-reply@mediai.local')

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
LAB_RESULTS_MODE = os.getenv('LAB_RESULTS_MODE', 'mock').lower()

# 9. Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {'format': '[{levelname}] {name}: {message}', 'style': '{'},
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'simple'},
    },
    'loggers': {
        'apps.agents': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
        'apps.blackboard': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
        'apps.consultations': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
        'django': {'handlers': ['console'], 'level': 'WARNING', 'propagate': True},
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'