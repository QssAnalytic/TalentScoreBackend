from rest_framework import serializers
from users.models import ReportModel

class CvProgramQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportModel
        fields = ['id', 'user', 'program_questions']


        def validate(self, attrs):
            request = self.context['request']
            attrs['user'] = request.user
            return super().validate(attrs)
        

class CVEducationSerializer(serializers.ModelSerializer):


    class Meta:
        model = ReportModel
        fields = ("id", "general_questions", "secondary_education_questions", "olympiad_questions", "user")
