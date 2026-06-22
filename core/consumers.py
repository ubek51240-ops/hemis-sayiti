import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import ChatMessage, Notification

class NotificationConsumer(AsyncWebsocketConsumer):
    """Global bildirishnomalar uchun WebSocket consumer"""
    
    async def connect(self):
        # Barcha foydalanuvchilar umumiy guruhga ulanadi
        await self.channel_layer.group_add("global_notifications", self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("global_notifications", self.channel_name)
    
    async def send_notification(self, event):
        """Global bildirishnomani barcha ulangan foydalanuvchilarga yuborish"""
        await self.send(text_data=json.dumps(event["data"]))


class LiveChatConsumer(AsyncWebsocketConsumer):
    """Jonli chat WebSocket consumer - guruhli xonalar uchun"""
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'live_chat_{self.room_name}'
        
        # Foydalanuvchi autentifikatsiyasini tekshirish
        self.user = self.scope.get('user')
        if self.user and self.user.is_authenticated:
            self.username = self.user.username
        else:
            self.username = 'Anonim'
        
        # Guruhga qo'shilish
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Onlayn foydalanuvchilar ro'yxatini yangilash
        await self._update_user_list()
        
        # Xonaga qo'shilganligi haqida xabar
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': f'{self.username} xonaga qo\'shildi',
                'username': 'System',
                'message_type': 'system',
                'timestamp': self._get_timestamp(),
            }
        )
    
    async def disconnect(self, close_code):
        # Admin (streamer) yoki oddiy viewer ekanligini aniqlash
        is_admin = False
        if self.user and self.user.is_authenticated:
            session = self.scope.get('session', {})
            active_role = session.get('active_role', '')
            is_admin = self.user.is_superuser or active_role in ['admin', 'super_admin']
            
        if is_admin:
            # Streamer uzildi -> barchaga efir tugaganini bildiramiz
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'broadcast_signal',
                    'sender_channel_name': self.channel_name,
                    'data': {
                        'type': 'stream_ended'
                    }
                }
            )
        else:
            # Oddiy viewer chiqdi -> streamerga ulanishni yopishni bildiramiz
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'broadcast_signal',
                    'sender_channel_name': self.channel_name,
                    'data': {
                        'type': 'viewer_left'
                    }
                }
            )

        # Xonadan chiqish
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        # Onlayn foydalanuvchilar ro'yxatini yangilash
        await self._update_user_list()
        
        # Xonadan chiqish haqida xabar
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': f'{self.username} xonani tark etdi',
                'username': 'System',
                'message_type': 'system',
                'timestamp': self._get_timestamp(),
            }
        )
    
    async def receive(self, text_data):
        """Xabar qabul qilish va guruhga tarqatish"""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            # WebRTC signallarini tarqatish (Offer, Answer, Candidate va boshqalar)
            if message_type in ['offer', 'answer', 'candidate', 'viewer_joined', 'viewer_left', 'stream_started', 'stream_ended']:
                target = data.get('target')
                if target:
                    # Aniq bitta peerga yuborish
                    await self.channel_layer.send(
                        target,
                        {
                            'type': 'direct_signal',
                            'sender_channel_name': self.channel_name,
                            'data': data
                        }
                    )
                else:
                    # Barcha guruh a'zolariga yuborish
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'broadcast_signal',
                            'sender_channel_name': self.channel_name,
                            'data': data
                        }
                    )
            else:
                # Oddiy chat xabarlari uchun mavjud mantiq
                message = data.get('message', '').strip()
                msg_type = data.get('message_type', 'chat')
                
                if not message:
                    return
                
                # Xabarni bazaga saqlash (agar kerak bo'lsa)
                if msg_type == 'chat' and self.user and self.user.is_authenticated:
                    await self._save_message(message)
                
                # Xabarni guruhga yuborish
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'username': self.username,
                        'message_type': msg_type,
                        'timestamp': self._get_timestamp(),
                    }
                )
        except json.JSONDecodeError:
            pass
    
    async def broadcast_signal(self, event):
        """WebRTC signalini yuborgan odamning o'ziga qaytarib yubormaslik sharti bilan tarqatish"""
        if self.channel_name != event['sender_channel_name']:
            data = event['data']
            data['sender'] = event['sender_channel_name']
            await self.send(text_data=json.dumps(data))

    async def direct_signal(self, event):
        """WebRTC signalini faqat ma'lum bir foydalanuvchiga yuborish"""
        data = event['data']
        data['sender'] = event['sender_channel_name']
        await self.send(text_data=json.dumps(data))
    
    async def chat_message(self, event):
        """Xabarni WebSocket orqali yuborish"""
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'username': event['username'],
            'message_type': event.get('message_type', 'chat'),
            'timestamp': event.get('timestamp', self._get_timestamp()),
        }))
    
    async def user_list(self, event):
        """Onlayn foydalanuvchilar ro'yxatini yuborish"""
        await self.send(text_data=json.dumps({
            'type': 'user_list',
            'users': event['users']
        }))
    
    async def _update_user_list(self):
        """Guruhdagi barcha ulangan kanallarni so'rab, foydalanuvchilar ro'yxatini yuborish"""
        # channels_redis orqali guruh a'zolarini olish
        # Bu yerda soddalashtirilgan: faqat o'z nomini qo'shamiz
        # Aslida Redis orqali guruh a'zolarini olish mumkin
        # Lekin biz faqat o'z nomimizni yuboramiz (boshqa foydalanuvchilar ham xuddi shunday qiladi)
        # To'liq ro'yxat uchun Redis dan foydalanish kerak
        # Hozircha faqat o'z nomimizni yuboramiz
        users = [self.username]
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_list',
                'users': users
            }
        )
    
    def _get_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime('%H:%M:%S')
    
    @database_sync_to_async
    def _save_message(self, message):
        """Xabarni ChatMessage modeliga saqlash (ixtiyoriy)"""
        try:
            if self.user and self.user.is_authenticated:
                # Xabarni saqlash (agar kerak bo'lsa)
                pass
        except Exception:
            pass
