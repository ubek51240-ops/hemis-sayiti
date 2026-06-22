from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
from django.utils import timezone
from django.db.models import Q
import json


class Profile(models.Model):
    ROLE_CHOICES = (
        ('super_admin', 'Super Admin'),
        ('admin', 'Admin'),
        ('operator', 'Talaba Qo\'shuvchi'),
        ('hemis_id_adder', 'HEMIS ID Qo\'shuvchi'),
        # ('accountant', 'BUxgalter'), # Vaqtinchalik o'chirildi
        ('talaba_viewer', 'Talabani Ko\'ruvchi'),
        # ('archive', 'Arxiv'), # Vaqtinchalik o'chirildi
        ('student', 'Talaba (Ariza beruvchi)'),
        ('employee', 'Xodim (Ariza beruvchi)'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='operator')
    # Multiple roles support - JSONField for storing list of roles
    roles = models.JSONField(default=list, blank=True, help_text="Bir nechta rollar")
    # Tashkiliy rol/bo'lim
    ORGANIZATIONAL_ROLE_CHOICES = (
        ('2', 'Fuqaro'),
        ('14', "O'quv bo'limi"),
        ('16', 'Xodim'),
        ('26', 'Office registration'),
        ('34', 'Kitobxon'),
        ('39', 'Hemis monitoring'),
    )
    organizational_role = models.CharField(
        max_length=10,
        choices=ORGANIZATIONAL_ROLE_CHOICES,
        blank=True,
        null=True,
        verbose_name="Tashkiliy Rol"
    )
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon raqam")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    jshshir = models.CharField(max_length=14, blank=True, null=True, verbose_name="JSHSHIR", help_text="14 ta raqam")
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name="Profil rasmi",
        help_text="Maksimal 2MB, JPG/PNG"
    )
    assigned_admin = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='subordinate_operators',
        limit_choices_to={'profile__role': 'admin'}
    )

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    def has_role(self, role):
        """Foydalanuvchida ma'lum rol borligini tekshirish"""
        if role in ['accountant', 'archive']:
            return False
        if self.role == role:
            return True
        if isinstance(self.roles, list):
            return role in self.roles
        return False

    def has_any_role(self, roles):
        """Foydalanuvchida ro'yxatdagi rollardan biri borligini tekshirish"""
        if not isinstance(roles, (list, tuple)):
            roles = [roles]
        for role in roles:
            if self.has_role(role):
                return True
        return False

    def get_all_roles(self):
        """Foydalanuvchining barcha rollarini qaytarish"""
        all_roles = []
        if self.role and self.role not in ['accountant', 'archive']:
            all_roles.append(self.role)
        if isinstance(self.roles, list):
            for r in self.roles:
                if r not in all_roles and r not in ['accountant', 'archive']:
                    all_roles.append(r)
        return all_roles

    def get_roles_display(self):
        """Barcha rollar nomlarini qaytarish"""
        role_dict = dict(self.ROLE_CHOICES)
        all_roles = self.get_all_roles()
        return [role_dict.get(r, r) for r in all_roles]

    def save(self, *args, **kwargs):
        # Agar roles bo'sh bo'lsa, role ni ichiga qo'shamiz
        if not self.roles:
            self.roles = []
        if self.role and self.role not in self.roles:
            self.roles.insert(0, self.role)
        super().save(*args, **kwargs)


