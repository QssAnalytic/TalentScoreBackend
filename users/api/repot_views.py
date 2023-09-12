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


# class ReportUploadAPIView(APIView):
#     parser_classes = (MultiPartParser,)

#     def post(self, request, *args, **kwargs):
#         # print(request.data.get('report_file'))
#         req_data = request.data.get('report_file')
#         format, imgstr = req_data.split(';base64,') 
#         ext = format.split('/')[-1] 
#         cont_data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
#         # print(req_data)
#         try:
#           email = request.data.get('email')
#           user = UserAccount.objects.get(email=email)
#         except ReportModel.DoesNotExist:
#             return Response({'error': 'User not found with the provided email.'}, status=status.HTTP_404_NOT_FOUND)
#         # print(email,cont_data)

#         data = {'user': user.id, 'report_file': cont_data, 
#                 'education_score': 0.0,
#                 'language_score': 0.0,
#                 'special_skills_score': 0.0,
#                 'sport_score': 0.0,
#                 'work_experiance_score': 0.0,
#                 'program_score': 0.0,
#                 }

#         file_serializer = ReportUploadSerializer(data=data)

#         if file_serializer.is_valid():
#             file_serializer.save()
#             return Response(file_serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReportUploadAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            text_data = request.data.get('report_file')
            user = UserAccount.objects.first()  # Change this to fetch the user based on your logic
            general_questions = request.data.get('general_questions')
            secondary_education_questions = request.data.get('secondary_education_questions')
            olympiad_questions = request.data.get('olympiad_questions')
            work_experience_questions = request.data.get('work_experience_questions')
            special_skills_questions = request.data.get('special_skills_questions')
            language_skills_questions = request.data.get('language_skills_questions')
            special_skills_certificate_questions = request.data.get('special_skills_certificate_questions')
            sport_questions = request.data.get('sport_questions')
            program_questions = request.data.get('program_questions')
        
            # email = request.data.get('email')
            # user = UserAccount.objects.filter(email=email)       

            # Decode the base64 data and validate it
            bytes_data =base64.b64decode(text_data, validate=True)

            # Check if the first 4 bytes match the PDF signature
            if bytes_data[0:4] != b'%PDF':
                raise ValueError('Missing the PDF file signature')

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
                                 sport_questions = sport_questions,
                                 program_questions = program_questions)
           
            if user_account_file_serializer and report:
                user_account_file_serializer.save()
                report.save()
                return Response({'message': 'Report file uploaded successfully.'}, status=status.HTTP_201_CREATED)
            else:
                return Response(user_account_file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # def post(self, request, *args, **kwargs):
        
    #     try:
    #       email = request.data.get('email')
        #   user = UserAccount.objects.first()
    #     except ReportModel.DoesNotExist:
    #         return Response({'error': 'User not found with the provided email.'}, status=status.HTTP_404_NOT_FOUND)
    #     file_key = request.data.get('file_key')
    #     req_data = request.data.get('report_file')
    #     try:
            # format, imgstr = req_data.split(';base64,')
    #         ext = format.split('/')[-1]
    #         cont_data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
    #     except (ValueError, TypeError):
    #         return Response({'error': 'Invalid report file data.'}, status=status.HTTP_400_BAD_REQUEST)

    #     # Create a dictionary with the data to be saved
    #     data = {
    #         'user': user.id,
    #         'file_key': file_key,
    #         'file': cont_data,
    #         'file_category': 'REPORT',
    #     }

    #     # Serialize and save the data
    #     user_account_file_serializer = UserAccountFilePage(data=data)
    #     if user_account_file_serializer.is_valid():
    #         user_account_file_serializer.save()
    #         return Response({'message': 'Report file uploaded successfully.'}, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(user_account_file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
                        float_value = float(value)
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
    def get(self, request, username):
        user = (
            UserAccount.objects.filter(email=username)
            .only("email")
            .first()
        )
        print(user)
        education_score = 1
        experience_score = 1
        special_skills_score = 1
        language_score = 1
        programming_skills_score = 1
        sport_score = 2
        report = ReportModel.objects.filter(user=user).last()
        print(report.id)
        for stage in report.general_questions:
            if stage['name'] == "umumi-suallar":
                education_score = get_education_score(user)                
                report.education_score = education_score

        for stage in report.work_experience_questions:
            if stage['name'] == "is-tecrubesi-substage":
                experience_score = get_experience_score(stage)
                report.work_experiance_score = experience_score

        for stage in report.special_skills_questions:
            if stage['name'] == "xususi-bacariqlar-substage":
                special_skills_score = get_skills_score(stage)
                report.special_skills_score = special_skills_score

        for stage in report.language_skills_questions:
            if stage['name'] == "dil-bilikleri-substage":
                language_score = get_language_score(stage)     
                report.language_score = language_score

        for stage in report.sport_questions:
            if stage['name'] == "idman-substage":
                sport_score = get_sport_skills_score(stage)   
                report.sport_score = sport_score

        for stage in report.program_questions:
            if stage['name'] == "proqram-bilikleri-substage":
                programming_skills_score = get_programming_skills_score(stage)  
                report.program_score = programming_skills_score
        report.save()
                            
        
        return Response(
            {
                "special_skills_score": special_skills_score,
                "language_score": language_score,
                "experience_score": experience_score,
                "education_score": education_score,
                "programming_skills_score": programming_skills_score,
                "sport_score": sport_score
            }
        )