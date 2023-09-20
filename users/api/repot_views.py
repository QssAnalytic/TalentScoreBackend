import base64
from rest_framework.views import APIView
from typing import Literal, Optional, TypedDict, Union
from decimal import Decimal
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework import status
from rest_framework.response import Response
from django.core.files.base import ContentFile
from users.models import ReportModel, UserAccount, UserAccountFilePage
from users.serializers.report_serializers import ReportUploadSerializer
from users.serializers.user_account_file_serializers import UserAccountFilePage
from users.helpers.sync_user_helpers import *
from users.helpers.report_score_result import get_report_score
from users.utils.random_unique_key_utils import generate_unique_random_key
class ReportUploadAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            text_data = request.data.get('report_file')
            user = UserAccount.objects.first()  # Change this to fetch the user based on your logic
            # general_questions = request.data.get('general_questions')
            # secondary_education_questions = request.data.get('secondary_education_questions')
            # olympiad_questions = request.data.get('olympiad_questions')
            # work_experience_questions = request.data.get('work_experience_questions')
            # special_skills_questions = request.data.get('special_skills_questions')
            # language_skills_questions = request.data.get('language_skills_questions')
            # special_skills_certificate_questions = request.data.get('special_skills_certificate_questions')
            # sport_questions = request.data.get('sport_questions')
            # program_questions = request.data.get('program_questions')
            user_info = request.data.get("user_info")
            print(user_info)
            print(5)
            for data in user_info:
                if data.get("name") =="umumi-suallar":
                    general_questions = {'formData':data.get('formData')}
                if data.get("name") =="orta-texniki-ve-ali-tehsil-suallari":
                    secondary_education_questions = {'formData':data.get('formData')}
                if data.get("name") =="olimpiada-suallar":
                    olympiad_questions = {'formData':data.get('formData')}
                if data.get("name") =="is-tecrubesi-substage":
                    work_experience_questions = {'formData':data.get('formData')}
                if data.get("name") =="xususi-bacariqlar-substage":
                    special_skills_questions = {'formData':data.get('formData')}
                if data.get("name") =="dil-bilikleri-substage":
                    language_skills_questions = {'formData':data.get('formData')}
                if data.get("name") == "elave-dil-bilikleri-substage":
                    extra_language_skills_questions = {'formData':data.get('formData')}
                if data.get("name") == "xususi-bacariqlar-sertifikat-substage":
                    special_skills_certificate_questions = {'formData':data.get('formData')}
                if data.get("name") == "idman-substage":
                    sport_questions = {'formData':data.get('formData')}
                if data.get("name") == "proqram-bilikleri-substage":
                    program_questions = {'formData':data.get('formData')}

            print(user_info)
            # Decode the base64 data and validate it
            bytes_data =base64.b64decode(text_data, validate=True)

            # Check if the first 4 bytes match the PDF signature
            # if bytes_data[0:4] != b'%PDF':
            #     raise ValueError('Missing the PDF file signature')

            # Create a ContentFile from the decoded bytes
            pdf_file = ContentFile(bytes_data, name='output.pdf')
            user_account_file_serializer = UserAccountFilePage(user_id=user.id, file=pdf_file, file_category='REPORT')
            report = ReportModel(user=user,
                                 report_file=user_account_file_serializer, 
                                 general_questions=general_questions,
                                 secondary_education_questions = secondary_education_questions,
                                 olympiad_questions = olympiad_questions,
                                 work_experience_questions = work_experience_questions,
                                 special_skills_certificate_questions = special_skills_certificate_questions,
                                 special_skills_questions = special_skills_questions,
                                 language_skills_questions = language_skills_questions,
                                 extra_language_skills_questions = extra_language_skills_questions,
                                 sport_questions = sport_questions,
                                 program_questions = program_questions)
            # return Response({'message': 'Report file uploaded successfully.'}, status=status.HTTP_201_CREATED)
            if user_account_file_serializer and report:
                user_account_file_serializer.save()
                report.save()
                return Response({'message': 'Report file uploaded successfully.'}, status=status.HTTP_201_CREATED)
            else:
                return Response(user_account_file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
    def post(self, request):
        # user = (
        #     UserAccount.objects.filter(email=email)
        #     .only("email")
        #     .first()
        # )
        education_score = 1
        experience_score = 1
        special_skills_score = 1
        language_score = 1
        programming_skills_score = 1
        sport_score = 1
        # report = ReportModel.objects.filter(user=user).last()
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
                data['education']['score'] = education_score
                data['education']['result'] = get_report_score(education_score)

                # report.education_score = education_score

            if stage['name'] == "is-tecrubesi-substage":
                experience_score = get_experience_score(stage)
                data['work']['score'] = experience_score
                data['work']['result'] = get_report_score(experience_score)
                # report.work_experiance_score = experience_score

            if stage['name'] == "xususi-bacariqlar-substage":
                special_skills_score = get_skills_score(stage)
                data['special']['result'] = get_report_score(special_skills_score)
                data['special']['score'] = special_skills_score
                # report.special_skills_score = special_skills_score

            if stage['name'] == "dil-bilikleri-substage":
                language_score = get_language_score(stage)
                data['language']['result'] = get_report_score(language_score)
                data['language']['score'] = language_score
                # report.language_score = language_score

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
                data['sport']['score'] = sport_score
                # report.sport_score = sport_score

            if stage['name'] == "proqram-bilikleri-substage":
                programming_skills_score = get_programming_skills_score(stage)
                data['program']['result'] = get_report_score(programming_skills_score)
                data['program']['score'] = programming_skills_score
                # report.program_score = programming_skills_score
            # # report.save()


        return Response(
            {"data":data,"report_key": generate_unique_random_key()}
        )