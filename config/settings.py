
from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# CONFIGURACIÓN GENERAL
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "development-only-insecure-key-change-me"
)

DEBUG = os.getenv("DJANGO_DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


# BASE DE DATOS POSTGRESQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "guiospro_db",
        "USER": "postgres",
        "PASSWORD": "123",
        "HOST": "localhost",
        "PORT": "5432",
    }
}


# APLICACIONES
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "allauth",
    "allauth.account",

    "evaluacion",
]


# MIDDLEWARE
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]


# SESIONES
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"


# URLS
ROOT_URLCONF = "config.urls"


# PLANTILLAS
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ARCHIVOS ESTÁTICOS
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]


# CONFIGURACIÓN DE DJANGO
WSGI_APPLICATION = "config.wsgi.application"

LANGUAGE_CODE = "es"
TIME_ZONE = "America/Guayaquil"

USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# AUTENTICACIÓN
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]


# REDIRECCIONES
LOGIN_URL = "account_login"
LOGIN_REDIRECT_URL = "evaluacion:panel"
LOGOUT_REDIRECT_URL = "account_login"


# CONFIGURACIÓN DE DJANGO-ALLAUTH

# Iniciar sesión con correo electrónico
ACCOUNT_LOGIN_METHODS = {"email"}

# Campos obligatorios para el registro
ACCOUNT_SIGNUP_FIELDS = [
    "email*",
    "password1*",
    "password2*",
]

# Evitar correos duplicados
ACCOUNT_UNIQUE_EMAIL = True

# No exigir verificación de correo
ACCOUNT_EMAIL_VERIFICATION = "none"

# Formulario personalizado para nombres y apellidos
ACCOUNT_SIGNUP_FORM_CLASS = (
    "evaluacion.allauth_forms.RegistroAdicionalForm"
)

# CORREO LOCAL (SIN BREVO)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
