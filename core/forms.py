from django import forms
from .models import Student, Profile, Faculty, Specialty, ExcelDownloadRequest, Announcement, ChatMessage, MessageReaction, SiteLogo, LoginPageContent, StudentPayment, Application, Comment, ExcelImportConfig
from django.contrib.auth.models import User
import re

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['passport', 'jshshir', 'full_name', 'course', 'phone', 'faculty', 'specialty', 'transcript', 'passport_scan', 'additional_documents']
        widgets = {
            'passport': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'AA1234567', 
                'style': 'text-transform:uppercase',
                'maxlength': '9',
                'id': 'id_passport'
            }),
            'jshshir': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '14 ta raqam',
                'maxlength': '14',
                'id': 'id_jshshir'
            }),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+998901234567'}),
            'faculty': forms.Select(attrs={'class': 'form-control', 'id': 'id_faculty'}),
            'specialty': forms.Select(attrs={'class': 'form-control', 'id': 'id_specialty'}),
            'transcript': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png'}),
            'passport_scan': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.jpg,.jpeg,.png'}),
            'additional_documents': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png'}),
        }

    def clean_passport(self):
        passport = self.cleaned_data.get('passport', '')
        return passport.strip().upper()

    def clean_jshshir(self):
        jshshir = self.cleaned_data.get('jshshir', '')
        return ''.join(c for c in jshshir if c.isdigit())

    def validate_uploaded_file(self, file_data, allowed_extensions, max_size_mb=5):
        if file_data:
            import os
            ext = os.path.splitext(file_data.name)[1].lower()
            if ext not in allowed_extensions:
                raise forms.ValidationError(f"Nomaqbul fayl formati! Faqat quyidagilarga ruxsat beriladi: {', '.join(allowed_extensions)}")
            
            max_size_bytes = max_size_mb * 1024 * 1024
            if file_data.size > max_size_bytes:
                raise forms.ValidationError(f"Fayl hajmi {max_size_mb} MB dan oshmasligi kerak!")
        return file_data

    def clean_transcript(self):
        transcript = self.cleaned_data.get('transcript')
        return self.validate_uploaded_file(transcript, ['.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png'])

    def clean_passport_scan(self):
        passport_scan = self.cleaned_data.get('passport_scan')
        return self.validate_uploaded_file(passport_scan, ['.pdf', '.jpg', '.jpeg', '.png'])

    def clean_additional_documents(self):
        additional_documents = self.cleaned_data.get('additional_documents')
        return self.validate_uploaded_file(additional_documents, ['.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png'])

    def clean(self):
        cleaned_data = super().clean()
        course = cleaned_data.get('course')
        transcript = cleaned_data.get('transcript')
        passport_scan = cleaned_data.get('passport_scan')

        if course in [2, 3, 4]:
            if not transcript:
                self.add_error('transcript', '2-4 kurs transfer talabasi uchun transcript yuklash kerak.')
            if not passport_scan:
                self.add_error('passport_scan', '2-4 kurs transfer talabasi uchun pasport rasmini yuklash kerak.')

        return cleaned_data

class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Eski parol'
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Yangi parol'
    )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['comment', 'status']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SpecialtyForm(forms.ModelForm):
    class Meta:
        model = Specialty
        fields = ['faculty', 'name']
        widgets = {
            'faculty': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ExcelRequestForm(forms.ModelForm):
    class Meta:
        model = ExcelDownloadRequest
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Excel yuklash sababini batafsil yozing...'
            }),
        }

class ExcelAdminForm(forms.ModelForm):
    class Meta:
        model = ExcelDownloadRequest
        fields = ['status', 'admin_comment']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'admin_comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Izoh yozing...'
            }),
        }

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'message', 'target_group', 'is_active', 'is_important', 'expires_at']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'target_group': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_important': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'expires_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

# --- Yangilangan ChatMessageForm ---
class ChatMessageForm(forms.ModelForm):
    """Chat xabari formasi"""
    sticker = forms.ChoiceField(
        choices=[
            ('', '💬 Xabar'),
            ('👍', '👍 Like'),
            ('❤️', '❤️ Love'),
            ('😂', '😂 Laugh'),
            ('😮', '😮 Wow'),
            ('😢', '😢 Sad'),
            ('😡', '😡 Angry'),
            ('🎉', '🎉 Celebrate'),
            ('🔥', '🔥 Fire'),
            ('✨', '✨ Sparkle'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = ChatMessage
        fields = ['message', 'sticker', 'reply_to']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',  # ✅ Tuzatildi: 'form-control'
                'rows': 3,
                'placeholder': 'Xabar yozing...',
                'id': 'id_message'
            }),
            'sticker': forms.Select(attrs={'class': 'form-control'}),
            'reply_to': forms.HiddenInput(),
        }

