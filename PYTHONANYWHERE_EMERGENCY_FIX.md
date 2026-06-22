# PythonAnywhere Emergency Fix

## AGAR FAYLLAR YO'Q BO'LSA

PythonAnywhere da cloned repository da fayllar yo'q bo'lsa, quyidagilarni qo'lda bajaring:

### 1-Qadam: To'liq Django project yaratish

```bash
cd ~/hemis-sayiti

# Manage.py yaratish
cat > manage.py << 'EOF'
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mini_hemis.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
EOF

chmod +x manage.py
```

### 2-Qadam: mini_hemis package yaratish

```bash
mkdir -p mini_hemis
touch mini_hemis/__init__.py
```

### 3-Qadam: Settings.py yaratish

```bash
cat > mini_hemis/settings.py << 'EOF'
"""
Django settings for mini_hemis project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = [
    'hemis-sayiti.onrender.com',
    'riva.pythonanywhere.com',
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    '*',
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
            ],
        },
    },
]

WSGI_APPLICATION = 'mini_hemis.wsgi.application'

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

# CORS
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# CSRF Trusted Origins for browser preview and PythonAnywhere
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:42613',
    'http://localhost:42613',
    'https://riva.pythonanywhere.com',
]

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# AXES SOZLAMALARI
AUTHENTICATION_BACKENDS = [
    'core.backends.AxesAdminExemptBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AXES_ENABLED = True
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 0.25
AXES_RESET_ON_SUCCESS = True
AXES_VERBOSE = True

AXES_LOCK_OUT_BY_USER = True
AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = False

AXES_LOCKOUT_TEMPLATE = 'account_lockout.html'
AXES_EMAIL = None
AXES_EMAIL_FROM = None
AXES_LOCKOUT_PARAMETERS = ['username']
EOF
```

### 4-Qadam: URLs.py yaratish

```bash
cat > mini_hemis/urls.py << 'EOF'
"""
URL configuration for mini_hemis project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

# Static files serving during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
EOF
```

### 5-Qadam: WSGI.py yaratish

```bash
cat > mini_hemis/wsgi.py << 'EOF'
"""
WSGI config for mini_hemis project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mini_hemis.settings')

application = get_wsgi_application()
EOF
```

### 6-Qadam: Test

```bash
python manage.py collectstatic
```

### 7-Qadam: Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 8-Qadam: Superuser

```bash
python manage.py createsuperuser
```

Endi barcha fayllar tayyor! Web app ni konfiguratsiya qiling!
