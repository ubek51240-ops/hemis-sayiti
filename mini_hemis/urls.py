"""
URL configuration for mini_hemis project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from core.admin import unlock_user_view
from django.http import HttpResponse, FileResponse
import os

# Custom 404 handler
def custom_404(request, exception=None):
    from django.shortcuts import render
    from django.conf import settings
    # Force render custom 404 even in DEBUG mode
    response = render(request, '404.html', status=404)
    response['X-Content-Type-Options'] = 'nosniff'
    return response

# Favicon view
def favicon_view(request):
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" fill="#2c3e50"/><text x="50" y="75" font-size="60" text-anchor="middle" fill="white" font-weight="bold">H</text></svg>'
    return HttpResponse(svg, content_type='image/svg+xml')

# Service worker - root scope (talab qilinadi PWA uchun)
def sw_view(request):
    sw_path = os.path.join(settings.BASE_DIR, 'static', 'js', 'service-worker.js')
    response = FileResponse(open(sw_path, 'rb'), content_type='application/javascript')
    response['Service-Worker-Allowed'] = '/'
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

# Manifest - root scope
def manifest_view(request):
    manifest_path = os.path.join(settings.BASE_DIR, 'static', 'manifest.json')
    return FileResponse(open(manifest_path, 'rb'), content_type='application/manifest+json')

urlpatterns = [
    path('favicon.ico', favicon_view, name='favicon'),
    path('sw.js', sw_view, name='service_worker'),
    path('manifest.json', manifest_view, name='manifest'),
    path('secure-control-center-2026/unlock-user/', unlock_user_view, name='admin_unlock_user'),
    path('secure-control-center-2026/', admin.site.urls),
    path('api/v1/', include('core.api.v1.urls')),
    path('', include('core.urls')),
]

# Custom 404 handler
handler404 = custom_404

# Static files serving during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Serve from STATICFILES_DIRS (static/) not STATIC_ROOT (staticfiles/)
    for static_dir in settings.STATICFILES_DIRS:
        urlpatterns += static(settings.STATIC_URL, document_root=str(static_dir))