# --- Yangi forma: MessageReactionForm ---
class MessageReactionForm(forms.Form):
    """Xabarga reaksiya qo'shish formasi"""
    reaction = forms.ChoiceField(
        choices=MessageReaction.REACTION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class ExcelUploadForm(forms.Form):
    """Excel file upload form for bulk student addition"""
    excel_file = forms.FileField(
        label='Excel fayli',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx,.xls'
        }),
        help_text='Faqat .xlsx yoki .xls formatdagi fayllar'
    )

class LoginPageContentForm(forms.ModelForm):
    class Meta:
        model = LoginPageContent
        fields = ['title', 'subtitle', 'about_text', 'directions', 'logo', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'subtitle': forms.TextInput(attrs={'class': 'form-control'}),
            'about_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'directions': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class StudentRegistrationForm(forms.ModelForm):
    """Talaba ro'yxatdan o'tish formasi - O'qishga kirish uchun"""
    full_name = forms.CharField(
        label='F.I.Sh',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Familiya Ism Sharif'
        })
    )
    passport = forms.CharField(
        label='Pasport raqami',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'AA1234567',
            'style': 'text-transform:uppercase',
            'maxlength': '9'
        }),
        max_length=9
    )
    jshshir = forms.CharField(
        label='JSHSHIR',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '14 ta raqam',
            'maxlength': '14'
        }),
        max_length=14
    )
    phone = forms.CharField(
        label='Telefon raqam',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+998901234567'
        }),
        max_length=20
    )
    faculty = forms.ModelChoiceField(
        label='Fakultet',
        queryset=Faculty.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_faculty'}),
        required=True
    )
    specialty = forms.ModelChoiceField(
        label="Yo'nalish",
        queryset=Specialty.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_specialty'}),
        required=True
    )
    password = forms.CharField(
        label='Parol',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Parolni kiriting (kamida 8 ta belgi)'
        }),
        min_length=8
    )
    confirm_password = forms.CharField(
        label='Parolni tasdiqlang',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Parolni qayta kiriting'
        })
    )

    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email manzil'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Fakultet tanlanganida specialty'larni yangilash uchun JS kerak
        faculty_id = self.data.get('faculty')
        if faculty_id:
            try:
                faculty_id = int(faculty_id)
                self.fields['specialty'].queryset = Specialty.objects.filter(faculty_id=faculty_id)
            except (ValueError, TypeError):
                pass

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Bu email manzil allaqachon ro\'yxatdan o\'tgan!')
        return email

    def clean_passport(self):
        passport = self.cleaned_data.get('passport', '').strip().upper()
        if not re.match(r'^[A-Z]{2}\d{7}$', passport):
            raise forms.ValidationError('Pasport formati noto\'g\'ri! (masalan: AA1234567)')
        if User.objects.filter(username=passport).exists():
            raise forms.ValidationError('Bu pasport raqami allaqachon ro\'yxatdan o\'tgan!')
        return passport

    def clean_jshshir(self):
        jshshir = self.cleaned_data.get('jshshir', '').strip()
        if not re.match(r'^\d{14}$', jshshir):
            raise forms.ValidationError('JSHSHIR 14 ta raqamdan iborat bo\'lishi kerak!')
        return jshshir

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Parollar mos kelmaydi!')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        passport = self.cleaned_data['passport']
        user.username = passport  # Talaba uchun username = pasport
        user.set_password(self.cleaned_data['password'])
        user.first_name = self.cleaned_data['full_name']
        if commit:
            user.save()
            if hasattr(user, 'profile'):
                profile = user.profile
                profile.role = 'student'
                profile.jshshir = self.cleaned_data.get('jshshir')
                profile.phone = self.cleaned_data.get('phone')
                profile.email = self.cleaned_data.get('email')
                profile.roles = ['student']
                profile.save()

            # Avtomatik Application record yaratish
            Application.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                passport=passport,
                email=user.email,
                phone=self.cleaned_data['phone'],
                faculty=self.cleaned_data['faculty'],
                specialty=self.cleaned_data['specialty'],
                status='pending'
            )

            # Avtomatik Student record yaratish (bosh sahifada ko'rinishi uchun)
            # created_by=None - bu o'zi ro'yxatdan o'tganligini ko'rsatadi
            jshshir = self.cleaned_data.get('jshshir', '')
            if not Student.objects.filter(passport=passport).exists():
                try:
                    Student.objects.create(
                        passport=passport,
                        jshshir=jshshir,
                        full_name=self.cleaned_data['full_name'],
                        course=1,  # Default 1-kurs (o'zi ro'yxatdan o'tish)
                        phone=self.cleaned_data['phone'],
                        faculty=self.cleaned_data['faculty'],
                        specialty=self.cleaned_data['specialty'],
                        status='pending',
                        created_by=None,  # O'zi ro'yxatdan o'tgan - operatori yo'q
                    )
                except Exception:
                    pass  # Agar JSHSHIR takrorlansa, Student yaratilmasin
        return user


