from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model
from users.models import UserAccount, ReportModel#, UserFile

UserAccount=get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"})

    class Meta:
        model = UserAccount
        fields=('email', 'first_name', 'last_name', 'birth_date','gender','native_language', 'country', 'password', 'password2')
        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True}
        }
    def save(self):
        
        user = UserAccount(
            email = self.validated_data['email'],
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name'],
            birth_date = self.validated_data['birth_date'],
            gender = self.validated_data['gender'],
            native_language = self.validated_data['native_language'],
            country = self.validated_data['country']
        ) 
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({"password": "Passwords do not match!"})
        user.set_password(password)
        user.save()
        return "user"

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField() 
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True)
    
class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ("email","first_name","birth_date","last_name","gender", "report_test", "profile_photo")


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['profile_photo']


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportModel
        fields = "__all__"


class CategoryFileSerializer(serializers.Serializer):
    category = serializers.CharField(max_length=150)
    file = serializers.FileField(allow_empty_file=False)

class UserVerificationFileUploadSerializer(serializers.Serializer):
    def to_internal_value(self, data):
        category_file_data = []
        for category, files in data.lists():
            category_file_data.append({'category': category, 'files': files})
        
        return category_file_data
    

    category = serializers.CharField(max_length=150) #for test
    # file = serializers.FileField(allow_empty_file=False)
    file = serializers.CharField(max_length=150) #for test
    


