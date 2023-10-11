import base64
from django.http import JsonResponse
from rest_framework.views import APIView
from typing import Literal, Optional, TypedDict, Union
from decimal import Decimal
from django.db import transaction
from django.db.models import Prefetch, Q
from django.db import connection #DELETE
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.files.base import ContentFile
from users.models import ReportModel, UserAccount, UserAccountFilePage
from users.serializers.report_serializers import ReportUploadSerializer, GetReportSerializer
from users.serializers.user_account_file_serializers import UserAccountFilePage, UserAccountFilePageSerializer

from users.helpers.sync_user_helpers import *
from users.helpers.report_score_result import get_report_score
from users.utils.random_unique_key_utils import generate_unique_random_key
from users.utils.user_utils import round_to_non_zero


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
            return Response({'error': 'data structure is false'}, status=status.HTTP_404_NOT_FOUND)
        
        user = request.user
        
        report = ReportModel.objects.filter(user=user).first()
        if report != None:
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
        return Response("you must pass report", status=status.HTTP_400_BAD_REQUEST)
            



class SkillInfo(TypedDict):
    text: str
    result: str
    education_score: Union[float, None]
    language_score: Union[float, None]
    special_skills_score: Union[float, None]
    sport_score: Union[float, None]
    work_experiance_score: Union[float, None]
    program_score: Union[float, None]

from django.db import connection
from django.db import reset_queries


def database_debug(func):
    def inner_func(self, request, *args, **kwargs):
        reset_queries()
        results = func(self, request)
        query_info = connection.queries
        print('function_name: {}'.format(func.__name__))
        print('query_count: {}'.format(len(query_info)))
        queries = ['{}\n'.format(query['sql']) for query in query_info]
        print('queries: \n{}'.format(''.join(queries)))
        return results
    return inner_func

class ReportInfoAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user = request.user
        file_id = request.data.get("id")
        report_prefetch = Prefetch(
            'report',
            queryset=ReportModel.objects.all(),
            to_attr='report_data'
        )
        
        data = {
                "education": {
                    "score": None,
                    "color": None
                },
                "language": {
                    "score": None,
                    "color": None
                },
                "special_skills": {
                    "score": None,
                    "color": None
                },
                "sport": {
                    "score": None,
                    "color": None
                },
                "work_experience": {
                    "score": None,
                    "color": None
                },
                "program": {
                    "score": None,
                    "color": None
                },
                "date_created": None,
                "file_key": None
            }
        
        rep = UserAccountFilePage.objects.filter(Q(user=user) & Q(id=file_id)).prefetch_related(report_prefetch)
        
        for i in rep:
            
            data['education']['score'] = i.report_data[0].education_score
            data['education']['color'] = i.report_data[0].education_color
            data['language']['score'] = i.report_data[0].language_score
            data['language']['color'] = i.report_data[0].language_color
            data['special_skills']['score'] = i.report_data[0].special_skills_score
            data['special_skills']['color'] = i.report_data[0].special_skills_color
            data['sport']['score'] = i.report_data[0].sport_score
            data['sport']['color'] = i.report_data[0].sport_color
            data['work_experience']['score'] = i.report_data[0].work_experiance_score
            data['work_experience']['clolor'] = i.report_data[0].work_experiance_color
            data['program']['score'] = i.report_data[0].program_score
            data['program']['color'] = i.report_data[0].program_color
            data['file_key'] = i.report_data[0].file_key
        return Response({"data": data}, status=status.HTTP_200_OK)
    



class UserScoreAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = UserAccount.objects.filter(id=request.user.id).first()
        education_score = 1
        general_question_stage = None
        secondary_education_questions_stage = None
        olympiad_questions_stage = None
        experience_score = 1
        work_experience_questions_stage = None
        special_skills_score = 1
        special_skills_questions_stage = None
        special_skills_certificate_questions_stage = None
        language_score = 1
        language_skills_questions_stage = None
        programming_skills_score = 1
        program_questions_stage = None
        sport_score = 1
        sport_questions_stage = None
        sport2_questions_stage = None
        report_file_secret_key = generate_unique_random_key()
        # report = ReportModel.objects.select_related("report_file__user").filter(report_file__user=user).last()

        data: TypedDict[str, SkillInfo] = {'education':{'text': 'Education',"score":1, 'result':'limited'},
                'language': {'text': 'Language skills',"score":1,'result':'limited'},
                'special': {'text': 'Special talent','score':1, 'result':'limited'},
                'sport': {'text': 'Sport skills','score':1, 'result':'limited'},
                'work': {'text': 'Work experience','score':1, 'result':'limited'},
                'program': {'text': 'Program skills','score':1, 'result':'limited'}}
        user_info = request.data.get('user_info')

        
        for stage in user_info:
            
            if stage['name'] == "umumi-suallar":
                education_score = get_education_score(request)
                data['education']['score'] = round_to_non_zero(1-education_score)
                data['education']['result'] = get_report_score(education_score)
                # report.education_score = data['education']['score']
                
                general_question_stage = stage

            if stage['name'] == "is-tecrubesi-substage":
                experience_score = get_experience_score(stage)
                
                data['work']['score'] = round_to_non_zero(1-experience_score)
                data['work']['result'] = get_report_score(experience_score)
                # report.work_experiance_score =  data['work']['score']
                work_experience_questions_stage = stage

            if stage['name'] == "xususi-bacariqlar-substage":
                special_skills_score = get_skills_score(stage)
                data['special']['result'] = get_report_score(special_skills_score)
                data['special']['score'] = round_to_non_zero(1-special_skills_score)
                # report.special_skills_score = data['special']['score']
                special_skills_certificate_questions_stage = stage

            if stage['name'] == "dil-bilikleri-substage":
                language_score = get_language_score(stage)
                data['language']['result'] = get_report_score(language_score)
                data['language']['score'] = round_to_non_zero(1-language_score)
                # report.language_score = data['language']['score']
                language_skills_questions_stage = stage

            if stage['name'] == 'idman-substage':
                
                if stage['formData']['haveSport']['answer'] != 'Yoxdur':
                    
                    sport_stage:list = stage['formData']['sports']
                    sport_stage2 = None
                    for level in sport_stage:
                        if level['value']['answer'] == 'Peşəkar':
                            sport_stage2:list = list(filter(lambda x: x['name'] == 'idman-substage2', user_info))
                            sport_stage2:list = sport_stage2[0]['formData']['professionalSports']

                            break
                        
                    sport_score = get_sport_skills_score(sport_stage = sport_stage, sport_stage2=sport_stage2)

                    data['sport']['result'] = get_report_score(sport_score)
                    data['sport']['score'] = round_to_non_zero(1-sport_score)
                    # report.sport_score = data['sport']['score']
                    sport_questions_stage = stage
                else:
                    sport_questions_stage = stage

            if stage['name'] == "proqram-bilikleri-substage":
                programming_skills_score = get_programming_skills_score(stage)
                data['program']['result'] = get_report_score(programming_skills_score)
                data['program']['score'] = round_to_non_zero(1-programming_skills_score)
                
                # report.program_score = data['program']['score']
                program_questions_stage = stage

            if stage['name'] == 'idman-substage2':
                sport2_questions_stage = stage

            if stage['name'] == 'orta-texniki-ve-ali-tehsil-suallari':
                
                secondary_education_questions_stage = stage
            if stage['name'] == 'olimpiada-suallari':
                
                olympiad_questions_stage = stage
            if stage['name'] == 'xususi-bacariqlar-sertifikat-substage':
                special_skills_certificate_questions_stage = stage
        
        with transaction.atomic():
            user.report_test = True
            user.save()
            report = ReportModel.objects.create(user=user,
                                                general_questions = general_question_stage,
                                                secondary_education_questions = secondary_education_questions_stage,
                                                olympiad_questions=olympiad_questions_stage,
                                                work_experience_questions=work_experience_questions_stage,
                                                language_skills_questions=language_skills_questions_stage,
                                                extra_language_skills_questions = special_skills_questions_stage,
                                                special_skills_certificate_questions = special_skills_certificate_questions_stage,
                                                sport_questions = sport_questions_stage,
                                                sport2_questions = sport2_questions_stage,
                                                program_questions = program_questions_stage,
                                                education_score = data['education']['score'],
                                                language_score = data['language']['score'],
                                                special_skills_score = data['special']['score'],
                                                sport_score = data['sport']['score'],
                                                work_experiance_score = data['work']['score'],
                                                program_score=data['program']['score'],
                                                file_key = report_file_secret_key
                                            )
        
        return Response(
            {"data":data,"report_key": report_file_secret_key}
        )

