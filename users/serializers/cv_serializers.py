from rest_framework import serializers
from users.models import ReportModel, Resume

class CVInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportModel # Update to UserPRofile model
        fields = ('general_questions', 'work_experience_questions', 'program_questions')


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = "__all__"

class GetResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        exclude = ["id", "resume_file"]