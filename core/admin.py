from django.contrib import admin
from .models import Profile, Faculty, Specialty, Student, AuditLog, ExcelDownloadRequest, Notification, Announcement, ChatMessage, StudentPayment, SiteLogo, LoginPageContent, ExcelImportConfig
from .admin_forms import CustomUserCreationForm
from axes.models import AccessAttempt, AccessLog, AccessFailureLog
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse, path
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render
from django.contrib import messages


# --- Custom User Admin (simplified add form) ---
class CustomUserAdmin(BaseUserAdmin):
    """Foydalanuvchi yaratish formasini soddalashtirilgan ko'rinishda"""
    change_form_template = 'admin/auth/user/change_form.html'
    add_form_template = 'admin/auth/user/change_form.html'
    add_form = CustomUserCreationForm

    def get_fieldsets(self, request, obj=None):
        """Faqat kerakli maydonlarni ko'rsatish"""
        if obj is None:
            # Yangi foydalanuvchi yaratish
            return [
                (None, {
                    'classes': ('wide',),
                    'fields': ('username', 'password1', 'password2'),
                }),
            ]
        return super().get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """Formani olish - edit va add uchun"""
        form = super().get_form(request, obj, **kwargs)
        
        # Form maydonlarining label'larini Uzbekchaga o'tkazish
        if obj is None:  # Add form
            if hasattr(form, 'fields'):
                if 'username' in form.fields:
                    form.fields['username'].label = "Foydalanuvchi nomi"
                if 'password1' in form.fields:
                    form.fields['password1'].label = "Parol"
                if 'password2' in form.fields:
                    form.fields['password2'].label = "Parolni tasdiqlang"
        
        return form


# Default UserAdmin ni o'chirish va custom ni o'rnatish
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User, CustomUserAdmin)


# --- Profile Admin ---
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'assigned_admin']
    list_filter = ['role']
    search_fields = ['user__username']
    exclude = ['organizational_role']


# --- Faculty Admin ---
@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


# --- Specialty Admin ---
@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ['name', 'faculty']
    list_filter = ['faculty']
    search_fields = ['name']


# --- Student Admin ---
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'passport', 'course', 'faculty', 'status', 'created_by', 'created_at']
    list_filter = ['status', 'course', 'faculty', 'created_at']
    search_fields = ['full_name', 'passport', 'jshshir']
    readonly_fields = ['created_at', 'updated_at', 'approved_at']


# --- AuditLog Admin ---
@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'timestamp']
    list_filter = ['timestamp', 'user']
    readonly_fields = ['timestamp']


# --- ExcelDownloadRequest Admin ---
@admin.register(ExcelDownloadRequest)
class ExcelDownloadRequestAdmin(admin.ModelAdmin):
    list_display = ['requested_by', 'status', 'created_at', 'approved_at', 'download_count']
    list_filter = ['status', 'created_at']
    search_fields = ['requested_by__username', 'reason']
    readonly_fields = ['created_at', 'approved_at', 'download_count']


# --- Notification Admin ---
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'title', 'notification_type', 'is_read', 'created_at']
    list_filter = ['is_read', 'notification_type', 'created_at']
    search_fields = ['recipient__username', 'title']
    readonly_fields = ['created_at']


# --- Announcement Admin ---
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'target_group', 'is_active', 'is_important', 'created_by', 'created_at', 'expires_at']
    list_filter = ['is_active', 'is_important', 'target_group', 'created_at']
    search_fields = ['title', 'message']
    readonly_fields = ['created_at']


# --- ChatMessage Admin ---
@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'message', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['sender__username', 'recipient__username', 'message']
    readonly_fields = ['created_at']