class EmployeeRegistrationForm(forms.ModelForm):
    """Xodim ro'yxatdan o'tish formasi - Rol olish uchun"""
    full_name = forms.CharField(
        label='Ism Familiya',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ism Familiya'
        })
    )
    username = forms.CharField(
        label='Login',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Loginni kiriting (masalan: azizbek)'
        }),
        help_text='Login uchun faqat harflar va raqamlar ishlatiladi'
    )
    phone = forms.CharField(
        label='Telefon raqam',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+998901234567'
        }),
        max_length=20
    )
    password = forms.CharField(
        label='Parol',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Parolni kiriting (kamida 8 ta belgi)'
        }),
        min_length=8
    )
    confirm_password = forms.CharField(
        label='Parolni tasdiqlang',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Parolni qayta kiriting'
        })
    )

    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email manzil'
            }),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip().lower()
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise forms.ValidationError('Login faqat harflar, raqamlar va pastki chiziqdan iborat bo\'lishi mumkin!')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Bu login allaqachon band!')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Bu email manzil allaqachon ro\'yxatdan o\'tgan!')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Parollar mos kelmaydi!')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        username = self.cleaned_data['username']
        user.username = username  # Xodim uchun o'z login
        user.set_password(self.cleaned_data['password'])
        user.first_name = self.cleaned_data['full_name']
        if commit:
            user.save()
            if hasattr(user, 'profile'):
                profile = user.profile
                profile.role = 'employee'
                profile.phone = self.cleaned_data.get('phone')
                profile.email = self.cleaned_data.get('email')
                profile.roles = ['employee']
                profile.save()

            # Xodim uchun Application yaratish (tasdiqlash uchun)
            Application.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                passport='',  # Xodim uchun pasport talab qilinmaydi
                email=user.email,
                phone=self.cleaned_data['phone'],
                faculty=None,  # Xodim uchun fakultet yo'q
                specialty=None,  # Xodim uchun yo'nalish yo'q
                status='pending'
            )
        return user

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        normalized = ''.join(c for c in phone if c.isdigit() or c == '+')
        if not normalized or len(re.sub(r'\D', '', normalized)) < 9:
            raise forms.ValidationError('Telefon raqam to\'g\'ri formatda emas.')
        return normalized

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Parollar mos kelmaydi!')

        return cleaned_data


class UserRegistrationForm(forms.ModelForm):
    """Super admin / admin uchun foydalanuvchi yaratish formasi"""
    password = forms.CharField(
        label='Parol',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Parolni kiriting (kamida 8 ta belgi)'
        }),
        min_length=8
    )
    confirm_password = forms.CharField(
        label='Parolni tasdiqlang',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Parolni qayta kiriting'
        })
    )
    role = forms.ChoiceField(
        label='Rol',
        choices=[
            ('operator', 'Operator'),
            ('admin', 'Admin'),
            # ('archive', 'Arxiv'), # Vaqtinchalik o'chirildi
            ('applicant', 'Ariza beruvchi'),
            ('student', 'Talaba (Ariza beruvchi)'),
            ('employee', 'Xodim (Ariza beruvchi)'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial='operator'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Login nomi'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email manzil'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ism'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Familiya'
            }),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Bu login nomi allaqachon mavjud!')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Bu email manzil allaqachon ro\'yxatdan o\'tgan!')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Parollar mos kelmaydi!')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            if hasattr(user, 'profile'):
                user.profile.role = self.cleaned_data['role']
                user.profile.save()
        return user

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['faculty', 'specialty']
        widgets = {
            'faculty': forms.Select(attrs={'class': 'form-control', 'id': 'id_faculty'}),
            'specialty': forms.Select(attrs={'class': 'form-control', 'id': 'id_specialty'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        faculty = cleaned_data.get('faculty')
        specialty = cleaned_data.get('specialty')
        if faculty and specialty and specialty.faculty != faculty:
            self.add_error('specialty', 'Tanlangan mutaxassislik tanlangan fakultetga tegishli bo\'lishi kerak.')
        return cleaned_data

class ApplicationReviewForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status', 'comment']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Izoh...'}),
        }