class Faculty(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Specialty(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    contract_amount = models.DecimalField(max_digits=12, decimal_places=0, default=0, help_text="Kontrakt summasi (so'm)")
    
    def __str__(self):
        return f"{self.faculty.name} - {self.name}"

class Student(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),
        ('approved', 'Qabul qilindi'),
        ('rejected', 'Rad etildi'),
    )
    
    passport = models.CharField(max_length=9, unique=True)
    jshshir = models.CharField(max_length=14, unique=True)
    hemis_id = models.CharField(max_length=20, unique=True, blank=True, null=True, help_text="HEMIS tizimidagi talaba ID raqami")
    full_name = models.CharField(max_length=100)
    course = models.IntegerField(choices=[(i, i) for i in range(1, 5)])
    phone = models.CharField(max_length=13)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)
    specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True)
    transcript = models.FileField(upload_to='documents/transcripts/', blank=True, null=True)
    passport_scan = models.FileField(upload_to='documents/passport_scans/', blank=True, null=True)
    additional_documents = models.FileField(upload_to='documents/other_documents/', blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    comment = models.TextField(blank=True, null=True, help_text="Faqat Admin/Super Admin yozishi mumkin")
    operator_comment = models.TextField(blank=True, null=True, help_text="Operator izohi")
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_students')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_students', help_text="Tasdiqlagan/Rad etgan admin")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def clean(self):
        if self.passport:
            self.passport = self.passport.strip().upper()
        
        if self.passport and not re.match(r'^[A-Z]{2}\d{7}$', self.passport):
            raise ValidationError({
                'passport': f'Pasport formati noto\'g\'ri. Masalan: AA1234567'
            })
        
        if self.jshshir and not re.match(r'^\d{14}$', self.jshshir):
            raise ValidationError({'jshshir': 'JSHSHIR 14 ta raqamdan iborat bo\'lishi kerak'})

        if self.course in [2, 3, 4]:
            if not self.transcript:
                raise ValidationError({
                    'transcript': '2-4 kurs transfer talabasi uchun transcript yuklanishi kerak.'
                })
            if not self.passport_scan:
                raise ValidationError({
                    'passport_scan': '2-4 kurs transfer talabasi uchun pasport rasmi yuklanishi kerak.'
                })

    def can_operator_edit(self):
        return self.status == 'pending'

    def __str__(self):
        return f"{self.full_name} ({self.passport})"

class Application(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),
        ('approved', 'Qabul qilindi'),
        ('rejected', 'Rad etildi'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    full_name = models.CharField(max_length=100)
    passport = models.CharField(max_length=9)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)
    specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    comment = models.TextField(blank=True, null=True)
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_applications'
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.full_name} - {self.get_status_display()}"

class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        username = self.user.username if self.user else "System"
        return f"{username} - {self.action}"

class Comment(models.Model):
    """Talaba yoki ariza uchun kommentlar"""
    COMMENT_TYPE_CHOICES = (
        ('student', 'Talaba'),
        ('application', 'Ariza'),
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment_type = models.CharField(max_length=20, choices=COMMENT_TYPE_CHOICES)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
    application = models.ForeignKey(Application, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_internal = models.BooleanField(default=False, help_text="Faqat adminlar ko'radi")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        target = self.student or self.application
        return f"{self.author.username} - {target}"

class ExcelDownloadRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),
        ('approved', 'Tasdiqlandi'),
        ('rejected', 'Rad etildi'),
    )
    
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='excel_requests')
    reason = models.TextField(help_text="Excel yuklash sababi")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_comment = models.TextField(blank=True, null=True, help_text="Admin izohi")
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_excel_requests')
    download_count = models.IntegerField(default=0, help_text="Necha marta yuklangan")
    notification_sent = models.BooleanField(default=False, help_text="Admin xabardor qilindimi")

    def __str__(self):
        return f"{self.requested_by.username} - {self.status} - {self.created_at}"

    def can_download(self):
        return self.status == 'approved'

class Notification(models.Model):
    """Ichki xabar tizimi"""
    NOTIFICATION_TYPES = (
        ('excel_request', 'Excel So\'rovi'),
        ('excel_approved', 'Excel Tasdiqlandi'),
        ('excel_rejected', 'Excel Rad Etildi'),
        ('student_approved', 'Talaba Tasdiqlandi'),
        ('student_rejected', 'Talaba Rad Etildi'),
        ('general', 'Umumiy'),
    )
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sent_notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='general')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    related_object_id = models.IntegerField(null=True, blank=True, help_text="Bog'liq obyekt ID")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.recipient.username} - {self.title}"

