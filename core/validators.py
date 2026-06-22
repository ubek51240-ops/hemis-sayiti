from django.contrib.auth.password_validation import (
    UserAttributeSimilarityValidator,
    MinimumLengthValidator,
    CommonPasswordValidator,
    NumericPasswordValidator,
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class UzbekUserAttributeSimilarityValidator(UserAttributeSimilarityValidator):
    """
    Parol foydalanuvchi ma'lumotlariga juda o'xshash bo'lmasligini tekshirish (Uzbekcha)
    """
    def validate(self, password, user=None):
        if not user:
            return
        
        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if value and self.similarity(password, value) > self.max_similarity:
                raise ValidationError(
                    "Parolingiz shaxsiy ma'lumotlaringizga juda o'xshash.",
                    code='password_too_similar',
                    params={'attribute': attribute_name},
                )


class UzbekMinimumLengthValidator(MinimumLengthValidator):
    """
    Parol minimal uzunligini tekshirish (Uzbekcha)
    """
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                f"Parolingiz kamida {self.min_length} ta belgidan iborat bo'lishi kerak.",
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return f"Parolingiz kamida {self.min_length} ta belgidan iborat bo'lishi kerak."


class UzbekCommonPasswordValidator(CommonPasswordValidator):
    """
    Umumiy parollarni tekshirish (Uzbekcha)
    """
    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValidationError(
                "Bu juda keng tarqalgan parol. Boshqa parol tanlang.",
                code='password_too_common',
            )

    def get_help_text(self):
        return "Siz keng tarqalgan parollardan foydalanmaysiz."


class UzbekNumericPasswordValidator(NumericPasswordValidator):
    """
    Raqamli parollarni tekshirish (Uzbekcha)
    """
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                "Parol to'liq raqamlardan iborat bo'la olmaydi.",
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        return "Parolingiz faqat raqamlardan iborat bo'lmasligi kerak."


class ComplexPasswordValidator:
    """
    Murakkab parol validator
    Kuchli parollarni talab qilish
    """
    
    def validate(self, password, user=None):
        errors = []
        
        # Kamida 1 ta katta harf
        if not any(char.isupper() for char in password):
            errors.append("Parolda kamida 1 ta katta harf (A-Z) bo'lishi kerak.")
        
        # Kamida 1 ta kichik harf
        if not any(char.islower() for char in password):
            errors.append("Parolda kamida 1 ta kichik harf (a-z) bo'lishi kerak.")
        
        # Kamida 1 ta raqam
        if not any(char.isdigit() for char in password):
            errors.append("Parolda kamida 1 ta raqam (0-9) bo'lishi kerak.")
        
        # Kamida 1 ta maxsus belgi
        special_chars = r"!@#$%^&*()_+-=[]{}|;:,.<>?"
        if not any(char in special_chars for char in password):
            errors.append(f"Parolda kamida 1 ta maxsus belgi ({special_chars}) bo'lishi kerak.")
        
        # Bo'sh joy tekshiruvi
        if ' ' in password:
            errors.append("Parolda bo'sh joy bo'lmasligi kerak.")
        
        if errors:
            from django.core.exceptions import ValidationError
            raise ValidationError(errors)
    
    def get_help_text(self):
        return (
            "Parol quyidagi talablar ga javob berishi kerak:\n"
            "- Kamida 8 ta belgi\n"
            "- Kamida 1 ta katta harf (A-Z)\n"
            "- Kamida 1 ta kichik harf (a-z)\n"
            "- Kamida 1 ta raqam (0-9)\n"
            "- Kamida 1 ta maxsus belgi (!@#$%^&*...)\n"
            "- Bo'sh joylarsiz"
        )
