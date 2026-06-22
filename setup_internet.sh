#!/bin/bash

echo "=== Mini Hemis Internet Setup Script ==="
echo ""

# Step 1: Check if Django is running
echo "1. Django server tekshirilmoqda..."
if pgrep -f "manage.py runserver" > /dev/null; then
    echo "   Django server ishlayapti!"
else
    echo "   Django server ishlamayapti. Iltimos, avval uni ishga tushiring:"
    echo "   venv/bin/python manage.py runserver 0.0.0.0:8000"
    exit 1
fi

# Step 2: Download ngrok if not exists
echo ""
echo "2. Ngrok tekshirilmoqda..."
if [ ! -f "./ngrok" ]; then
    echo "   Ngrok yuklab olinmoqda..."
    wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz -q --show-progress
    tar xf ngrok-v3-stable-linux-amd64.tgz
    rm ngrok-v3-stable-linux-amd64.tgz
    chmod +x ngrok
    echo "   Ngrok muvaffaqiyatli yuklandi!"
else
    echo "   Ngrok allaqachon yuklangan!"
fi

# Step 3: Check if ngrok auth token is set
echo ""
echo "3. Ngrok authtoken tekshirilmoqda..."
if ! ./ngrok config check > /dev/null 2>&1; then
    echo "   Authtoken topilmadi. Iltimos, quyidagi qadamlarni bajaring:"
    echo "   1. https://ngrok.com ga kirib ro'yxatdan o'ting"
    echo "   2. Dashboarddan authtoken oling"
    echo "   3. Quyidagi komandani bajaring:"
    echo "      ./ngrok authtoken YOUR_TOKEN_HERE"
    echo "   4. Keyin bu scriptni qayta ishga tushiring"
    exit 1
else
    echo "   Authtoken topildi!"
fi

# Step 4: Start ngrok
echo ""
echo "4. Ngrok tunnel ochilmoqda..."
echo "   Django server: http://0.0.0.0:8000"
echo "   Ngrok tunnel: https://xxxxx.ngrok.io"
echo ""
echo "   Ngrok ishga tushirilmoqda..."
echo "   URL ni nusxalab istalgan browserda oching!"
echo ""
echo "   To'xtatish uchun: CTRL+C"
echo ""

./ngrok http 8000
