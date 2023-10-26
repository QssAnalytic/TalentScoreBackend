from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
import pytest
import uuid

from users.models import UserAccount, UserAccountFilePage, ReportModel, CertificateModel, UniqueRandom, UserVerificationFile, UserCV, UserProfile



        
        
        
@pytest.mark.django_db
def test_userprofile_creation():
    user = UserAccount.objects.create(email='test@example.com')
    user_profile = UserProfile(user=user)
    user_profile.save()
    assert UserProfile.objects.count() == 1

@pytest.mark.django_db
def test_userprofile_str_method():
    user = UserAccount.objects.create(email='test@example.com')
    user_profile = UserProfile(user=user)
    assert str(user_profile) == 'test@example.com'

@pytest.mark.django_db
def test_userprofile_general_questions_default():
    user = UserAccount.objects.create(email='test@example.com')
    user_profile = UserProfile(user=user)
    user_profile.save()
    assert user_profile.general_questions is None

@pytest.mark.django_db
def test_userprofile_secondary_education_questions_default():
    user = UserAccount.objects.create(email='test@example.com')
    user_profile = UserProfile(user=user)
    user_profile.save()
    assert user_profile.secondary_education_questions is None
        
        


@pytest.mark.django_db
def test_date_created_auto_now_add():
    user = UserAccount.objects.create(email='test@example.com')
    user_profile = UserProfile(user=user)
    user_profile.save()  # Save the user profile to trigger the auto_now_add behavior
    assert user_profile.date_created is not None


@pytest.mark.django_db
def test_userprofile_special_skills_score_zero():
    """
    Проверка, что 'special_skills_score' может быть равным нулю
    """
    user = UserAccount.objects.create(email='test@example.com')
    user_profile = UserProfile(user=user, special_skills_score=0)
    user_profile.save()
    assert user_profile.special_skills_score == 0


@pytest.mark.django_db
def test_userprofile_program_questions_empty():
    """
    Проверка, что 'program_questions' может быть пустым списком
    """
    user = UserAccount.objects.create(email='test@example.com')
    user_profile = UserProfile(user=user, program_questions=[])
    user_profile.save()
    assert user_profile.program_questions == []


@pytest.mark.django_db
def test_userprofile_scores_and_colors_defaults():
    user = UserAccount.objects.create(email='test@example.com')
    user_profile = UserProfile(user=user)

    assert user_profile.education_score == 1
    assert user_profile.education_color == '#00E5BC'

    assert user_profile.language_score == 1
    assert user_profile.language_color == '#FF0038'

    assert user_profile.special_skills_score == 1
    assert user_profile.special_skills_color == '#00A8E1'

    assert user_profile.sport_score == 1
    assert user_profile.sport_color == '#09959A'

    assert user_profile.work_experiance_score == 1
    assert user_profile.work_experiance_color == '#FFCB05'

    assert user_profile.program_score == 1
    assert user_profile.program_color == '#8800E0'






@pytest.mark.django_db
def test_create_certificate_model():
    user = UserAccount.objects.create_user(
        email='test@example.com',
        password='password123',
    )
    user_profile = UserProfile.objects.create(user=user)
    
    certificate_file = UserAccountFilePage.objects.create(
        user=user_profile,  # Here, we associate the UserProfile's user with the certificate_file
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



@pytest.mark.django_db
def test_create_report_model():
    user = UserAccount.objects.create_user(email='test@example.com', password='password123')
    user_profile = UserProfile.objects.create(user=user)
    report_file = UserAccountFilePage.objects.create(user=user_profile, file_category='REPORT')
    report = ReportModel.objects.create(report_file=report_file, user=user)
    assert report.report_file == report_file

    
    
@pytest.mark.django_db   
def test_report_model_date_created_auto_now_add():
    user = UserAccount.objects.create_user(email='test@example.com', password='password123')
    user_profile = UserProfile.objects.create(user=user)
    report_file = UserAccountFilePage.objects.create(user=user_profile, file_category='REPORT')
    report = ReportModel.objects.create(report_file=report_file, user=user)
    assert report.date_created is not None