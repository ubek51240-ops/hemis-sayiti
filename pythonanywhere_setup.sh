#!/bin/bash

echo "=== PythonAnywhere Complete Setup Script ==="
echo ""

# User input
read -p "PythonAnywhere usernameingizni kiriting: " username

echo "1. Eski repository o'chirilmoqda..."
cd ~
rm -rf hemis-sayiti 2>/dev/null || true

echo "2. Yangi repository clone qilinmoqda..."
git clone https://github.com/ubek51240-ops/hemis-sayiti.git
cd hemis-sayiti

echo "3. Virtual environment yaratilmoqda..."
python -m venv hemis-env
source hemis-env/bin/activate

echo "4. Packages install qilinmoqda..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "Requirements.txt topilmadi, asosiy packages o'rnatilmoqda..."
    pip install django djangorestframework whitenoise mysqlclient django-axes django-cors-headers pillow openpyxl gunicorn
fi

echo "5. Settings.py yangilanmoqda..."
if [ -f "mini_hemis/settings.py" ]; then
    sed -i "s/your-username/$username/g" mini_hemis/settings.py
else
    echo "Settings.py topilmadi!"
fi

echo "6. Static files directory yaratilmoqda..."
mkdir -p /home/$username/minihemis/static 2>/dev/null || mkdir -p ~/minihemis/static

echo "7. Migrations bajarilmoqda..."
if [ -f "manage.py" ]; then
    python manage.py makemigrations
    python manage.py migrate
else
    echo "Manage.py topilmadi!"
fi

echo "8. Static files collect qilinmoqda..."
if [ -f "manage.py" ]; then
    python manage.py collectstatic --noinput
else
    echo "Static files collect uchun manage.py topilmadi!"
fi

echo ""
echo "=== SETUP COMPLETE ==="
echo "Endi quyidagilarni qiling:"
echo "1. PythonAnywhere Web section ga kiring"
echo "2. Web app yarating (Manual configuration, Python 3.11)"
echo "3. Source code: /home/$username/hemis-sayiti"
echo "4. Working directory: /home/$username/hemis-sayiti"
echo "5. Environment variables qo'shing:"
echo "   - SECRET_KEY=django-insecure-your-secret-key"
echo "   - DB_PASSWORD=your-db-password"
echo "   - DB_NAME=$username\$mini_hemis"
echo "   - DB_USER=$username"
echo "   - DB_HOST=$username.mysql.pythonanywhere-services.com"
echo "   - PYTHONANYWHERE=1"
echo "   - DEBUG=False"
echo ""
echo "6. WSGI file ni yangilang va reload qiling!"
echo "7. https://$username.pythonanywhere.com ga kiring"
