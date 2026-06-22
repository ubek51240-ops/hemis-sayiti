"""
Terminal orqali foydalanuvchini blokdan chiqarish.
Ishlatish: python manage.py unlock_user username
"""

from django.core.management.base import BaseCommand, CommandError
from axes.models import AccessAttempt
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Foydalanuvchini blokdan chiqarish'
    
    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Foydalanuvchi nomi')
    
    def handle(self, *args, **options):
        username = options['username']
        
        try:
            user = User.objects.get(username=username)
            
            # Super adminni tekshirish
            if hasattr(user, 'profile') and user.profile.role == 'super_admin':
                self.stdout.write(
                    self.style.WARNING(f'⚠️ {username} - Super admin hech qachon bloklanmaydi!')
                )
                return
            
            # AccessAttempt larni o'chirish
            deleted_count, _ = AccessAttempt.objects.filter(username=username).delete()
            
            if deleted_count > 0:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ {username} foydalanuvchi blokdan chiqarildi! ({deleted_count} ta urinish o\'chirildi)')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠️ {username} uchun hech qanday blok topilmadi!')
                )
            
        except User.DoesNotExist:
            raise CommandError(f'❌ {username} foydalanuvchi topilmadi!')
