import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================
# SECURITY
# ==============================

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-change-this-key"
)

DEBUG = os.getenv(
    "DEBUG",
    "False"
).lower() == "true"


ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".onrender.com",
]


CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
]


# ==============================
# APPLICATIONS
# ==============================

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'users',
    'cars',
    'bookings',
    'recommendations',
    'analytics',
]


# ==============================
# MIDDLEWARE
# ==============================

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'config.urls'


# ==============================
# TEMPLATES
# ==============================

TEMPLATES = [

    {
        'BACKEND':
        'django.template.backends.django.DjangoTemplates',

        'DIRS': [
            BASE_DIR / 'templates'
        ],

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


WSGI_APPLICATION = 'config.wsgi.application'


# ==============================
# DATABASE
# Render PostgreSQL
# ==============================

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "yourdriveai",
            "USER": "postgres",
            "PASSWORD": "postgres",
            "HOST": "localhost",
            "PORT": "5432",
        }
    }


# ==============================
# PASSWORD VALIDATION
# ==============================

AUTH_PASSWORD_VALIDATORS = []


# ==============================
# LANGUAGE
# ==============================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True



# ==============================
# STATIC FILES
# ==============================


STATIC_URL = '/static/'


STATICFILES_DIRS = [

    BASE_DIR / 'static'

]


STATIC_ROOT = BASE_DIR / 'staticfiles'


STATICFILES_STORAGE = (

    'whitenoise.storage.CompressedManifestStaticFilesStorage'

)



# ==============================
# MEDIA FILES
# ==============================


MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'



DEFAULT_AUTO_FIELD = (
    'django.db.models.BigAutoField'
)



# ==============================
# AUTH
# ==============================


LOGIN_REDIRECT_URL = 'home'

LOGOUT_REDIRECT_URL = 'home'

LOGIN_URL = 'login'



# ==============================
# EMAIL
# ==============================


if os.getenv('EMAIL_HOST'):

    EMAIL_BACKEND = (
        'django.core.mail.backends.smtp.EmailBackend'
    )

    EMAIL_HOST = os.getenv('EMAIL_HOST')

    EMAIL_PORT = int(
        os.getenv('EMAIL_PORT','587')
    )

    EMAIL_USE_TLS = True


    EMAIL_HOST_USER = os.getenv(
        'EMAIL_HOST_USER'
    )


    EMAIL_HOST_PASSWORD = os.getenv(
        'EMAIL_HOST_PASSWORD'
    )


else:

    EMAIL_BACKEND = (
        'django.core.mail.backends.console.EmailBackend'
    )



DEFAULT_FROM_EMAIL = os.getenv(
    'DEFAULT_FROM_EMAIL',
    'noreply@yourdriveai.com'
)



# ==============================
# PRODUCTION SECURITY
# ==============================


if not DEBUG:

    SECURE_SSL_REDIRECT = True

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True



# ==============================
# LOGGING
# ==============================


LOGGING = {

    'version': 1,

    'disable_existing_loggers': False,

    'handlers': {

        'console': {

            'class':
            'logging.StreamHandler',

        },

    },


    'loggers': {

        'bookings': {

            'handlers': [
                'console'
            ],

            'level':
            'INFO',

        },

    },

}