# --- Student Payment Admin ---
@admin.register(SiteLogo)
class SiteLogoAdmin(admin.ModelAdmin):
    list_display = ['id', 'logo', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(LoginPageContent)
class LoginPageContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    readonly_fields = ['created_at', 'updated_at']

# @admin.register(StudentPayment)
# class StudentPaymentAdmin(admin.ModelAdmin):
#     list_display = ['student', 'amount', 'payment_type', 'payment_date', 'created_by', 'created_at']
#     list_filter = ['payment_type', 'payment_date', 'created_at']
#     search_fields = ['student__full_name', 'student__passport', 'description']
#     date_hierarchy = 'payment_date'
#     ordering = ['-payment_date', '-created_at']


# --- AXES Access Attempt Admin (Unlock funksiyasi bilan) ---
# Avval unregister qilish
try:
    admin.site.unregister(AccessAttempt)
except admin.sites.NotRegistered:
    pass

@admin.register(AccessAttempt)
class AccessAttemptAdmin(admin.ModelAdmin):
    list_display = ['username', 'ip_address', 'attempt_time', 'failures_since_start', 'unlock_action']
    list_filter = ['attempt_time', 'username']
    search_fields = ['username', 'ip_address']
    readonly_fields = ['username', 'ip_address', 'user_agent', 'http_accept', 'path_info', 'attempt_time', 'failures_since_start']
    ordering = ['-attempt_time']
    
    def unlock_action(self, obj):
        """Admin panel orqali blokdan chiqarish tugmasi"""
        if obj.username:
            return format_html(
                '<a class="button" href="/admin/unlock-user/?username={}" '
                'onclick="return confirm(\'{} foydalanuvchini blokdan chiqarmoqchimisiz?\')">🔓 Blokdan Chiqarish</a>',
                obj.username,
                obj.username,
            )
        return '-'
    
    unlock_action.short_description = 'Amal'
    unlock_action.allow_tags = True


# --- AXES Access Log Admin ---
try:
    admin.site.unregister(AccessLog)
except admin.sites.NotRegistered:
    pass

@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):
    list_display = ['username', 'ip_address', 'attempt_time', 'path_info']
    list_filter = ['attempt_time']
    search_fields = ['username', 'ip_address']
    readonly_fields = ['username', 'ip_address', 'user_agent', 'http_accept', 'path_info', 'attempt_time']
    ordering = ['-attempt_time']


# --- AXES Access Failure Log Admin ---
try:
    admin.site.unregister(AccessFailureLog)
except admin.sites.NotRegistered:
    pass

@admin.register(AccessFailureLog)
class AccessFailureLogAdmin(admin.ModelAdmin):
    list_display = ['username', 'ip_address', 'attempt_time', 'path_info']
    list_filter = ['attempt_time']
    search_fields = ['username', 'ip_address']
    readonly_fields = ['username', 'ip_address', 'user_agent', 'http_accept', 'path_info', 'attempt_time']
    ordering = ['-attempt_time']


# --- Unlock User View ---
@staff_member_required
def unlock_user_view(request):
    """Foydalanuvchini blokdan chiqarish"""
    username = request.GET.get('username')
    
    if username:
        try:
            # AccessAttempt larni o'chirish
            deleted_count, _ = AccessAttempt.objects.filter(username=username).delete()
            
            messages.success(request, f"✅ {username} foydalanuvchi blokdan chiqarildi! ({deleted_count} ta urinish o'chirildi)")
            
            # Audit log
            AuditLog.objects.create(
                user=request.user,
                action=f"Foydalanuvchi blokdan chiqarildi",
                details=f"{username} admin tomonidan blokdan chiqarildi"
            )
            
        except Exception as e:
            messages.error(request, f"❌ Xatolik: {str(e)}")
    else:
        messages.error(request, "❌ Username topilmadi!")
    
    return redirect('/admin/axes/accessattempt/')


@admin.register(ExcelImportConfig)
class ExcelImportConfigAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name_col', 'passport_col', 'jshshir_col', 'course_col', 'phone_col', 'faculty_col', 'specialty_col', 'operator_comment_col', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']

    