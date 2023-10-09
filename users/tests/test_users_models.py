from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
import pytest
import uuid

from users.models import UserAccount, UserAccountFilePage, ReportModel, CertificateModel, UniqueRandom, UserVerificationFile, UserCV


@pytest.mark.django_db
def test_create_report():
    user_account_file = UserAccountFilePage.objects.create(file_category="REPORT", user=UserAccount.objects.create(email="test@example.com"))
    
    report = ReportModel.objects.create(
        report_file=user_account_file,

        user=user_account_file.user
    )
    
    assert report.report_file == user_account_file
    assert report.user == user_account_file.user



@pytest.mark.django_db
def test_general_questions_validation():
    
    user = UserAccount.objects.create(email='test@example.com')
    
   
    try:
        report = ReportModel(
            general_questions=[1, 2, 3],  
           
        )
        report.full_clean()
    except ValidationError as e:
        assert 'general_questions' in e.message_dict

@pytest.mark.django_db
def test_program_color_default():
    user = UserAccount.objects.create(email='test@example.com')
    report = ReportModel(user=user)  
    assert report.program_color == '#8800E0'  

@pytest.mark.django_db
def test_work_experiance_score_default():
    user = UserAccount.objects.create(email='test@example.com')
    report = ReportModel(user=user)  
    assert report.work_experiance_score == 1  

@pytest.mark.django_db
def test_work_experiance_color_default():
    user = UserAccount.objects.create(email='test@example.com')
    report = ReportModel(user=user)  
    assert report.work_experiance_color == '#FFCB05'  

@pytest.mark.django_db
def test_education_score_default():
    user = UserAccount.objects.create(email='test@example.com')
    report = ReportModel(user=user)  
    assert report.education_score == 1  

@pytest.mark.django_db
def test_language_score_default():
    user = UserAccount.objects.create(email='test@example.com')
    report = ReportModel(user=user)  
    assert report.language_score == 1  

@pytest.mark.django_db
def test_special_skills_score_default():
    user = UserAccount.objects.create(email='test@example.com')
    report = ReportModel(user=user)  
    assert report.special_skills_score == 1  

@pytest.mark.django_db
def test_sport_score_default():
    user = UserAccount.objects.create(email='test@example.com')
    report = ReportModel(user=user)  
    assert report.sport_score == 1  

@pytest.mark.django_db
def test_date_created_auto_now_add():
    user = UserAccount.objects.create(email='test@example.com')
    report = ReportModel(user=user)
    report.save()  # Save the report to trigger the auto_now_add behavior
    assert report.date_created is not None

@pytest.mark.django_db
def test_report_file_default():
    user = UserAccount.objects.create(email='test@example.com')
    report = ReportModel(user=user)  # Create a report without specifying report_file
    assert report.report_file is None  # Check if report_file defaults to None







@pytest.mark.django_db
def test_create_certificate_model():
    user = UserAccount.objects.create_user(
        email='test@example.com',
        password='password123',
    )
    certificate_file = UserAccountFilePage.objects.create(
        user=user,
        file_category='CERTIFICATE',
    )
    certificate = CertificateModel.objects.create(
        certificate_file=certificate_file,
    )
    assert certificate.certificate_file == certificate_file





from django.db.utils import IntegrityError

@pytest.mark.django_db
def test_user_account_email_unique():
   
    UserAccount.objects.create_user(email="test@example.com", password="password")
    
    with pytest.raises(IntegrityError):
        UserAccount.objects.create_user(email="test@example.com", password="password")



@pytest.mark.django_db
def test_create_unique_random():
    user = UserAccount.objects.create_user(
        email='test@example.com',
        password='password123',
    )
    unique_random = UniqueRandom.objects.create(
        user=user,
        unique_value=str(uuid.uuid4()),
    )
    assert unique_random.user == user

@pytest.mark.django_db
def test_unique_random_unique_value():
    # Create a UniqueRandom instance with a specific unique_value
    UniqueRandom.objects.create(unique_value="unique_value_1")
    # Try to create another instance with the same unique_value
    with pytest.raises(IntegrityError):
        UniqueRandom.objects.create(unique_value="unique_value_1")




@pytest.mark.django_db
def test_user_verification_file_creation():
    user = UserAccount.objects.create(email="testuser@gmail.com", password="testpassword")
    file = SimpleUploadedFile("file.txt", b"file_content")
    verification_file = UserVerificationFile.objects.create(
        user=user,
        category="test_category",
        file=file
    )
    assert verification_file.id is not None
    assert str(verification_file) == 'UserVerificationFile object ({})'.format(verification_file.id)

@pytest.mark.django_db
def test_user_verification_file_category_length():
    with pytest.raises(Exception):
        user = UserAccount.objects.create(username="testuser", password="testpassword")
        file = SimpleUploadedFile("file.txt", b"file_content")
        
        
        with pytest.raises(Exception):
            verification_file = UserVerificationFile.objects.create(
                user=user,
                category="a" * 151,  
                file=file
            )

        
        assert UserVerificationFile.objects.count() == 0

@pytest.mark.django_db(transaction=True)
def test_user_verification_file_without_user():
    file = SimpleUploadedFile("file.txt", b"file_content")
    with pytest.raises(Exception):
        verification_file = UserVerificationFile.objects.create(
            user=None,
            category="test_category",
            file=file
        )
    assert UserVerificationFile.objects.count() == 0

@pytest.mark.django_db
def test_user_verification_file_deletion():
    user = UserAccount.objects.create(email="testuser@gmail.com", password="testpassword")
    file = SimpleUploadedFile("file.txt", b"file_content")
    verification_file = UserVerificationFile.objects.create(
        user=user,
        category="test_category",
        file=file
    )
    verification_file.delete()
    assert UserVerificationFile.objects.count() == 0

@pytest.mark.django_db
def test_create_user_verification_file():

    user = UserAccount.objects.create_user(
        email='test@example.com',
        password='password123',
    )
    user_verification_file = UserVerificationFile.objects.create(
        user=user,
        category='CATEGORY',
    )
    assert user_verification_file.user == user
    assert user_verification_file.category == 'CATEGORY'


