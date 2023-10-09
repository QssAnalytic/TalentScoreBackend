from users.serializers import RegistrationSerializer, LoginSerializer
from rest_framework.exceptions import ValidationError
from django.db.utils import IntegrityError
from users.models import UserAccount
from rest_framework.exceptions import AuthenticationFailed
from django.urls import reverse
from django.test import Client
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import time
import pytest

@pytest.mark.django_db
def test_register_email_field_format_validation():
    valid_data = {
        'email': 'valid.email@example.com',
        'password': 'password123',
        'password2': 'password123',
    }

    serializer = RegistrationSerializer(data=valid_data)
    assert serializer.is_valid() is True

    invalid_data = {
        'email': 'invalid-format',
        'password': 'password123',
        'password2': 'password123'
    }
    serializer= RegistrationSerializer(data=invalid_data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)

@pytest.mark.django_db
def test_register_missing_email():
    invalid_data = {
        'email': '',
        'password': 'password123',
        'password2': 'password123'
    }
    serializer = RegistrationSerializer(data=invalid_data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)

@pytest.mark.django_db
def test_register_password_equal_validation():
    invalid_data = {
        'password': 'password123',
        'password2': 'password12345',
    }

    serializer = RegistrationSerializer(data=invalid_data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)

@pytest.mark.django_db
def test_register_missing_confirm_password_validation():
    invalid_data = {
        'email': 'valid.email@example.com',
        'password': 'password123',
    }
    serializer = RegistrationSerializer(data=invalid_data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)

@pytest.mark.django_db
def test_try_for_second_register_validation():
    valid_data = {
        'first_name' :'Jhon',
        'last_name' :'Doe',
        'email' :'Jhon200@gmail.com',
        'birth_date':'2023-05-25',
        'gender':'Male',
        'native_language':'English',
        'country':'UK',
        'email': 'valid.email@example.com',
        'password': 'password123',
        'password2': 'password123',
    }
    serializer = RegistrationSerializer(data=valid_data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    with pytest.raises(ValidationError):
        serializer = RegistrationSerializer(data=valid_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

@pytest.mark.django_db
def test_valid_registration():
    registration_data = {
        'email': 'newuser@gmail.com',
        'first_name': 'John',
        'last_name': 'Doe',
        'birth_date': '1990-01-01',
        'gender': 'Male',
        'native_language': 'English',
        'country': 'USA',
        'password': 'valid_password',
        'password2': 'valid_password',
    }
    client = Client()
    response = client.post(reverse('register'), data=registration_data, follow=True)
    assert response.status_code == status.HTTP_200_OK
    assert 'Registered!' in response.content.decode('utf-8')
    user = UserAccount.objects.get(email='newuser@gmail.com')
    assert user is not None
    assert user.email == 'newuser@gmail.com'

@pytest.mark.django_db
def test_user_not_valid_email_format_login():
    invalid_data = {
        'email' : 'invalid-format',
        'password' : 'password123'
    }
    serializer = LoginSerializer(data=invalid_data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)

# @pytest.mark.django_db
# def test_user_not_valid_password_format__login():
#     invalid_data = {
#         'email' : 'example@gmail.com',
#         'password' : '123'
#     }
#     serializer = LoginSerializer(data=invalid_data)
#     with pytest.raises(ValidationError):
#         serializer.is_valid(raise_exception=True)

@pytest.mark.django_db
def test_user_email_missing__login():
    user = UserAccount.objects.create(
                                    email='valid.email@example.com',
                                    password='password1234')
    invalid_data = {
        'password' : 'password1234'
    }
    serializer = LoginSerializer(data=invalid_data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)

@pytest.mark.django_db
def test_user_missing_password_login():
    user = UserAccount.objects.create(
                                    email='valid.email@example.com',
                                    password='password1234')
    invalid_data = {
        'email' : 'valid.email@example.com'
    }
    serializer = LoginSerializer(data=invalid_data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)
        serializer.save()

@pytest.mark.django_db
def test_user_valid_login():
    user = UserAccount.objects.create(
                                    email='valid.email@example.com',
                                    password='password1234')
    valid_data = {
        'email': user.email,
        'password': user.password
    }
    login_serializer = LoginSerializer(data=valid_data)
    assert login_serializer.is_valid() is True

@pytest.mark.django_db
def test_login_view_with_valid_credentials(client):
    UserAccount.objects.create_user(email='valid.email@example.com', password='valid_password')
    response = client.post('/user/login/', data={'email': 'valid.email@example.com', 'password': 'valid_password'})
    assert response.status_code == 200

@pytest.mark.django_db
def test_login_view_with_invalid_credentials(client):
    response = client.post('/user/login/', data={'email': 'invalid.email@example.com', 'password': 'invalid_password'})
    assert response.status_code == 401

@pytest.mark.django_db
def test_valid_login_authentication():
    user = UserAccount.objects.create_user(email='testuser@gmail.com', password='valid_password')
    login_data = {
        'email': 'testuser@gmail.com',
        'password': 'valid_password'
    }
    client = Client()
    response = client.post(reverse('login'), data=login_data, follow=True)
    assert response.status_code == status.HTTP_200_OK
    assert user.is_authenticated

@pytest.mark.django_db
def test_invalid_login_authentication():
    login_data = {
        'email': 'testuser',
        'password': 'invalid_password'
    }
    client = Client()
    response = client.post(reverse('login'), data=login_data)
    assert not response.wsgi_request.user.is_authenticated

@pytest.mark.django_db
def test_login_view_cookies_and_tokens():
    user = UserAccount.objects.create_user(email='testuser@gmail.com', password='valid_password')
    login_data = {
        'email': 'testuser@gmail.com',
        'password': 'valid_password'
    }
    client = Client()
    response = client.post(reverse('login'), data=login_data, follow=True)
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.cookies
    assert 'refresh' in response.cookies
    refresh_token = response.cookies['refresh'].value
    refresh_token_obj = RefreshToken(refresh_token)
    access_token_obj = refresh_token_obj.access_token
    assert access_token_obj['user_id'] == user.id
    assert access_token_obj['exp'] > int(time.time())
    assert user.is_authenticated

# from rest_framework_simplejwt.tokens import RefreshToken
# from django.conf import settings
# @pytest.mark.django_db
# def test_user_logout():
#     user = UserAccount.objects.create_user(email='testuser@gmail.com', password='valid_password')
#     client = Client()
#     client.login(email='testuser@gmail.com', password='valid_password')
#     assert client.session['_auth_user_id'] == str(user.id)
#     refresh_token = RefreshToken.for_user(user)
#     access_token = str(refresh_token.access_token)
#     refresh_token = str(refresh_token)
#     logout_url = reverse('logout')
#     client.cookies[settings.SIMPLE_JWT["AUTH_COOKIE"]] = access_token
# #     client.cookies[settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"]] = refresh_token
#     response = client.post(logout_url, follow=True)
#     assert response.status_code == status.HTTP_200_OK
#     assert not response.wsgi_request.user.is_authenticated