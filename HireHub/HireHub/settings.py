from pathlib import Path

# -------------------------
# Base directory
# -------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------
# Security
# -------------------------
SECRET_KEY = 'django-insecure--1y6$bp-%8x&8!^!$9j8l&zwkj6ku!d@ragyxa=crfw*vw^9nu'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# -------------------------
# Installed apps
# -------------------------
INSTALLED_APPS = [
    # Django default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Allauth for authentication
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # Your apps
    'accounts',
    'applications',
    'jobs',
]

# -------------------------
# Middleware
# -------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# -------------------------
# URL configuration
# -------------------------
ROOT_URLCONF = 'HireHub.urls'

# -------------------------
# Templates
# -------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',  # Required by allauth
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# -------------------------
# WSGI
# -------------------------
WSGI_APPLICATION = 'HireHub.wsgi.application'

# -------------------------
# Database
# -------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# -------------------------
# Password validation
# -------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -------------------------
# Internationalization
# -------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# -------------------------
# Static files
# -------------------------
STATIC_URL = 'static/'

# -------------------------
# Django Sites
# -------------------------
SITE_ID = 1

# -------------------------
# Authentication backends
# -------------------------
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # default
    'allauth.account.auth_backends.AuthenticationBackend',  # allauth
)

# -------------------------
# Allauth settings
# -------------------------
SOCIALACCOUNT_AUTO_SIGNUP = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False

# settings.py
SESSION_COOKIE_AGE = 1209600  # default 2 weeks, but optional
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # <- important

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# -------------------------
# Social account providers
# -------------------------
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    }
}

# -------------------------
# Email backend for testing
# -------------------------
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'