class PasswordResetCode(models.Model):
    """Parolni tiklash uchun 6 xonalik kod"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Parolni tiklash kodi"
        verbose_name_plural = "Parolni tiklash kodlari"
    
    def __str__(self):
        return f"{self.user.username} - {self.code}"
    
    def is_valid(self):
        """Kod yaroqliqligini tekshirish (15 daqiqa ichida)"""
        from django.utils import timezone
        from datetime import timedelta
        return not self.is_used and (timezone.now() - self.created_at) < timedelta(minutes=15)
    
    @classmethod
    def generate_code(cls, user):
        """Foydalanuvchi uchun yangi kod generatsiya qilish (6-8 xonali)"""
        import random
        import string
        
        # Eski kodlarni o'chirish
        cls.objects.filter(user=user, is_used=False).update(is_used=True)
        
        # 6 yoki 8 xonalik kod (tasodifiy)
        code_length = random.choice([6, 8])
        code = ''.join(random.choices(string.digits, k=code_length))
        return cls.objects.create(user=user, code=code)

class EmailSettings(models.Model):
    """Email sozlamalari - super admin uchun"""
    email = models.EmailField(verbose_name="Email manzili")
    password = models.CharField(max_length=255, verbose_name="Email paroli", blank=True, null=True)
    smtp_host = models.CharField(max_length=255, default="smtp.gmail.com", verbose_name="SMTP server")
    smtp_port = models.IntegerField(default=587, verbose_name="SMTP port")
    use_tls = models.BooleanField(default=True, verbose_name="TLS ishlatish")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Email sozlama"
        verbose_name_plural = "Email sozlamalari"
    
    def __str__(self):
        return f"{self.email} ({'Faol' if self.is_active else 'Faol emas'})"
    
    @classmethod
    def get_active_settings(cls):
        """Faol email sozlamalarini olish"""
        return cls.objects.filter(is_active=True).first()

    @classmethod
    def create_notification(cls, recipient, title, message, notification_type='general', sender=None, related_object_id=None):
        notification = cls.objects.create(
            recipient=recipient,
            sender=sender,
            title=title,
            message=message,
            notification_type=notification_type,
            related_object_id=related_object_id
        )
        return notification

class Announcement(models.Model):
    """E'lonlar tizimi"""
    TARGET_CHOICES = (
        ('all', 'Barcha foydalanuvchilar'),
        ('super_admin', 'Faqat Super Admin'),
        ('admin', 'Faqat Admin'),
        ('operator', 'Faqat Operator'),
        ('archive', 'Faqat Arxiv'),
    )
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    target_group = models.CharField(max_length=20, choices=TARGET_CHOICES, default='all')
    is_active = models.BooleanField(default=True)
    is_important = models.BooleanField(default=False, help_text="Muhim e'lon (pop-up)")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True, help_text="Muddati")
    
    class Meta:
        ordering = ['-created_at', '-is_important']
    
    def __str__(self):
        return self.title
    
    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False

# --- Yangilangan ChatMessage modeli ---
class ChatMessage(models.Model):
    """Operator ↔ Admin muloqot"""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(null=True, blank=True)
    
    # Yangi maydonlar
    sticker = models.CharField(max_length=100, blank=True, null=True, help_text="Sticker emoji")
    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.sender.username} → {self.recipient.username}: {self.message[:30]}"

# --- Yangi model - Message Reaction ---
class MessageReaction(models.Model):
    """Xabarga reaksiya"""
    REACTION_CHOICES = [
        ('👍', 'Like'),
        ('❤️', 'Love'),
        ('😂', 'Laugh'),
        ('😮', 'Wow'),
        ('😢', 'Sad'),
        ('😡', 'Angry'),
        ('🎉', 'Celebrate'),
        ('👀', 'Look'),
    ]
    
    message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction = models.CharField(max_length=10, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['message', 'user']
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.user.username} {self.reaction}"

# --- Yangi model - Sticker Pack ---
class StickerPack(models.Model):
    """Sticker to'plamlari"""
    name = models.CharField(max_length=100)
    emoji = models.CharField(max_length=100, help_text="Vergul bilan ajratilgan")
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

