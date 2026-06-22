from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # WebSocket for live chat - supports optional trailing slash
    re_path(r'^ws/live/(?P<room_name>[a-zA-Z0-9_-]+)/?$', consumers.LiveChatConsumer.as_asgi()),
    # WebSocket for global notifications
    re_path(r'^ws/notifications/?$', consumers.NotificationConsumer.as_asgi()),
]
