"""
URL configuration for core app (web views).
"""

from django.urls import path, include
from core import views

urlpatterns = [
    # Landing page (bosh sahifa)
    path('', views.landing_page, name='landing'),
    path('offline/', views.offline_page, name='offline'),
    path('offline-queue/', views.offline_queue_page, name='offline_queue'),
    path('landing-settings/', views.landing_settings, name='landing_settings'),
    
    # Faculty and Specialty detail pages (public)
    path('faculty/<int:faculty_id>/', views.faculty_detail, name='faculty_detail'),
    path('specialty/<int:specialty_id>/', views.specialty_detail, name='specialty_detail'),
    
    # All faculties and specialties listing pages
    path('faculties/', views.all_faculties, name='all_faculties'),
    path('specialties/', views.all_specialties, name='all_specialties'),
    path('landing-settings/news/add/', views.landing_news_add, name='landing_news_add'),
    path('landing-settings/news/<int:pk>/edit/', views.landing_news_edit, name='landing_news_edit'),
    path('landing-settings/news/<int:pk>/delete/', views.landing_news_delete, name='landing_news_delete'),
    # Authentication
    path('login/', views.login_view, name='login'),
    path('register/', views.register_student_view, name='register'),  # Default - Talaba uchun
    path('register/student/', views.register_student_view, name='register_student'),
    path('register/employee/', views.register_employee_view, name='register_employee'),
    path('logout/', views.logout_view, name='logout'),
    path('submit-application/', views.submit_application, name='submit_application'),
    path('my-application/', views.my_application, name='my_application'),
    path('applications/', views.applications_list, name='applications_list'),
    path('all-applicants/', views.all_applicants_list, name='all_applicants_list'),
    path('bulk-action/', views.bulk_student_action, name='bulk_student_action'),
    path('add-comment/', views.add_comment, name='add_comment'),
    path('application/<int:pk>/process/', views.process_application, name='process_application'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('notifications/', views.notifications_view, name='notifications'),
    
    # Student management
    path('add-student/', views.add_student, name='add_student'),
    path('upload-students-excel/', views.upload_students_excel, name='upload_students_excel'),
    path('edit-student/<int:pk>/', views.edit_student, name='edit_student'),
    path('process/<int:pk>/', views.process_student, name='process_student'),
    path('delete/<int:pk>/', views.delete_student, name='delete_student'),
    path('hemis-id-list/', views.hemis_id_list, name='hemis_id_list'),
    path('update-hemis-id/<int:pk>/', views.update_hemis_id, name='update_hemis_id'),
    
    # Faculty and Specialty Excel uploads
    path('upload-faculty-excel/', views.upload_faculty_excel, name='upload_faculty_excel'),
    path('download-faculty-sample-excel/', views.download_faculty_sample_excel, name='download_faculty_sample_excel'),
    path('upload-specialty-excel/', views.upload_specialty_excel, name='upload_specialty_excel'),
    path('download-specialty-sample-excel/', views.download_specialty_sample_excel, name='download_specialty_sample_excel'),
    
    # Excel operations
    path('export-excel/', views.export_excel, name='export_excel'),
    path('download-sample-excel/', views.download_sample_excel, name='download_sample_excel'),
    path('download-yoriqnoma-excel/', views.download_yoriqnoma_excel, name='download_yoriqnoma_excel'),
    path('download-failed-students-excel/', views.download_failed_students_excel, name='download_failed_students_excel'),
    path('request-excel/', views.request_excel, name='request_excel'),
    path('excel-requests/', views.excel_requests_list, name='excel_requests_list'),
    path('excel-request/<int:pk>/process/', views.process_excel_request, name='process_excel_request'),
    
    # Profile
    path('profile/', views.profile_settings, name='profile_settings'),
    
    # Faculty & Specialty management
    path('manage-faculties/', views.manage_faculties, name='manage_faculties'),
    path('edit-faculty/<int:pk>/', views.edit_faculty, name='edit_faculty'),
    path('delete-faculty/<int:pk>/', views.delete_faculty, name='delete_faculty'),
    path('edit-specialty/<int:pk>/', views.edit_specialty, name='edit_specialty'),
    path('delete-specialty/<int:pk>/', views.delete_specialty, name='delete_specialty'),
    path('update-specialty-contract/<int:pk>/', views.update_specialty_contract, name='update_specialty_contract'),
    
    # Statistics & Reports
    path('operator-statistics/', views.operator_statistics, name='operator_statistics'),
    path('export-operator-statistics/', views.export_operator_statistics_excel, name='export_operator_statistics'),
    path('export-all-students/', views.export_all_students_excel, name='export_all_students'),
    path('operator-ranking/', views.operator_ranking, name='operator_ranking'),
    
    # Announcements
    path('announcements/', views.announcements_list, name='announcements_list'),
    path('announcement/create/', views.create_announcement, name='create_announcement'),
    path('announcement/<int:pk>/delete/', views.delete_announcement, name='delete_announcement'),
    
    # Chat
    path('chat/', views.chat_list, name='chat_list'),
    path('chat/<int:user_id>/', views.chat_conversation, name='chat_conversation'),
    path('chat/message/<int:pk>/delete/', views.delete_chat_message, name='delete_chat_message'),
    path('chat/message/<int:pk>/edit/', views.edit_chat_message, name='edit_chat_message'),
    path('chat/reaction/<int:message_id>/', views.add_reaction, name='add_reaction'),
    path('chat/reaction/<int:message_id>/remove/', views.remove_reaction, name='remove_reaction'),
    path('chat/message/<int:message_id>/reactions/', views.get_message_reactions, name='get_message_reactions'),
    
    # Audit logs
    path('audit-logs/', views.audit_logs_view, name='audit_logs'),
    
    # Bloklangan foydalanuvchilar
    path('blocked-users/', views.blocked_users_view, name='blocked_users'),
    path('unlock-user/<str:username>/', views.unlock_user_direct, name='unlock_user_direct'),
    
    # Super admin blokdan chiqarish
    path('unblock-my-profile/', views.unblock_super_admin_profile, name='unblock_super_admin_profile'),
    path('clear-all-super-admin-blocks/', views.clear_all_super_admin_blocks, name='clear_all_super_admin_blocks'),
    
    # Barcha bloklarni o'chirish
    path('clear-all-blocks/', views.clear_all_blocks, name='clear_all_blocks'),
    
    # Parolni tiklash
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('verify-reset-code/<str:username>/', views.verify_reset_code_view, name='verify_reset_code'),
    path('reset-password/<str:username>/', views.reset_password_view, name='reset_password'),
    
    # Email sozlamalari (Super Admin)
    path('email-settings/', views.email_settings_view, name='email_settings'),
    path('email-settings/<int:settings_id>/edit/', views.edit_email_settings, name='edit_email'),
    path('email-settings/<int:settings_id>/delete/', views.delete_email_settings, name='delete_email'),
    path('test-email/<int:settings_id>/', views.test_email_settings, name='test_email'),
    path('toggle-email/<int:settings_id>/', views.toggle_email_settings, name='toggle_email'),
    
    # Excel import sozlamalari (Super Admin)
    path('excel-import-settings/', views.excel_import_settings_view, name='excel_import_settings'),
    
    # User management (Super Admin)
    path('manage-users/', views.manage_users, name='manage_users'),
    path('create-user/', views.create_user, name='create_user'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    
    # Logo management
    path('logo-management/', views.logo_management, name='logo_management'),
    path('logo/login-page-settings/', views.login_page_settings, name='login_page_settings'),
    path('logo/toggle/<int:pk>/', views.toggle_logo, name='toggle_logo'),
    path('logo/delete/<int:pk>/', views.delete_logo, name='delete_logo'),
    
    # Theme management
    path('save-theme/', views.save_theme, name='save_theme'),
    
    # Live stream
    path('live/<str:room_name>/', views.live_stream, name='live_stream'),

    # Role switching
    path('switch-role/<str:role>/', views.switch_role, name='switch_role'),

    # Accountant (BUxgalteriya)
    path('accountant/', views.accountant_dashboard, name='accountant_dashboard'),
    path('accountant/payment/<int:student_id>/', views.add_payment, name='add_payment'),
    path('accountant/view-payments/<int:student_id>/', views.view_payments, name='view_payments'),

    # AJAX endpoints
    path('get-specialties/', views.get_specialties, name='get_specialties'),
    
    # ❌ BU QATORLARNI O'CHIRING (email kerak emas):
    # path('password-reset/', views.password_reset_request, name='password_reset_request'),
    # path('password-reset/sent/', views.password_reset_sent, name='password_reset_sent'),
    # path('password-reset/confirm/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
]

# API v1 yo'nalishlari (complete_urls.py orqali ham qo'shiladi)
# Bu yerda qo'shilmasa ham bo'ladi, chunki complete_urls.py da qo'shilgan
