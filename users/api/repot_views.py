import base64
from rest_framework.views import APIView
from typing import Literal, Optional, TypedDict, Union
from decimal import Decimal
from django.db import transaction
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.files.base import ContentFile
from users.models import ReportModel, UserAccount, UserAccountFilePage
from users.serializers.report_serializers import ReportUploadSerializer
from users.serializers.user_account_file_serializers import UserAccountFilePage, UserAccountFilePageSerializer

from users.helpers.sync_user_helpers import *
from users.helpers.report_score_result import get_report_score
from users.utils.random_unique_key_utils import generate_unique_random_key

class ReportUploadAPIView(APIView):
    # parser_classes = (MultiPartParser,)
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        if 'report_file' not in request.data:
            return Response({'error': 'Missing report_file field in request data.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            req_data = request.data.get('report_file')
            format, imgstr = req_data.split(';base64,')
            ext = format.split('/')[-1]
            cont_data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        except:
            return Response({'error': 'User not found with the provided email.'}, status=status.HTTP_404_NOT_FOUND)
        
        user = request.user
        report = ReportModel.objects.get(user=user)
        data_to_serialize = {
            'user': user.id,
            'file': cont_data,
            'file_category': 'REPORT',
        }
        file_serializer = UserAccountFilePageSerializer(data=data_to_serialize)
        with transaction.atomic():
            if file_serializer.is_valid():
                report.report_file = file_serializer.save()
                report.save()
                return Response({'message': "file uploaded"}, status=status.HTTP_201_CREATED)
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SkillInfo(TypedDict):
    text: str
    result: str
    education_score: Union[float, None]
    language_score: Union[float, None]
    special_skills_score: Union[float, None]
    sport_score: Union[float, None]
    work_experiance_score: Union[float, None]
    program_score: Union[float, None]


class ReportInfoAPIView(APIView):
    def get(self, request, *args, **kwargs):
        rep = ReportModel.objects.select_related('user').filter(user__email='tami@mail.ru').defer('report_file').values()
        data: TypedDict[str, SkillInfo] = {'education':{'text': 'Education', 'result':''}, 
                'language': {'text': 'Language skills', 'result':''},
                'special': {'text': 'Special talent', 'result':''},
                'sport': {'text': 'Sport skills', 'result':''},
                'work': {'text': 'Work experience', 'result':''},
                'program': {'text': 'Program skills', 'result':''}}
        rep_data = rep[0]

        for key, value in rep_data.items():
            for d_key, d_value in data.items():
                if d_key in key:
                    if isinstance(value, Decimal):
                        # float_value = float(value)
                        float_value = value
                        result = ''
                        if 1 <= float_value <= 20:
                            result = 'limited'
                        elif 21 <= float_value <= 40:
                            result = 'decent'
                        elif 41 <= float_value <= 60:
                            result = 'moderate'
                        elif 61 <= float_value <= 80:
                            result = 'solid'
                        elif 81 <= float_value <= 100:
                            result = 'extensive'
                        d_value[key] = float_value
                        d_value['result'] = result
                    else:
                        d_value[key] = value
            
        return Response({"data":data}, status=status.HTTP_200_OK)


class UserScoreAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = UserAccount.objects.filter(id=request.user.id).first()
        education_score = 1
        experience_score = 1
        special_skills_score = 1
        language_score = 1
        programming_skills_score = 1
        sport_score = 1
        # report = ReportModel.objects.select_related("report_file__user").filter(report_file__user=user).last()
        report = ReportModel.objects.create(user=user)
        data: TypedDict[str, SkillInfo] = {'education':{'text': 'Education',"score":1, 'result':''},
                'language': {'text': 'Language skills',"score":1,'result':''},
                'special': {'text': 'Special talent','score':1, 'result':''},
                'sport': {'text': 'Sport skills','score':1, 'result':''},
                'work': {'text': 'Work experience','score':1, 'result':''},
                'program': {'text': 'Program skills','score':1, 'result':''}}
        user_info = request.data.get('user_info')


        for stage in user_info:
            if stage['name'] == "umumi-suallar":
                education_score = get_education_score(request)
                data['education']['score'] = 1-education_score
                data['education']['result'] = get_report_score(education_score)
                report.education_score = education_score
                report.general_questions = stage

            if stage['name'] == "is-tecrubesi-substage":
                experience_score = get_experience_score(stage)
                data['work']['score'] = 1-experience_score
                data['work']['result'] = get_report_score(experience_score)
                report.work_experiance_score = experience_score
                report.work_experience_questions = stage

            if stage['name'] == "xususi-bacariqlar-substage":
                special_skills_score = get_skills_score(stage)
                data['special']['result'] = get_report_score(special_skills_score)
                data['special']['score'] = 1-special_skills_score
                report.special_skills_score = special_skills_score
                report.special_skills_questions = stage

            if stage['name'] == "dil-bilikleri-substage":
                language_score = get_language_score(stage)
                data['language']['result'] = get_report_score(language_score)
                data['language']['score'] = 1-language_score
                report.language_score = language_score
                report.language_skills_questions = stage

            if stage['name'] == 'idman-substage':
                sport_stage:list = stage['formData']['sports']
                sport_stage2 = None
                for level in sport_stage:
                    if level['value']['answer'] == 'Peşəkar':
                        sport_stage2:list = list(filter(lambda x: x['name'] == 'idman-substage2', user_info))
                        sport_stage2:list = sport_stage2[0]['formData']['professionalSports']
                        
                        break

                sport_score = get_sport_skills_score(sport_stage = sport_stage, sport_stage2=sport_stage2)

                data['sport']['result'] = get_report_score(sport_score)
                data['sport']['score'] = 1-sport_score
                report.sport_score = sport_score
                report.sport_questions = stage

            if stage['name'] == "proqram-bilikleri-substage":
                programming_skills_score = get_programming_skills_score(stage)
                data['program']['result'] = get_report_score(programming_skills_score)
                data['program']['score'] = 1-programming_skills_score
                report.program_score = programming_skills_score
                report.program_questions = stage

            if stage['name'] == 'idman-substage2':
                report.sport2_questions = stage

            if stage['name'] == 'orta-texniki-ve-ali-tehsil-suallari':
                education_stage = stage
                report.secondary_education_questions = stage
            if stage['name'] == 'olimpiada-suallari':
                olimpia_stage = stage
                report.olympiad_questions = stage
            if stage['name'] == 'xususi-bacariqlar-sertifikat-substage':
                report.special_skills_certificate_questions = stage
            report.save()


        return Response(
            {"data":data,"report_key": generate_unique_random_key()}
        )