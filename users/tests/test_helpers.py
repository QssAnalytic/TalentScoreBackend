import pytest
from users.helpers.sync_user_helpers import (get_education_score, 
                                            get_experience_score,
                                            get_language_score, 
                                            get_programming_skills_score, 
                                            get_sport_skills_score)
from users.tests.test_users_report_views_api import test_data
from django.http import HttpRequest

@pytest.mark.django_db
def test_education_score():
    request = HttpRequest()
    request.data = test_data
    result = get_education_score(request)
    expected_result = round(1- result, 9)
    print(expected_result)
    assert expected_result == 0.4780448

@pytest.mark.django_db
def test_experience_score():
    request = HttpRequest()
    request = test_data['user_info']
    for data in request:
        if data['name'] == 'is-tecrubesi-substage':
            result = get_experience_score(data)
            assert 0.496 == 1-result

@pytest.mark.django_db
def test_language_score():
    request = HttpRequest()
    request = test_data['user_info']
    for data in request:
        if data['name'] == 'Language skills':
            result = get_language_score(data)
            assert 0 == 1-result

@pytest.mark.django_db
def test_sport_score():
    request = HttpRequest()
    request = test_data['user_info']
    for data in request:
        if data['name'] == 'idman-substage' and data['name'] == 'idman-substage2':
            result = get_sport_skills_score(data)
            assert 0.9999946 == 1-result

@pytest.mark.django_db
def test_program_score():
    request = HttpRequest()
    request = test_data['user_info']
    for data in request:
        if data['name'] == 'proqram-bilikleri-substage':
            result = get_programming_skills_score(data)
            assert 1 == 1-result