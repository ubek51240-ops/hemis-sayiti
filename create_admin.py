#!/usr/bin/env python
import os
import django
import getpass

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mini_hemis.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Profile

# Superuser yaratish
if not User.objects.filter(username='admin').exists():
    print("--- Yangi Super-admin Yaratish ---")
    password = os.environ.get('SUPERADMIN_PASSWORD')
    while not password:
        password = getpass.getpass("Super-admin uchun kuchli parol kiriting (min 8 ta belgi): ")
        if len(password) < 8:
            print("Xato: Parol kamida 8 ta belgidan iborat bo'lishi kerak!")
            password = None
            
    user = User.objects.create_superuser('admin', 'admin@example.com', password)
    profile, created = Profile.objects.update_or_create(user=user, defaults={'role': 'super_admin'})
    print('Superuser "admin" muvaffaqiyatli yaratildi!')
else:
    print('Admin user allaqachon mavjud')

# Test user yaratish
if not User.objects.filter(username='operator').exists():
    print("\n--- Yangi Operator Yaratish ---")
    password = os.environ.get('OPERATOR_PASSWORD')
    while not password:
        password = getpass.getpass("Operator uchun kuchli parol kiriting (min 8 ta belgi): ")
        if len(password) < 8:
            print("Xato: Parol kamida 8 ta belgidan iborat bo'lishi kerak!")
            password = None
            
    user = User.objects.create_user('operator', 'operator@example.com', password)
    profile, created = Profile.objects.update_or_create(user=user, defaults={'role': 'operator'})
    print('Operator "operator" muvaffaqiyatli yaratildi!')
else:
    print('Operator user allaqachon mavjud')

print('\nBarcha foydalanuvchilar:')
for user in User.objects.all():
    try:
        profile = user.profile
        print(f'  {user.username} - {profile.role}')
    except Profile.DoesNotExist:
        print(f'  {user.username} - Profile yo\'q')
