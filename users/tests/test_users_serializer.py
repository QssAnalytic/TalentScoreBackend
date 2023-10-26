from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.utils import IntegrityError
from users.models import UserAccount, UserAccountFilePage, ReportModel, CertificateModel, UniqueRandom, UserVerificationFile, UserCV, UserProfile
from users.serializers import UserProfileSerializer, ReportSerializer
import pytest
import uuid

class TestUserProfileSerializer(TestCase):

    @pytest.mark.django_db
    def test_user_profile_serializer(self):
        user = UserAccount.objects.create(email='test@example.com')
        user_profile_data = {
            'user': user.pk,
            'general_questions': [1, 2, 3],
            'education_score': 0.8,
            'education_color': '#FF0000'
            
        }
        
        serializer = UserProfileSerializer(data=user_profile_data)
        assert serializer.is_valid()

class TestReportSerializer(TestCase):

    @pytest.mark.django_db
    def test_report_serializer(self):
        user = UserAccount.objects.create(email='test@example.com')
        user_profile = UserProfile.objects.create(user=user)
        report_file = UserAccountFilePage.objects.create(user=user_profile, file_category='REPORT')

        report_data = {
            'report_file': report_file.pk,
            'user': user.pk,
            'file_key': uuid.uuid4()
            
        }
        
        serializer = ReportSerializer(data=report_data)
        assert serializer.is_valid()



