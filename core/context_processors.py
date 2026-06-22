from .models import Notification, ChatMessage

def active_role(request):
    """Foydalanuvchining faol rolini context ga qo'shish"""
    context = {
        'active_role': None,
        'unread_notifications': 0,
        'unread_chat_count': 0,
    }
    
    if request.user.is_authenticated:
        # Session dan active_role ni olish
        role = request.session.get('active_role', request.user.profile.role if hasattr(request.user, 'profile') else 'operator')
        context['active_role'] = role
        
        # O'qilmagan xabarlar soni
        context['unread_notifications'] = Notification.objects.filter(recipient=request.user, is_read=False).count()
        
        # O'qilmagan chat xabarlar soni
        context['unread_chat_count'] = ChatMessage.objects.filter(recipient=request.user, is_read=False).count()
    
    return context
