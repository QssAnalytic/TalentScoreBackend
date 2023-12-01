from rest_framework import serializers
from app import models


class SubAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SubAnswer 
        exclude = ["id", "answer", "sub_answer_weight"]

class AnswerListSerializer(serializers.ModelSerializer):
    subanswers = SubAnswerSerializer(many=True, read_only=True)
    #stage_fit = serializers.CharField(source = 'get_stage_slug')
    class Meta:
        model = models.Answer
        exclude = ["questionIdd", "created_at", "updated_at", "stage_fit", "answer_weight_for_hashing"]








