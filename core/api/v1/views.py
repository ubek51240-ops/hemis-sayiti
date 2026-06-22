from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
import json
import time
from core.models import Profile, Student, Faculty, Specialty, Notification
from .serializers import (
    UserSerializer, ProfileSerializer, LoginSerializer,
    StudentListSerializer, StudentDetailSerializer,
    FacultySerializer, SpecialtySerializer
)

# --- Auth Views ---
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """Login va token qaytarish"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data,
            'message': 'Muvaffaqiyatli kirildi'
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """Logout - tokenni o'chirish"""
    try:
        request.user.auth_token.delete()
    except (AttributeError, Token.DoesNotExist):
        pass
    return Response({'message': 'Muvaffaqiyatli chiqildi'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_profile(request):
    """Hozirgi foydalanuvchi profilini olish"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

# --- User ViewSet ---
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Foydalanuvchilar ro'yxati (faqat admin/super_admin)"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        # IDOR himoyasi: oddiy foydalanuvchilar faqat o'z profilini ko'radi
        if user.profile.role == 'super_admin':
            return User.objects.all()
        elif user.profile.role == 'admin':
            operator_ids = user.subordinate_operators.values_list('user_id', flat=True)
            return User.objects.filter(id__in=list(operator_ids) + [user.id])
        # Operator va boshqa rollar faqat o'zini ko'radi
        return User.objects.filter(id=user.id)
    
    def get_permissions(self):
        # List faqat admin/super_admin uchun
        if self.action == 'list':
            return [permissions.IsAuthenticated()]
        # Retrieve uchun qo'shimcha tekshiruv
        return [permissions.IsAuthenticated()]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        
        # IDOR tekshiruvi: oddiy foydalanuvchi boshqa foydalanuvchini ko'ra olmaydi
        if user.profile.role not in ['super_admin', 'admin'] and instance.id != user.id:
            return Response(
                {'error': 'Boshqa foydalanuvchi ma\'lumotlarini ko\'rish huquqi yo\'q'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

# --- Student ViewSet ---
class StudentViewSet(viewsets.ModelViewSet):
    """Talabalar API"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return StudentListSerializer if self.action == 'list' else StudentDetailSerializer
        return StudentDetailSerializer
    
    def get_queryset(self):
        user = self.request.user
        # IDOR himoyasi: faqat ruxsat etilgan talabalarni ko'rsatish
        if user.profile.role == 'super_admin':
            queryset = Student.objects.all()
        elif user.profile.role == 'admin':
            operator_ids = list(user.subordinate_operators.values_list('user_id', flat=True))
            queryset = Student.objects.filter(
                Q(created_by__in=operator_ids) | Q(created_by__isnull=True)
            )
        elif user.profile.role == 'operator':
            queryset = Student.objects.filter(created_by=user)
        elif user.profile.role == 'hemis_id_adder':
            queryset = Student.objects.filter(status='approved')
        elif user.profile.role == 'talaba_viewer':
            queryset = Student.objects.filter(status__in=['approved', 'rejected'])
        else:
            # Student, employee, applicant - hech qanday talabani ko'ra olmaydi
            return Student.objects.none()
        
        # Qidiruv
        query = self.request.query_params.get('q')
        if query:
            queryset = queryset.filter(
                Q(full_name__icontains=query) |
                Q(passport__icontains=query) |
                Q(jshshir__icontains=query)
            )
        
        # Status filtri
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.select_related('faculty', 'specialty', 'created_by', 'approved_by').order_by('-created_at')
    
    def perform_create(self, serializer):
        user = self.request.user
        # Faqat operator va super_admin qo'sha oladi
        if user.profile.role not in ['operator', 'super_admin']:
            raise permissions.PermissionDenied("Siz talaba qo'sha olmaysiz")
        serializer.save(created_by=user)
    
    def perform_update(self, serializer):
        user = self.request.user
        instance = self.get_object()
        # IDOR tekshiruvi: operator faqat o'z talabasini tahrirlay oladi
        if user.profile.role == 'operator' and instance.created_by != user:
            raise permissions.PermissionDenied("Siz faqat o'zingiz qo'shgan talabani tahrirlay olasiz")
        serializer.save()
    
    def perform_destroy(self, instance):
        user = self.request.user
        # IDOR tekshiruvi: operator faqat o'z talabasini o'chira oladi
        if user.profile.role == 'operator' and instance.created_by != user:
            raise permissions.PermissionDenied("Siz faqat o'zingiz qo'shgan talabani o'chira olasiz")
        instance.delete()

# --- Faculty ViewSet ---
class FacultyViewSet(viewsets.ReadOnlyModelViewSet):
    """Fakultetlar API"""
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [permissions.IsAuthenticated]

# --- Specialty ViewSet ---
class SpecialtyViewSet(viewsets.ReadOnlyModelViewSet):
    """Mutaxassisliklar API"""
    serializer_class = SpecialtySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Specialty.objects.all()
        faculty_id = self.request.query_params.get('faculty_id')
        if faculty_id:
            queryset = queryset.filter(faculty_id=faculty_id)
        return queryset

# --- Stats View ---
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def stats_view(request):
    """Statistika ma'lumotlari"""
    user = request.user
    students = Student.objects.all()
    
    if user.profile.role == 'operator':
        students = students.filter(created_by=user)
    elif user.profile.role == 'admin':
        operator_ids = user.subordinate_operators.values_list('user_id', flat=True)
        students = students.filter(created_by__in=operator_ids)
    
    return Response({
        'total': students.count(),
        'pending': students.filter(status='pending').count(),
        'approved': students.filter(status='approved').count(),
        'rejected': students.filter(status='rejected').count(),
    })

# --- Notifications Views ---
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def notifications_list(request):
    """Xabarlar ro'yxati"""
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    
    # Faqat o'qilmaganlar
    unread_only = request.query_params.get('unread_only', 'false').lower() == 'true'
    if unread_only:
        notifications = notifications.filter(is_read=False)
    
    data = []
    for notification in notifications:
        data.append({
            'id': notification.id,
            'title': notification.title,
            'message': notification.message,
            'type': notification.notification_type,
            'sender': notification.sender.username if notification.sender else 'System',
            'created_at': notification.created_at.isoformat(),
            'is_read': notification.is_read,
            'url': notification.get_absolute_url() if hasattr(notification, 'get_absolute_url') else None
        })
    
    return Response({'results': data})

@csrf_exempt
@require_GET
def notification_stream(request):
    """Server-Sent Events orqali real-time xabarlar"""
    # Xavfsizlik: faqat autentifikatsiya qilingan foydalanuvchilar
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    user_id = request.GET.get('user_id')
    
    if not user_id:
        return JsonResponse({'error': 'User ID required'}, status=400)
    
    # IDOR himoyasi: faqat o'z xabarlarini ko'ra oladi
    if str(request.user.id) != str(user_id):
        return JsonResponse({'error': 'Faqat o\'z xabarlaringizni ko\'rishingiz mumkin'}, status=403)
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    
    def event_stream():
        last_notification_id = 0
        
        while True:
            # Yangi xatlarni tekshirish
            notifications = Notification.objects.filter(
                recipient=user,
                id__gt=last_notification_id
            ).order_by('created_at')
            
            for notification in notifications:
                data = {
                    'id': notification.id,
                    'title': notification.title,
                    'message': notification.message,
                    'type': notification.notification_type,
                    'sender': notification.sender.username if notification.sender else 'System',
                    'created_at': notification.created_at.isoformat(),
                    'is_read': notification.is_read
                }
                
                yield f"data: {json.dumps(data)}\n\n"
                last_notification_id = notification.id
            
            # 5 soniya kutish
            time.sleep(5)
    
    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['Connection'] = 'keep-alive'
    # Xavfsiz CORS headerlari
    response['Access-Control-Allow-Origin'] = request.META.get('HTTP_ORIGIN', '')
    response['Access-Control-Allow-Headers'] = 'Cache-Control'
    
    return response

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_notification_view(request):
    """Xabar yuborish"""
    try:
        user_id = request.data.get('user_id')
        notification_data = request.data.get('notification')
        
        if not user_id or not notification_data:
            return Response({'error': 'user_id va notification kerak'}, status=400)
        
        # Qabul qiluvchini topish
        try:
            recipient = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'Foydalanuvchi topilmadi'}, status=404)
        
        # Xabarni yaratish
        notification = Notification.objects.create(
            recipient=recipient,
            sender=request.user,
            title=notification_data.get('title', 'Yangi xabar'),
            message=notification_data.get('message', ''),
            notification_type=notification_data.get('type', 'info')
        )
        
        return Response({
            'message': 'Xabar muvaffaqiyatli yuborildi',
            'notification_id': notification.id
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=500)
