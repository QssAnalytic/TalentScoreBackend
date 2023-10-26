from users.api.cv_views import JobTitleAPIView, SummryPromptAPIView

import pytest


from users.models import ReportModel, UserAccount, UserAccountFilePage, UserProfile



@pytest.mark.django_db
def test_create_userprofile_with_report():

    fake_report_data = {
        'general_questions': {
            'formData': {
                'education': {'answer': 'Orta təhsil'},
                'educationGrant': {'answer': 'Əlaçı'},
            }
        }
    }


    fake_email = 'test@example.com'
    user = UserAccount.objects.create(email=fake_email)  


    user_profile = UserProfile.objects.create(
        general_questions=fake_report_data['general_questions'],
        user=user,
    )

    assert UserProfile.objects.count() == 1
    assert user_profile.user.email == fake_email
    assert user_profile.general_questions == fake_report_data['general_questions']







from rest_framework.test import APIClient
from django.urls import reverse
from users.models import UserAccount
import pytest

@pytest.mark.django_db
class TestCVEducationContenAPIViewAuthenticated:

    def test_get_education_content_authenticated(self):
        user = UserAccount.objects.create(email='test@example.com', password='password123')

        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse('cv-education-list')
        response = client.get(url)
        assert response.status_code == 200

@pytest.mark.django_db
class TestCVEducationContenAPIViewUnauthenticated:

    def test_get_education_content_unauthenticated(self):
        client = APIClient()
        url = reverse('cv-education-list')
        response = client.get(url)
        assert response.status_code == 401



@pytest.mark.django_db
class TestCvProgramQuestionAPIViewAuthenticated:

    def test_get_program_questions_authenticated(self):
        user = UserAccount.objects.create(email='test@example.com', password='password123')
        user_profile = UserProfile.objects.create(user=user)

        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse('cv-program')
        response = client.get(url)
        assert response.status_code == 200

@pytest.mark.django_db
class TestCvProgramQuestionAPIViewUnauthenticated:

    def test_get_program_questions_unauthenticated(self):
        client = APIClient()
        url = reverse('cv-program')
        response = client.get(url)
        assert response.status_code == 401












