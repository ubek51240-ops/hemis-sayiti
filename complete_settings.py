"""
Django settings for mini_hemis project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# SECURITY WARNING: keep the secret key used in production secret!
# Production muhitida .env faylida kuchli SECRET_KEY o'rnatish majburiy
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-this-in-production')
if SECRET_KEY == 'django-insecure-change-this-in-production' and not DEBUG:
    import warnings
    warnings.warn("⚠️ Production muhitida default SECRET_KEY ishlatilmoqda! .env faylida kuchli kalit o'rnating.")

# PRODUCTION MODE - Xavfsizlik uchun majburiy
PRODUCTION = os.environ.get('PRODUCTION', 'False').lower() == 'true'

# ALLOWED_HOSTS - Xavfsizlik uchun faqat aniq domenlar
if DEBUG:
    ALLOWED_HOSTS = [
        'localhost',
        '127.0.0.1',
        '0.0.0.0',
        '10.42.0.251',
    ]
else:
    ALLOWED_HOSTS = [
        'hemis-sayiti.onrender.com',
        'riva.pythonanywhere.com',
    ]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'django_axes',
    'channels',  # WebSocket va real-time chat
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
]

ROOT_URLCONF = 'mini_hemis.urls'

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
                'core.context_processors.active_role',
            ],
        },
    },
]

WSGI_APPLICATION = 'mini_hemis.wsgi.application'
ASGI_APPLICATION = 'mini_hemis.asgi.application'

# Channel Layers (WebSocket uchun)
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# PythonAnywhere Production Settings
if 'PYTHONANYWHERE' in os.environ:
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-this-in-production')
    
    # Database for PythonAnywhere
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('DB_NAME', 'riva$mini_hemis'),
            'USER': os.environ.get('DB_USER', 'riva'),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ.get('DB_HOST', 'riva.mysql.pythonanywhere-services.com'),
            'PORT': os.environ.get('DB_PORT', '3306'),
        }
    }
    
    # Static files for PythonAnywhere
    STATIC_URL = '/static/'
    STATIC_ROOT = os.environ.get('STATIC_ROOT', '/home/riva/minihemis/static/')
    
    # Media files for PythonAnywhere
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.environ.get('MEDIA_ROOT', '/home/riva/minihemis/media/')
    
    # Additional security settings for production
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

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
LANGUAGE_CODE = 'uz'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# CORS - XAVFSIZLIK: Faqat aniq domenlarga ruxsat
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOW_CREDENTIALS = True
else:
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOWED_ORIGINS = [
        'https://hemis-sayiti.onrender.com',
        'https://riva.pythonanywhere.com',
    ]
    CORS_ALLOW_METHODS = [
        'GET',
        'POST',
        'PUT',
        'PATCH',
        'DELETE',
        'OPTIONS',
    ]
    CORS_ALLOW_HEADERS = [
        'accept',
        'accept-encoding',
        'authorization',
        'content-type',
        'dnt',
        'origin',
        'user-agent',
        'x-csrftoken',
        'x-requested-with',
    ]

# CSRF Trusted Origins - faqat production domenlari
if DEBUG:
    CSRF_TRUSTED_ORIGINS = [
        'http://127.0.0.1:8000',
        'http://localhost:8000',
    ]
else:
    CSRF_TRUSTED_ORIGINS = [
        'https://hemis-sayiti.onrender.com',
        'https://riva.pythonanywhere.com',
    ]

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# =============================================================================
# DJANGO-AXES SOZLAMALARI (Brute-force Himoyasi)
# =============================================================================

# Authentication Backends - AxesStandaloneBackend qo'shildi
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',  # Django-axes 5.0+ yangi backend
    'core.backends.AxesAdminExemptBackend',  # Admin uchun maxsus backend
    'django.contrib.auth.backends.ModelBackend',
]

# Asosiy axes sozlamalari
AXES_ENABLED = True
AXES_FAILURE_LIMIT = 5  # 5 ta noto'g'ri urinish
AXES_COOLOFF_TIME = 300  # 5 daqiqa bloklash (sekundlarda)
AXES_RESET_ON_SUCCESS = True  # Muvaffaqiyatli login dan keyin reset
AXES_VERBOSE = True  # Log yozish

# Bloklash parametrlari (username + IP birgalikda)
AXES_LOCKOUT_PARAMETERS = [['username', 'ip_address']]

# Bloklash sababini ko'rsatish
AXES_LOCKOUT_TEMPLATE = 'account_lockout.html'

# Email xabarnoma (ixtiyoriy)
# AXES_EMAIL = ['admin@example.com']
# AXES_EMAIL_FROM = 'security@example.com'

# AxesMiddleware joylashuvi (MIDDLEWARE da) tekshirildi ✅

# =============================================================================
# KUCHLI XAVFSIZLIK SOZLAMALARI
# =============================================================================

# 1. SESSION VA COOKIE XAVFSIZLIGI
SESSION_COOKIE_SECURE = not DEBUG  # HTTPS da ishlash uchun
SESSION_COOKIE_HTTPONLY = True  # JavaScript dan himoya
SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF himoyasi (Strict ba'zi funksiyalarni buzishi mumkin)
CSRF_COOKIE_SECURE = not DEBUG  # HTTPS da ishlash uchun
CSRF_COOKIE_HTTPONLY = True  # JavaScript dan himoya
CSRF_COOKIE_SAMESITE = 'Lax'  # CSRF himoyasi

# Session vaqtini cheklash (30 daqiqa)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 1800  # 30 daqiqa

# 2. HTTPS VA SSL/TLS SOZLAMALARI
SECURE_SSL_REDIRECT = not DEBUG  # HTTP dan HTTPS ga yo'naltirish
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# HSTS faqat productionda
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000  # 1 yil
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False

# 3. BROWSER XAVFSIZLIK HEADERLARI
SECURE_BROWSER_XSS_FILTER = True  # XSS filter
SECURE_CONTENT_TYPE_NOSNIFF = True  # MIME type sniffing ni bloklash
X_FRAME_OPTIONS = 'DENY'  # Clickjacking himoyasi
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# 4. CONTENT SECURITY POLICY (CSP)
# XSS va data injection hujumlaridan himoya
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'") if DEBUG else ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_IMG_SRC = ("'self'", "data:", "https:")
CSP_FONT_SRC = ("'self'", "https:", "data:")
CSP_CONNECT_SRC = ("'self'",)
CSP_FRAME_ANCESTORS = ("'none'",)  # Clickjacking himoyasi
CSP_BASE_URI = ("'self'",)
CSP_FORM_ACTION = ("'self'",)

# 5. DJANGO-DEFENDER SOZLAMALARI (Brute-force himoyasi)
DEFENDER_LOGIN_FAILURE_LIMIT = 5  # 5 ta noto'g'ri urinish
DEFENDER_COOLOFF_TIME = 300  # 5 daqiqa bloklash
DEFENDER_LOCKOUT_TEMPLATE = 'defender/lockout.html'
DEFENDER_STORE_ACCESS_ATTEMPTS = True  # Urinlarni saqlash
DEFENDER_USE_CELERY = False  # Celery ishlatilmaydi
DEFENDER_LOCKOUT_IP = True  # IP bo'yicha bloklash
DEFENDER_LOCKOUT_USERNAME = True  # Username bo'yicha bloklash
DEFENDER_BEHIND_REVERSE_PROXY = False
DEFENDER_DISABLE_IP_LOCKOUT = False
DEFENDER_DISABLE_USERNAME_LOCKOUT = False

# 6. RATE LIMITING SOZLAMALARI
RATELIMIT_VIEW = 'core.views.rate_limited'  # Rate limit view
RATELIMIT_BLOCK = True  # Bloklashni yoqish
RATELIMIT_STRATEGY = 'fixed-window'  # Fixed window strategiya

# 7. PASSWORD VALIDATORS (kuchli parollar uchun)
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 12,  # Minimum 12 ta belgi
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    # Maxfiy xavfsizlik validator
    {
        'NAME': 'core.validators.ComplexPasswordValidator',
    },
]

# 8. ADMIN XAVFSIZLIGI
ADMIN_LOGIN_ATTEMPTS = 3  # Admin uchun 3 ta urinish
ADMIN_LOCKOUT_DURATION = 1800  # 30 daqiqa bloklash

# 9. FILE UPLOAD XAVFSIZLIGI
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5 MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5 MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000  # Max field limit
DATA_UPLOAD_MAX_NUMBER_FILES = 10  # Max file limit

# 10. LOGGING VA MONITORING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        'security': {
            'format': '[SECURITY] {asctime} - {levelname} - {module} - {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'maxBytes': 10485760,  # 10 MB
            'backupCount': 10,
            'formatter': 'verbose'
        },
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'security.log',
            'maxBytes': 10485760,  # 10 MB
            'backupCount': 10,
            'formatter': 'security'
        },
        'auth_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'auth.log',
            'maxBytes': 10485760,  # 10 MB
            'backupCount': 10,
            'formatter': 'security'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.security': {
            'handlers': ['security_file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['security_file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
        'axes.watch_login': {
            'handlers': ['auth_file', 'console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'defender': {
            'handlers': ['auth_file', 'console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'core.security': {
            'handlers': ['security_file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# 11. REST FRAMEWORK XAVFSIZLIGI
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10/minute',  # Anonim foydalanuvchilar uchun
        'user': '100/minute',  # Autentifikatsiya qilingan foydalanuvchilar uchun
    },
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# 12. SECURITY MIDDLEWARE (qo'shimcha middleware)
MIDDLEWARE = [
    'core.middleware.SecurityHeadersMiddleware',  # Xavfsizlik headerlari
    'core.middleware.RateLimitMiddleware',  # Rate limiting
    'core.middleware.IPBlockMiddleware',  # IP bloklash
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
    'defender.middleware.FailedLoginMiddleware',  # Django-defender
    'csp.middleware.CSPMiddleware',  # Content Security Policy
]

# 13. INSTALLED APPS (xavfsizlik paketlari)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'django_axes',
    'defender',  # Django-defender
    'csp',  # Django-csp
    'core',
]

# 14. DATABASE XAVFSIZLIGI
# SQL Injection himoyasi uchun parametrlangan so'rovlardan foydalanish
DATABASES['default']['OPTIONS'] = {
    'charset': 'utf8mb4',
}

# 15. MEDIA FILE XAVFSIZLIGI
# Faqat ruxsat etilgan file turlari
ALLOWED_FILE_TYPES = [
    'image/jpeg',
    'image/png',
    'image/gif',
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.ms-excel',
]
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

# 16. BLOKLANGAN IP MANZILLAR (dynamic ravishda qo'shiladi)
BLOCKED_IPS = []  # core.middleware da ishlatiladi

# 17. WHITELISTED IP MANZILLAR (admin panel uchun)
ADMIN_WHITELIST_IPS = []  # faqat shu IP lar admin panelga kirishi mumkin

# 18. HONEYPOT SOZLAMALARI (botlarni aniqlash uchun)
HONEYPOT_FIELD_NAME = 'website'  # Botlar to'ldiradigan yashirin maydon

# 19. XAVFSIZLIK XABARLARI
SECURITY_CONTACT_EMAIL = os.environ.get('SECURITY_EMAIL', 'security@example.com')

# 20. MA'LUMOTLAR SHIFRLASHI (sensitive data uchun)
ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY', SECRET_KEY[:32])

print("✅ KUCHLI XAVFSIZLIK TIZIMI YOQILDI")
print(f"   - DEBUG: {DEBUG}")
print(f"   - HTTPS: {not DEBUG}")
print(f"   - CSP: ENABLED")
print(f"   - Rate Limiting: ENABLED")
print(f"   - Brute-force Protection: ENABLED")
