# PythonAnywhere Complete Deployment Guide

## MUAMMOLARNI TO'LIQ HAL QILISH

### 1-QADAM: ESKI REPOSITORY NI O'CHIRISH
```bash
cd ~
rm -rf hemis-sayiti
```

### 2-QADAM: YANGI REPOSITORY NI CLONE QILISH
```bash
git clone https://github.com/ubek51240-ops/hemis-sayiti.git
cd hemis-sayiti
```

### 3-QADAM: VIRTUAL ENVIRONMENT YARATISH
```bash
python -m venv hemis-env
source hemis-env/bin/activate
```

### 4-QADAM: PACKAGES INSTALL
```bash
pip install -r requirements.txt
```

### 5-QADAM: DATABASE SETUP
1. PythonAnywhere "Databases" section ga kiring
2. MySQL database yarating: `mini_hemis`
3. Username va parolni eslab qoling

### 6-QADAM: ENVIRONMENT VARIABLES QO'SHISH
PythonAnywhere Web tab -> Variables section:
```
SECRET_KEY=django-insecure-your-secret-key-here
DB_PASSWORD=your-db-password
DB_NAME=your-username$mini_hemis
DB_USER=your-username
DB_HOST=your-username.mysql.pythonanywhere-services.com
DB_PORT=3306
PYTHONANYWHERE=1
DEBUG=False
```

### 7-QADAM: SETTINGS.PY NI TO'G'RILASH
`mini_hemis/settings.py` da `your-username` ni o'zingizning PythonAnywhere username bilan almashtiring:
```python
# ALLOWED_HOSTS da
'your-username.pythonanywhere.com',

# Database section da
'NAME': os.environ.get('DB_NAME', 'your-username$mini_hemis'),
'USER': os.environ.get('DB_USER', 'your-username'),
'HOST': os.environ.get('DB_HOST', 'your-username.mysql.pythonanywhere-services.com'),
```

### 8-QADAM: STATIC FILES
```bash
mkdir -p /home/your-username/minihemis/static
python manage.py collectstatic --noinput
```

### 9-QADAM: MIGRATIONS
```bash
python manage.py makemigrations
python manage.py migrate
```

### 10-QADAM: SUPERUSER YARATISH
```bash
python manage.py createsuperuser
```

### 11-QADAM: WEB APP SETUP
1. PythonAnywhere "Web" section ga kiring
2. "Add a new web app" -> "Manual configuration" -> Python 3.11
3. Source code: `/home/your-username/hemis-sayiti`
4. Working directory: `/home/your-username/hemis-sayiti`
5. WSGI configuration file: `/var/www/your-username_pythonanywhere_com_wsgi.py`

### 12-QADAM: WSGI FILE CONFIGURATION
`/var/www/your-username_pythonanywhere_com_wsgi.py` faylini quyidagiga o'zgartiring:
```python
import os
import sys
import django

path = '/home/your-username/hemis-sayiti'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mini_hemis.settings')

django.setup()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 13-QADAM: STATIC FILES PATH
Web app settings:
- Static files URL: `/static/`
- Static files directory: `/home/your-username/minihemis/static/`

### 14-QADAM: RELOAD VA TEST
1. "Reload" button bosing
2. `https://your-username.pythonanywhere.com` ga kiring
3. Login ishlaydimi?

## MUAMMOLAR VA YECHIMLARI

### MUAMMO 1: IndentationError
**Xatolik:** `IndentationError: unexpected indent`
**Yechim:** Repository ni qayta clone qiling, bizda to'g'ri versiya bor

### MUAMMO 2: ModuleNotFoundError
**Xatolik:** `ModuleNotFoundError: No module named 'mini_hemis'`
**Yechim:** 
```bash
pip install -r requirements.txt
source hemis-env/bin/activate
```

### MUAMMO 3: Database Connection Error
**Xatolik:** `django.db.backends.mysql: Error`
**Yechim:** Environment variables tekshiring
```bash
echo $DB_PASSWORD
echo $DB_NAME
```

### MUAMMO 4: Static Files Error
**Xatolik:** Static files yuklanmayapti
**Yechim:**
```bash
python manage.py collectstatic --noinput
ls -la /home/your-username/minihemis/static/
```

### MUAMMO 5: 502 Bad Gateway
**Yechim:** 
1. Web app reload qiling
2. WSGI file tekshiring
3. Loglarni ko'ring
4. Virtual environment tekshiring

## TEZ TEST UCHUN SKRIPT
```bash
#!/bin/bash
echo "PythonAnywhere Quick Setup"

# 1. Clone repository
cd ~
rm -rf hemis-sayiti
git clone https://github.com/ubek51240-ops/hemis-sayiti.git
cd hemis-sayiti

# 2. Virtual environment
python -m venv hemis-env
source hemis-env/bin/activate

# 3. Install packages
pip install -r requirements.txt

# 4. Migrations
python manage.py makemigrations
python manage.py migrate

# 5. Static files
mkdir -p /home/your-username/minihemis/static
python manage.py collectstatic --noinput

echo "Setup complete! Configure web app now."
```

## QO'LDA YOZISH (SKRIPT ISHLAMAGANDA)

Agar avtomatik skript ishlamasa, quyidagilarni qo'lda bajaring:

### 1-Qadam: Toza qilish
```bash
cd ~
rm -rf hemis-sayiti
git clone https://github.com/ubek51240-ops/hemis-sayiti.git
cd hemis-sayiti
```

### 2-Qadam: Virtual environment
```bash
python -m venv hemis-env
source hemis-env/bin/activate
```

### 3-Qadam: Packages install
```bash
pip install django djangorestframework whitenoise mysqlclient django-axes django-cors-headers pillow openpyxl gunicorn
```

### 4-Qadam: Settings to'g'rilash
```bash
nano mini_hemis/settings.py
```
Quyidagilarni toping va `your-username` ni `riva` bilan almashtiring:
```python
ALLOWED_HOSTS = [
    'hemis-sayiti.onrender.com',
    'riva.pythonanywhere.com',  # Bu qatorni qo'shing
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    '*',
]
```

### 5-Qadam: Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6-Qadam: Static files
```bash
mkdir -p ~/minihemis/static
python manage.py collectstatic --noinput
```

### 7-Qadam: Test
```bash
python manage.py collectstatic
# Xatoliksiz ishlashi kerak!
```

## MUVAFFAQIYAT TESTI
- [ ] Login ishlaydi
- [ ] Chat ishlaydi  
- [ ] Static files yuklanadi
- [ ] Admin panel ishlaydi
- [ ] Database ishlaydi

Agar barchasi ishlasa, tabriklayman! Saytingiz PythonAnywhere da ishlayapti!
