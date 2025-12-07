"""
Django settings for mypos project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-mypos-secret-key-change-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# CSRF settings for Cloud9
# Cloud9 uses dynamic subdomains like: https://[ID].vfs.cloud9.[region].amazonaws.com
# Add your specific Cloud9 URL here (from the error message or browser address bar)

CSRF_TRUSTED_ORIGINS = [
    'https://1319ddcff73146a496c752c092761686.vfs.cloud9.us-east-1.amazonaws.com',
    # Add more Cloud9 URLs here if needed
    # The Cloud9CsrfMiddleware will also try to auto-detect and add Cloud9 origins
]

# Additional CSRF settings for Cloud9 development
# These settings help with Cloud9's proxy setup
CSRF_COOKIE_SECURE = False  # Set to False for Cloud9 (uses HTTPS proxy)
CSRF_COOKIE_SAMESITE = 'Lax'  # More permissive for Cloud9
CSRF_USE_SESSIONS = False  # Use cookie-based CSRF tokens


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pos',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'mypos.csrf.Cloud9CsrfViewMiddleware',  # Custom Cloud9 CSRF middleware (replaces default)
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mypos.urls'

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

WSGI_APPLICATION = 'mypos.wsgi.application'


# Database - Using DynamoDB via boto3, not Django's default DB
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
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


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (uploaded images)
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# AWS Configuration - Will use default credentials from AWS Academy
AWS_REGION = 'us-east-1'  # Default region, can be changed

# DynamoDB Tables
DYNAMODB_CUSTOMERS_TABLE = 'mypos-customers'
DYNAMODB_TRANSACTIONS_TABLE = 'mypos-transactions'

# S3 Bucket
# Note: S3 bucket names must be globally unique. Change this to a unique name if you get a conflict.
# Example: 'mypos-product-images-yourname-12345'
S3_BUCKET_NAME = 'mypos-product-images'

# SNS Topic
SNS_TOPIC_ARN = None  # Will be created programmatically

