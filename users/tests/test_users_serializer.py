from users.models import ReportModel
from users.serializers.user_serializers import ReportSerializer
import pytest


@pytest.mark.django_db
def test_fields_in_serializer():
    serializer = ReportSerializer()
    assert 'general_questions' in serializer.fields
    assert 'secondary_education_questions' in serializer.fields
    



@pytest.mark.django_db
def test_report_serializer():
    data = {"general_questions": "value1", "field2": "value2"}
    serializer = ReportSerializer(data=data)
    assert serializer.is_valid()


@pytest.mark.django_db
def test_create_report():
    data = {"general_questions": "value1", "field2": "value2"} 
    serializer = ReportSerializer(data=data)
    assert serializer.is_valid()
    report_instance = serializer.save()
    assert isinstance(report_instance, ReportModel)


@pytest.mark.django_db
def test_update_report():
    report_instance = ReportModel.objects.create(general_questions="value1", secondary_education_questions="value2")
    data = {"general_questions": "new_value_for_general_questions", "secondary_education_questions": "new_value_for_secondary_education_questions"}
    serializer = ReportSerializer(report_instance, data=data)  
    assert serializer.is_valid()
    updated_report_instance = serializer.save()
    updated_report_instance.refresh_from_db()
    assert updated_report_instance.general_questions == "new_value_for_general_questions"
    assert updated_report_instance.secondary_education_questions == "new_value_for_secondary_education_questions"
