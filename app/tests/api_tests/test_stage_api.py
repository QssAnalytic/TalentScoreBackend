from rest_framework.test import APITestCase
from django.urls import reverse
from app.models import Stage
from app.serializers.stage_serializers import StageParentListSerializer
from users.models import UserAccount

class AnswerTest(APITestCase):
    def setUp(self):
        self.user = UserAccount.objects.create_user(email="testuser@gmail.com", password="testpassword")

    def test_parent_stage_serializer_authenticated(self):
        url = reverse('parent-stage-api')
        stage1 = Stage.objects.create(stage_name="First Stage")
        stage2 = Stage.objects.create(stage_name="Second Stage")
        stages = Stage.objects.all()
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        expected_data = StageParentListSerializer(stages, many=True).data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)





