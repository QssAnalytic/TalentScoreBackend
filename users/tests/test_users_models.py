import pytest
from users.models import UserAccount, UserAccountFilePage, UserProfile
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError


@pytest.mark.django_db
def test_create_user_account():
    user = UserAccount.objects.create(
        first_name='Jhon',
        last_name='Doe',
        email='Jhon200@gmail.com',
        birth_date='2023-05-25',
        gender='Male',
        native_language='English',
        country='UK',
        is_active='True',
        is_superuser='False',
        is_staff='False'
        )
    retrieved_user = UserAccount.objects.get(last_name='Doe')
    assert retrieved_user == user

@pytest.mark.django_db
def test_unique_user_account():
    UserAccount.objects.create(
        email='Jhon200@gmail.com'
        )
    with pytest.raises(IntegrityError):
        UserAccount.objects.create(
        email='Jhon200@gmail.com'
        )

@pytest.mark.django_db
def test_invalid_user_account_birth_date():
    with pytest.raises(ValidationError):
        UserAccount.objects.create(birth_date='invalid-format')

# @pytest.mark.django_db
# def test_invalid_user_account_email():
#     with pytest.raises(ValidationError):
#         UserAccount.objects.create(email='invalid-format')


@pytest.mark.django_db
def test_blank_email():
    with pytest.raises(IntegrityError):
        UserAccount.objects.create(email=None)

@pytest.mark.django_db
def test_duplicate_email():
    UserAccount.objects.create(email='duplicate@example.com')
    with pytest.raises(IntegrityError):
        UserAccount.objects.create(email='duplicate@example.com')

@pytest.mark.django_db
def test_user_str_representation():
    user = UserAccount.objects.create(email="test@example.com")
    assert str(user) == "test@example.com"

@pytest.mark.django_db
def test_has_perm_and_has_module_perms():
    superuser = UserAccount.objects.create(email="superuser@example.com", is_superuser=True)
    regular_user = UserAccount.objects.create(email="user@example.com", is_superuser=False)

    assert superuser.has_perm("some_permission") is True
    assert regular_user.has_perm("some_permission") is False
    assert superuser.has_module_perms("some_app_label") is True
    assert regular_user.has_module_perms("some_app_label") is False

@pytest.mark.django_db
def test_create_user_account_file_page():
    user = UserAccount.objects.create_user(email='testuser@gmail.com', password='valid_password')
    user_profile = UserProfile.objects.create(user=user)
    user_account_file_page = UserAccountFilePage.objects.create(
        user=user_profile,
        file_category=UserAccountFilePage.FileCategoryChoices.CV,
        file='path/to/cv.pdf'
    )
    assert isinstance(user_account_file_page, UserAccountFilePage)
    assert user_account_file_page.user == user_profile
    assert user_account_file_page.file_category == UserAccountFilePage.FileCategoryChoices.CV

@pytest.mark.django_db
def test_user_account_file_page_string_representation():
    user = UserAccount.objects.create_user(email='testuser@gmail.com', password='valid_password')
    user_profile = UserProfile.objects.create(user=user)
    user_account_file_page = UserAccountFilePage.objects.create(
        user=user_profile,
        file_category=UserAccountFilePage.FileCategoryChoices.REPORT,
        file='path/to/cv.pdf' 
    )
    expected_str = f'REPORT of {user_profile}'
    assert str(user_account_file_page) == expected_str