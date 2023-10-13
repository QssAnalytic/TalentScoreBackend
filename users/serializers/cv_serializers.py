from rest_framework import serializers
<<<<<<< HEAD

from users.models import ReportModel



class CVEducationSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = ReportModel
        fields = ("id", "general_questions", "secondary_education_questions", "olympiad_questions", "user")


    
=======
from users.models import ReportModel

class CvProgramQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportModel
        fields = ['id', 'user', 'program_questions']


        def validate(self, attrs):
            request = self.context['request']
            attrs['user'] = request.user
            return super().validate(attrs)
>>>>>>> 2e7f137678fb2f6b9ef7a2db0ed587f0fc771ee8
