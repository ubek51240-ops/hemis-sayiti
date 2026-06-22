from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):
    """
    Django admin panel uchun custom foydalanuvchi yaratish formasi
    To'g'ri Uzbekcha label'lar va xatolik xabarlari bilan
    """
    
    username = forms.CharField(
        label="Foydalanuvchi nomi",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Login nomini kiriting'
        })
    )
    
    password1 = forms.CharField(
        label="Parol",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Parolni kiriting'
        }),
        help_text=(
            "<ul>"
            "<li>Parolingiz kamida 8 ta belgidan iborat bo'lishi kerak.</li>"
            "<li>Parolingiz shaxsiy ma'lumotlaringizga juda o'xshash bo'lmasligi kerak.</li>"
            "<li>Parolingiz faqat raqamlardan iborat bo'lmasligi kerak.</li>"
            "<li>Siz keng tarqalgan parollardan foydalanmaysiz.</li>"
            "</ul>"
        )
    )
    
    password2 = forms.CharField(
        label="Parolni tasdiqlang",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Parolni qayta kiriting'
        }),
        help_text="Parolni tasdiqlash uchun yana bir kiriting."
    )

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {
            'username': forms.CharField,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove any auto-generated help text that might conflict
        if hasattr(self.fields['username'], 'help_text'):
            self.fields['username'].help_text = "Faqat harflar, raqamlar va @/./+/-/_ belgilari."

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Kiritilgan parollar mos kelmadi!")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