class UsernameChangeForm(forms.ModelForm):
    """Username o'zgartirish formasi"""
    current_password = forms.CharField(
        label='Joriy parol',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Joriy parolingizni kiriting'
        }),
        help_text='Xavfsizlik uchun joriy parolingizni kiriting'
    )

    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Yangi login nomi'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError('Bu login nomi allaqachon mavjud!')
        return username

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.user.check_password(current_password):
            raise forms.ValidationError('Parol noto\'g\'ri!')
        return current_password

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

class SiteLogoForm(forms.ModelForm):
    class Meta:
        model = SiteLogo
        fields = ['logo', 'is_active']
        widgets = {
            'logo': forms.FileInput(attrs={'class': 'form-control', 'accept': '.jpg,.jpeg,.png,.gif'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# --- PasswordReset formalari O'CHIRILDI (email parol tiklash funksiyasi bilan birga) ---
# PasswordResetRequestForm va PasswordResetConfirmForm olib tashlandi

class ProfileEditForm(forms.ModelForm):
    """Foydalanuvchi profilini tahrirlash uchun forma"""
    first_name = forms.CharField(
        max_length=30,
        required=False,
        label='Ism',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ismingiz'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        label='Familiya',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Familiyangiz'})
    )
    email = forms.EmailField(
        required=False,
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'})
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        label='Telefon raqam',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+998901234567'})
    )
    avatar = forms.ImageField(
        required=False,
        label='Profil rasmi',
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        help_text='JPG/PNG, maksimal 2MB'
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop('profile', None)
        super().__init__(*args, **kwargs)
        if self.profile:
            self.fields['phone'].initial = self.profile.phone

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar and hasattr(avatar, 'size') and avatar.size > 2 * 1024 * 1024:
            raise forms.ValidationError("Rasm hajmi 2MB dan oshmasligi kerak.")
        return avatar

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            if self.profile:
                self.profile.phone = self.cleaned_data.get('phone')
                self.profile.email = self.cleaned_data.get('email')
                avatar = self.cleaned_data.get('avatar')
                if avatar:
                    self.profile.avatar = avatar
                self.profile.save()
        return user


class CommentForm(forms.ModelForm):
    """Komment qo'shish uchun forma"""
    class Meta:
        model = Comment
        fields = ['content', 'is_internal']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Komment yozing...'
            }),
            'is_internal': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


class ExcelImportConfigForm(forms.ModelForm):
    class Meta:
        model = ExcelImportConfig
        fields = [
            'full_name_col', 'passport_col', 'jshshir_col', 'course_col',
            'phone_col', 'faculty_col', 'specialty_col', 'operator_comment_col',
            'is_active'
        ]
        widgets = {
            'full_name_col': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '2'}),
            'passport_col': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '2'}),
            'jshshir_col': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '2'}),
            'course_col': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '2'}),
            'phone_col': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '2'}),
            'faculty_col': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '2'}),
            'specialty_col': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '2'}),
            'operator_comment_col': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '2'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        cols = {}
        pattern = re.compile(r'^[A-Z]{1,2}$')
        
        fields_to_check = [
            'full_name_col', 'passport_col', 'jshshir_col', 'course_col',
            'phone_col', 'faculty_col', 'specialty_col', 'operator_comment_col'
        ]
        
        for field in fields_to_check:
            val = cleaned_data.get(field)
            if val:
                val = val.strip().upper()
                cleaned_data[field] = val
                if not pattern.match(val):
                    self.add_error(field, "Ustun nomi noto'g'ri (A-Z yoki AA-ZZ formatida bo'lishi kerak)")
                else:
                    if val in cols:
                        dup_field_label = self.fields[field].label or field
                        other_field_label = self.fields[cols[val]].label or cols[val]
                        self.add_error(field, f"Bu ustun '{other_field_label}' ustuni bilan bir xil bo'la olmaydi!")
                    cols[val] = field
            else:
                self.add_error(field, "Ushbu maydon majburiy.")
                
        return cleaned_data

