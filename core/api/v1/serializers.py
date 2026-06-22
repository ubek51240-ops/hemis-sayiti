from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from core.models import Profile, Student, Faculty, Specialty

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'date_joined']
        read_only_fields = ['id', 'date_joined']
    
    def get_role(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.get_role_display()
        return 'operator'

# Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = ['id', 'user', 'role', 'assigned_admin']
        read_only_fields = ['id']

# Login Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Login yoki parol noto'g'ri")

# Student Serializer (qisqa)
class StudentListSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source='faculty.name', read_only=True)
    specialty_name = serializers.CharField(source='specialty.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Student
        fields = ['id', 'full_name', 'passport', 'course', 'faculty_name', 'specialty_name', 'status', 'status_display', 'created_at']

# Student Detail Serializer
class StudentDetailSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source='faculty.name', read_only=True)
    specialty_name = serializers.CharField(source='specialty.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at', 'approved_at']

    def validate(self, attrs):
        from django.core.exceptions import ValidationError as DjangoValidationError
        
        # Create a mock/temporary model instance to validate model constraints
        instance = self.instance
        if instance:
            # For update: apply changes to a copy of the instance to dry-run validation
            import copy
            instance_copy = copy.copy(instance)
            for field, value in attrs.items():
                setattr(instance_copy, field, value)
        else:
            # For create: construct a new instance with provided attributes
            instance_copy = Student(**attrs)
            
        try:
            instance_copy.clean()
        except DjangoValidationError as e:
            if hasattr(e, 'message_dict'):
                raise serializers.ValidationError(e.message_dict)
            raise serializers.ValidationError(e.messages)
            
        return attrs

# Faculty Serializer
class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['id', 'name']

# Specialty Serializer
class SpecialtySerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source='faculty.name', read_only=True)
    
    class Meta:
        model = Specialty
        fields = ['id', 'name', 'faculty', 'faculty_name']
