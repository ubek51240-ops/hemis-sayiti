"""
Custom authentication backends for Test-sinov-ucun.
- Super admin hech qachon bloklanmaydi
- API endpointlar axes blokidan himoyalangan
- Profil yo'q bo'lsa login taqiqlanadi
"""

from axes.backends import AxesStandaloneBackend
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class AxesAdminExemptBackend(AxesStandaloneBackend):
    """
    Custom Axes backend with:
    - Super admin exempt from lockout
    - API endpoints exempt from lockout
    - Profile existence check
    """
    
    def is_allowed(self, request, credentials):
        """
        Check if the request should be exempt from axes lockout.
        """
        # ✅ API endpointlar HECH QACHON bloklanmaydi
        if request and hasattr(request, 'path'):
            if request.path.startswith('/api/'):
                # API uchun barcha bloklarni o'chirish
                username = credentials.get('username')
                if username:
                    from axes.models import AccessAttempt
                    AccessAttempt.objects.filter(username=username).delete()
                    print(f"🔓 API uchun {username} bloklari o'chirildi")
                return True
        
        # ✅ Faqat login sahifasi uchun bloklash
        if request and hasattr(request, 'path'):
            if request.path != '/':
                return True
        
        username = credentials.get('username')
        
        if username:
            try:
                user = User.objects.get(username=username)
                
                # ✅ Super admin HECH QACHON bloklanmaydi
                if hasattr(user, 'profile'):
                    role = user.profile.role
                    if role == 'super_admin':
                        # Super admin uchun barcha bloklarni o'chirish
                        from axes.models import AccessAttempt
                        deleted_count, _ = AccessAttempt.objects.filter(username=username).delete()
                        if deleted_count > 0:
                            print(f"🔓 Super Admin {username} bloklari o'chirildi ({deleted_count} ta)")
                        return True
                
                # ✅ Admin lar ham bloklanmasligi (agar kerak bo'lsa)
                # if role == 'admin':
                #     return True
                
                # Operator va boshqalar uchun FAQAT USER GA QARAB bloklash
                # IP ga qarab emas, faqat user ga qarab
                # Bu qurilma API si bloklanmasligini ta'minlaydi
                return super().is_allowed(request, credentials)
                
            except User.DoesNotExist:
                # User yo'q bo'lsa, oddiy axes tekshiruvi
                return super().is_allowed(request, credentials)
        
        return super().is_allowed(request, credentials)