# --- Site Logotipi modeli ---
class SiteLogo(models.Model):
    """Sayt logotipini boshqarish"""
    logo = models.ImageField(upload_to='logos/', help_text="Sayt logotipi")
    is_active = models.BooleanField(default=True, help_text="Logotip faol yoki yo'qligi")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Logotip {self.id}"
    
    @classmethod
    def get_active_logo(cls):
        """Faol logotipni olish"""
        return cls.objects.filter(is_active=True).first()

class LoginPageContent(models.Model):
    """Kirish sahifasida ko'rsatiladigan universitet ma'lumotlari"""
    title = models.CharField(max_length=200, default='Buxoro Innovatsiyalar Universiteti')
    subtitle = models.CharField(max_length=200, blank=True, default='HEMIS OTM axborot tizimi')
    about_text = models.TextField(blank=True, help_text='Universitet haqida maʼlumot')
    directions = models.TextField(blank=True, help_text='Yoʻnalishlar yoki asosiy yoʻnalishlar')
    logo = models.ImageField(upload_to='login_page/', blank=True, null=True, help_text='Kirish sahifasida koʻrsatiladigan logotip')
    is_active = models.BooleanField(default=True, help_text='Bu matn va logo faolmi')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Kirish sahifa kontenti {self.id}"

    @classmethod
    def get_active_content(cls):
        return cls.objects.filter(is_active=True).first()


class LandingPageContent(models.Model):
    """Bosh sahifa (landing page) uchun sozlamalar - super admin o'zgartiradi"""
    hero_title = models.CharField(max_length=200, default="Ta'lim va taraqqiyot yo'lidamiz")
    hero_subtitle = models.CharField(max_length=200, default='TALABA BOSHQARUV TIZIMI')
    hero_description = models.TextField(default="Zamonaviy ta'lim tizimi orqali talabalarni qabul qilish va boshqaruvni avtomatlashtirish")
    hero_image = models.ImageField(upload_to='landing/', blank=True, null=True, help_text='Hero rasm')
    hero_video = models.FileField(upload_to='landing/videos/', blank=True, null=True, help_text='Hero video (MP4)')

    # Kontakt ma'lumotlari
    contact_address = models.CharField(max_length=300, default="Toshkent sh., O'zbekiston")
    contact_phone = models.CharField(max_length=50, default='+998 71 123 45 67')
    contact_email = models.EmailField(default='info@minihemis.uz')
    contact_location_url = models.URLField(blank=True, help_text='Google Maps URL')

    # About bo'limi
    about_title = models.CharField(max_length=200, default='Bizning maqsadimiz')
    about_text = models.TextField(blank=True, default='Universitet haqida ma\'lumot')

    # Statistika raqamlari (qo'lda sozlash uchun)
    override_students_count = models.IntegerField(blank=True, null=True, help_text="Talabalar soni (qo'lda sozlash uchun, bo'sh qoldirilsa avtomatik hisoblanadi)")
    override_applications_count = models.IntegerField(blank=True, null=True, help_text="Arizalar soni (qo'lda sozlash uchun, bo'sh qoldirilsa avtomatik hisoblanadi)")
    override_faculties_count = models.IntegerField(blank=True, null=True, help_text="Fakultetlar soni (qo'lda sozlash uchun, bo'sh qoldirilsa avtomatik hisoblanadi)")
    override_specialties_count = models.IntegerField(blank=True, null=True, help_text="Yo'nalishlar soni (qo'lda sozlash uchun, bo'sh qoldirilsa avtomatik hisoblanadi)")

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Landing Page Content'
        verbose_name_plural = 'Landing Page Contents'

    def __str__(self):
        return f"Landing Page #{self.id}"

    @classmethod
    def get_active(cls):
        return cls.objects.filter(is_active=True).first()


