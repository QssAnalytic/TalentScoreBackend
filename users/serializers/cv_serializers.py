from rest_framework import serializers
from users.models import UserProfile

class CvProgramQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'program_questions']


        def validate(self, attrs):
            request = self.context['request']
            attrs['user'] = request.user
            return super().validate(attrs)
        

class CVEducationSerializer(serializers.ModelSerializer):


    class Meta:
        model = UserProfile
        fields = ("id", "general_questions", "secondary_education_questions", "olympiad_questions", "user")
