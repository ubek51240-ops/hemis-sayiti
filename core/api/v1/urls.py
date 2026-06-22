from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'students', views.StudentViewSet, basename='student')
router.register(r'faculties', views.FacultyViewSet, basename='faculty')
router.register(r'specialties', views.SpecialtyViewSet, basename='specialty')

urlpatterns = [
    # Auth
    path('auth/login/', views.login_view, name='api-login'),
    path('auth/logout/', views.logout_view, name='api-logout'),
    path('auth/me/', views.user_profile, name='api-me'),
    
    # Stats
    path('stats/', views.stats_view, name='api-stats'),
    
    # Notifications
    path('notifications/', views.notifications_list, name='api-notifications'),
    path('notifications/stream/', views.notification_stream, name='api-notification-stream'),
    path('send-notification/', views.send_notification_view, name='api-send-notification'),
    
    # Router
    path('', include(router.urls)),
]
