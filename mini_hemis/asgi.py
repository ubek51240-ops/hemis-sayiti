import os
from django.core.asgi import get_asgi_application

# Sozlamalar moduli birinchi bo'lib yuklanishi shart!
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mini_hemis.settings')
django_asgi_app = get_asgi_application()

# Qolgan routing va channels importlari faqat get_asgi_application() dan keyin kelishi kerak
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from core.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
