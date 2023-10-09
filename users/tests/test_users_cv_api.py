from users.api.cv_views import JobTitleAPIView, SummryPromptAPIView

import pytest


from users.models import ReportModel, UserAccount, UserAccountFilePage



@pytest.mark.django_db
def test_create_report_model():
    
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

    report_model = ReportModel.objects.create(
        general_questions=fake_report_data['general_questions'],
        user=user
    )

    assert ReportModel.objects.count() == 1

    assert report_model.user.email == fake_email

    assert report_model.general_questions == fake_report_data['general_questions']




