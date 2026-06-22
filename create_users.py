#!/usr/bin/env python
import os
import sys
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mini_hemis.settings')
import django
django.setup()

from django.contrib.auth.models import User
from core.models import Profile

def create_users():
    # Admin yaratish
    if not User.objects.filter(username='admin').exists():
        user = User.objects.create_user('admin', 'admin@example.com', 'admin123')
        user.is_staff = True
        user.is_superuser = True
        user.save()
        Profile.objects.create(user=user, role='super_admin')
        print('Admin yaratildi: admin / admin123')
    else:
        print('Admin allaqachon mavjud')

    # Operator yaratish  
    if not User.objects.filter(username='operator').exists():
        user = User.objects.create_user('operator', 'operator@example.com', 'operator123')
        Profile.objects.create(user=user, role='operator')
        print('Operator yaratildi: operator / operator123')
    else:
        print('Operator allaqachon mavjud')

    # Foydalanuvchilarni ko'rish
    print('Joriy foydalanuvchilar:')
    for user in User.objects.all():
        try:
            profile = user.profile
            print(f'  {user.username} - {profile.role} - Active: {user.is_active}')
        except Profile.DoesNotExist:
            print(f'  {user.username} - Profile yo\'q')

if __name__ == '__main__':
    create_users()
