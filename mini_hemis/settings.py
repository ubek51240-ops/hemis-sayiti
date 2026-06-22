"""
Django settings for mini_hemis project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / '.env', override=True)
except ImportError:
    pass

# SECURITY WARNING: don't run with debug turned on in production!
# Production muhitida DEBUG=False qilish majburiy
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# SECURITY WARNING: keep the secret key used in production secret!
# Production muhitida .env faylida kuchli SECRET_KEY o'rnatish majburiy
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-this-in-production')
if SECRET_KEY == 'django-insecure-change-this-in-production' and not DEBUG:
    import warnings
    warnings.warn("⚠️ Production muhitida default SECRET_KEY ishlatilmoqda! .env faylida kuchli kalit o'rnating.")

ALLOWED_HOSTS = ['*']



# CSRF - ishonchli domenlar
if DEBUG:
    CSRF_TRUSTED_ORIGINS = [
        'http://localhost:8000',
        'http://127.0.0.1:8000',
        'https://*.ngrok-free.dev',
        'https://*.ngrok.io',
    ]
else:
    CSRF_TRUSTED_ORIGINS = [
        'https://hemis-sayiti.onrender.com',
        'https://riva.pythonanywhere.com',
        'https://*.ngrok-free.dev',
        'https://*.ngrok.io',
    ]

# CSRF Cookie sozlamalari
CSRF_COOKIE_DOMAIN = None
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SECURE = not DEBUG

# Proxy header recognition
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

# Application definition
INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'whitenoise.runserver_nostatic',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'axes',  # Login urinishlarini cheklash
    'channels',  # WebSocket va real-time chat
    
    # Local apps
    'core',
]

MIDDLEWARE = [
    'core.middleware.NgrokMiddleware',  # Ngrok proxy header rewriting (must be first)
    'core.middleware.SecurityHeadersMiddleware',  # Xavfsizlik headerlari
    'core.middleware.IPBlockMiddleware',  # IP bloklash
    'core.middleware.InputSanitizationMiddleware',  # Input sanitization
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'axes.middleware.AxesMiddleware',  # Brute-force himoyasi
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'core.middleware.RateLimitMiddleware',  # Rate limiting (auth'dan keyin joylashtirilishi kerak)
    'core.middleware.AdminSecurityMiddleware',  # Admin xavfsizligi (auth'dan keyin joylashtirilishi kerak)
    'core.middleware.LogoMiddleware',
    'core.middleware.AdminAxesBypassMiddleware',
    'core.middleware.SessionTimeoutMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'core.validators.UzbekUserAttributeSimilarityValidator'},
    {'NAME': 'core.validators.UzbekMinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'core.validators.UzbekCommonPasswordValidator'},
    {'NAME': 'core.validators.UzbekNumericPasswordValidator'},
    {'NAME': 'core.validators.ComplexPasswordValidator'},  # Kuchli parol validator
]

# Internationalization
LANGUAGE_CODE = 'uz-uz'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

# Session settings
SESSION_COOKIE_AGE = 1800  # 30 daqiqa
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Security settings - Development vs Production
if DEBUG:
    # Development settings (xavfsizlikni pasaytirmaslik uchun minimal)
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_HSTS_SECONDS = 0
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
else:
    # Production settings
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
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

# SITE_URL - used for generating absolute URLs (e.g. in emails and API responses)
SITE_URL = os.environ.get('SITE_URL', 'http://localhost:8000')

# Email settings - .env dan o'qiladi
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')

# Agar credentials bor bo'lsa - SMTP, aks holda console (terminal'ga chiqaradi)
if EMAIL_HOST_USER and EMAIL_HOST_PASSWORD:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', 'False').lower() == 'true'

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER or 'noreply@talabaqabul.uz')

# =============================================================================
# DJANGO-AXES SOZLAMALARI (Brute-force Himoyasi)
# =============================================================================

# Axes middleware - (Yagona MIDDLEWARE sozlamasi tepada e'lon qilindi)

# Authentication Backends - AxesStandaloneBackend qo'shildi
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',  # Django-axes 5.0+ yangi backend
    'django.contrib.auth.backends.ModelBackend',
]

# Asosiy axes sozlamalari
AXES_ENABLED = True
AXES_FAILURE_LIMIT = 5  # 5 ta noto'g'ri urinish
AXES_COOLOFF_TIME = 900  # 15 daqiqa bloklash (sekundlarda)
AXES_RESET_ON_SUCCESS = True
AXES_VERBOSE = True

# Bloklash parametrlari (username va ip_address bo'yicha)
AXES_LOCKOUT_PARAMETERS = ['username', 'ip_address']

# Bloklash sababini ko'rsatish
AXES_LOCKOUT_TEMPLATE = 'account_lockout.html'

# HTTP status code
AXES_HTTP_RESPONSE_CODE = 429

# PythonAnywhere Production Settings
if 'PYTHONANYWHERE' in os.environ:
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-this-in-production')
    
    # Database for PythonAnywhere
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('DB_NAME', 'your-username$mini_hemis'),
            'USER': os.environ.get('DB_USER', 'your-username'),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ.get('DB_HOST', 'your-username.mysql.pythonanywhere-services.com'),
            'PORT': os.environ.get('DB_PORT', '3306'),
        }
    }
    
    # Static files for PythonAnywhere
    STATIC_URL = '/static/'
    STATIC_ROOT = os.environ.get('STATIC_ROOT', '/home/your-username/minihemis/static/')
    
    # Media files for PythonAnywhere
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.environ.get('MEDIA_ROOT', '/home/your-username/minihemis/media/')
    
    # Email for PythonAnywhere
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
    
    # Additional security settings for production
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

# Axes faqat login sahifasini kuzatadi
