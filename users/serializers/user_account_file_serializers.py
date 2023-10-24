from rest_framework import serializers

from users.models import UserAccountFilePage

# class ReportUploadSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ReportModel
#         fields = "__all__"
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
class UserAccountFilePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccountFilePage
        fields = ("id", "user","file", "file_category")

