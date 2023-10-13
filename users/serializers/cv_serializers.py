from rest_framework import serializers

from users.models import ReportModel



class CVEducationSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = ReportModel
        fields = ("id", "general_questions", "secondary_education_questions", "olympiad_questions", "user")


    