class LandingNews(models.Model):
    """Bosh sahifada ko'rsatiladigan yangiliklar"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='landing/news/', blank=True, null=True)
    video_url = models.URLField(blank=True, help_text='YouTube/Vimeo URL')
    link = models.URLField(blank=True, help_text='Batafsil link')
    order = models.IntegerField(default=0, help_text='Tartibi (kichik raqam - birinchi)')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Landing Yangilik'
        verbose_name_plural = 'Landing Yangiliklar'

    def __str__(self):
        return self.title


# --- Talaba To'lovlari modeli ---
class StudentPayment(models.Model):
    """Talabaning to'lov ma'lumotlari"""
    PAYMENT_TYPE_CHOICES = (
        ('tuition', "O'quv to'lovi"),
        ('contract', 'Shartnoma tolovi'),
        ('other', 'Boshqa'),
    )
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments', verbose_name="Talaba")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="To'lov summasi")
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES, default='tuition', verbose_name="To'lov turi")
    payment_date = models.DateField(verbose_name="To'lov sanasi")
    description = models.TextField(blank=True, null=True, verbose_name="Izoh")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Kiritdi")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-payment_date', '-created_at']
        verbose_name = "Talaba to'lovi"
        verbose_name_plural = "Talaba to'lovlari"
    
    def __str__(self):
        return f"{self.student.full_name} - {self.amount:,.0f} so'm ({self.payment_date})"

# --- PasswordResetToken modeli O'CHIRILDI (email parol tiklash funksiyasi bilan birga) ---


class ExcelImportConfig(models.Model):
    """Excel import ustunlar sozlamalari - super admin uchun"""
    full_name_col = models.CharField(max_length=2, default='A', verbose_name="Ism Familiya (F.I.SH) ustuni")
    passport_col = models.CharField(max_length=2, default='B', verbose_name="Pasport ustuni")
    jshshir_col = models.CharField(max_length=2, default='C', verbose_name="JSHSHIR ustuni")
    course_col = models.CharField(max_length=2, default='D', verbose_name="Kurs ustuni")
    phone_col = models.CharField(max_length=2, default='E', verbose_name="Telefon ustuni")
    faculty_col = models.CharField(max_length=2, default='F', verbose_name="Fakultet ustuni")
    specialty_col = models.CharField(max_length=2, default='G', verbose_name="Mutaxassislik ustuni")
    operator_comment_col = models.CharField(max_length=2, default='H', verbose_name="Operator izohi ustuni")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Excel import sozlamasi"
        verbose_name_plural = "Excel import sozlamalari"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Excel import sozlamasi ({'Faol' if self.is_active else 'Faol emas'}) - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
        
    @classmethod
    def get_active_config(cls):
        """Faol excel sozlamalarini olish, agar yo'q bo'lsa default yaratadi"""
        cfg = cls.objects.filter(is_active=True).first()
        if not cfg:
            cfg = cls.objects.create(
                full_name_col='A',
                passport_col='B',
                jshshir_col='C',
                course_col='D',
                phone_col='E',
                faculty_col='F',
                specialty_col='G',
                operator_comment_col='H',
                is_active=True
            )
        return cfg

    def get_ordered_columns(self):
        """Qator/ustunlarni tartiblangan holda qaytaradi (A, B, C...)"""
        fields = [
            ('full_name', self.full_name_col, "To'liq ism familiya"),
            ('passport', self.passport_col, "Pasport seriya va raqami (AA1234567)"),
            ('jshshir', self.jshshir_col, "JSHSHIR (14 ta raqam)"),
            ('course', self.course_col, "Kurs (1, 2, 3, 4)"),
            ('phone', self.phone_col, "Telefon raqam"),
            ('faculty', self.faculty_col, "Fakultet nomi"),
            ('specialty', self.specialty_col, "Mutaxassislik nomi"),
            ('operator_comment', self.operator_comment_col, "Operator izohi (ixtiyoriy)"),
        ]
        from openpyxl.utils import column_index_from_string
        ordered = []
        for field, col, label in fields:
            if col:
                try:
                    idx = column_index_from_string(col.upper())
                    ordered.append((idx, col.upper(), label))
                except ValueError:
                    pass
        ordered.sort()
        return [{'index': idx, 'column': col, 'label': label} for idx, col, label in ordered]

