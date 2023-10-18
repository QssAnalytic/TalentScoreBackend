from rest_framework import serializers
from users.models import ReportModel

class CVInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportModel # Update to UserPRofile model
        fields = ('general_questions', 'work_experience_questions', 'program_questions')
