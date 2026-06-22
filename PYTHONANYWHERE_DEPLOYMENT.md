# PythonAnywhere Deployment Guide

## Kerakli Narsalar
- PythonAnywhere account (Free yoki Paid)
- GitHub repository
- MySQL database

## 1-Qadam: PythonAnywhere Setup

### 1.1 Account Yaratish
1. [pythonanywhere.com](https://pythonanywhere.com) ga kirib ro'yxatdan o'ting
2. Free account yoki paid account tanlang

### 1.2 Project Yaratish
1. "Web" section ga kering
2. "Add a new web app" bosing
3. "Manual configuration" tanlang
4. Python 3.11+ tanlang

## 2-Qadam: Kodni Pull Qilish

### 2.1 Git Repository Clone
```bash
git clone https://github.com/ubek51240-ops/hemis-sayiti.git
cd hemis-sayiti
```

### 2.2 Virtual Environment Yaratish
```bash
python -m venv venv
source venv/bin/activate
```

### 2.3 Packages Install
```bash
pip install -r requirements.txt
```

## 3-Qadam: Database Setup

### 3.1 MySQL Database Yaratish
1. PythonAnywhere "Databases" section ga kering
2. "Create a new database" bosing
3. Database name: `mini_hemis`
4. MySQL username va parolni saqlang

### 3.2 Settings.py ni Yangilash
`settings.py` da quyidagilarni o'zingizga moslashtiring:
```python
# 'your-username' ni PythonAnywhere username bilan almashtiring
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your-username$mini_hemis',
        'USER': 'your-username',
        'PASSWORD': 'your-db-password',
        'HOST': 'your-username.mysql.pythonanywhere-services.com',
        'PORT': '3306',
    }
}
```

## 4-Qadam: Migrations

### 4.1 Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4.2 Superadmin Yaratish
```bash
python manage.py createsuperuser
```

### 4.3 Static Files
```bash
python manage.py collectstatic
```

## 5-Qadam: Web App Configuration

### 5.1 WSGI File
`/var/www/your-username_pythonanywhere_com_wsgi.py` faylini yangilang:
```python
import os
import sys

path = '/home/your-username/hemis-sayiti'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'mini_hemis.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 5.2 Environment Variables
Web app settings da quyidagi environment variables qo'shing:
```
SECRET_KEY=your-secret-key-here
DB_PASSWORD=your-db-password
PYTHONANYWHERE=1
```

## 6-Qadam: Static Files Setup

### 6.1 Static Files Path
Web app settings da:
- Static files URL: `/static/`
- Static files directory: `/home/your-username/hemis-sayiti/static/`

### 6.2 Static Files Collect
```bash
python manage.py collectstatic --noinput
```

## 7-Qadam: Security Settings

### 7.1 ALLOWED_HOSTS
`settings.py` da:
```python
ALLOWED_HOSTS = [
    'your-username.pythonanywhere.com',
    'hemis-sayiti.onrender.com',
    'localhost',
    '127.0.0.1',
]
```

### 7.2 DEBUG Mode
```python
DEBUG = False
SECRET_KEY = os.environ['SECRET_KEY']
```

## 8-Qadam: Test va Launch

### 8.1 Web App Reload
1. PythonAnywhere "Web" section ga kering
2. "Reload" button bosing
3. Loglarni tekshiring

### 8.2 Test
- `https://your-username.pythonanywhere.com` ga kiring
- Login ishlaydimi?
- Static files yuklanadimi?

## 9-Qadam: Muammolar va Yechimlar

### 9.1 IndentationError in manage.py
**Xatolik:** `IndentationError: unexpected indent`
**Yechim:**
```bash
# Yangi kodni pull qiling
git pull origin main

# Manage.py ni tekshiring
cat manage.py

# Agar xato bo'lsa, to'g'rilang:
nano manage.py
```

**To'g'ri manage.py:**
```python
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
```

### 9.2 Database Connection Error
```bash
# MySQL client o'rnatish
pip install mysqlclient

# Environment variables tekshiring
echo $DB_PASSWORD
echo $DB_NAME
```

### 9.3 Static Files Error
```bash
# Static files path tekshirish
ls -la /home/your-username/hemis-sayiti/static/

# Static files collect
python manage.py collectstatic --noinput
```

### 9.4 502 Bad Gateway
- Web app reload qiling
- WSGI file tekshiring
- Loglarni ko'ring
- Virtual environment tekshiring

### 9.5 ModuleNotFoundError
```bash
# Barcha packages install qiling
pip install -r requirements.txt

# Virtual environment tekshiring
which python
python --version
```

## 10-Qadam: Auto Update (Optional)

### 10.1 Pull Script
```bash
#!/bin/bash
cd /home/your-username/hemis-sayiti
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
touch /var/www/your-username_pythonanywhere_com_wsgi.py
```

## Muvaffaqiyat Testi

- [ ] Login ishlaydi
- [ ] Chat ishlaydi
- [ ] Static files yuklanadi
- [ ] Database ishlaydi
- [ ] Admin panel ishlaydi

Muammo bo'lsa, PythonAnywhere loglarini tekshiring!
