# class FileCategory(models.Model):
#     name = models.CharField(max_length=50)
#     file_count = models.PositiveIntegerField(default=0, editable=False)  # Field to store the file count
#     allows_multiple_files = models.BooleanField(default=False)
    
#     def __str__(self):
#         return self.name


# class UserFile(models.Model):
#     user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
#     category = models.ForeignKey(FileCategory, on_delete=models.CASCADE)
#     file = models.FileField(upload_to=user_file_upload_path, null=True, blank=True)
    
#     class Meta:
#         verbose_name = 'User File'
#         verbose_name_plural = 'User Files'
    
#     def __str__(self):
#         return f"{self.user.email} - {self.category}"
    
#     def save(self, *args, **kwargs):
#         # Increment the file count for the category when a new UserFile is created
#         if not self.pk: 
#             self.category.file_count += 1
#             self.category.save()
#         super().save(*args, **kwargs)
    
#     def delete(self, *args, **kwargs):
#         # Decrement the file count for the category when a UserFile is deleted
#         self.category.file_count -= 1
#         self.category.save()
#         super().delete(*args, **kwargs)

# class UserFiles(models.Model):
#     user = models.ForeignKey('users.UserAccount', models.CASCADE)
#     passport = models.FileField(upload_to='user-files/passports/', blank=True, null=True)
#     attestat9 = models.FileField(upload_to='user-files/attestat9/', blank=True, null=True)
#     attestat11 = models.FileField(upload_to='user-files/attestat11/', blank=True, null=True)
#     student_card = models.FileField(upload_to='user-files/student-cards/', blank=True, null=True)
#     bachelor_diplom = models.FileField(upload_to='user-files/diplom/bachelor/', blank=True, null=True)
#     master_diplom = models.FileField(upload_to='user-files/diplom/master/', blank=True, null=True)
#     phd_diplom = models.FileField(upload_to='user-files/diplom/phd/', blank=True, null=True)
#     olimp_sened = models.FileField(upload_to='user-files/olimpiad-docs/', blank=True, null=True)
#     ielts = models.FileField(upload_to='user-files/language-certificates/ielts/', blank=True, null=True)
#     toefl = models.FileField(upload_to='user-files/language-certificates/toefl/', blank=True, null=True) #10
#     other_lang_cert = models.FileField(upload_to='user-files/language-certificates/other/', blank=True, null=True)
#     experience_doc = models.FileField(upload_to='user-files/experience-docs/', blank=True, null=True)
#     program_cert = models.FileField(upload_to='user-files/program-certificates/', blank=True, null=True)
#     sport_cert = models.FileField(upload_to='user-files/sport-certificates/', blank=True, null=True)
#     special_skills_doc = models.FileField(upload_to='user-files/special-skills-docs/', blank=True, null=True)
    
#     class Meta:
#         verbose_name = 'User Files'
#         verbose_name_plural = 'User Files'
    
#     def __str__(self) -> str:
#         return self.user.email

#REPORT
# class ReportUploadAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         try:
#             text_data = request.data.get('report_file')
#             user = UserAccount.objects.first()  # Change this to fetch the user based on your logic
#             # general_questions = request.data.get('general_questions')
#             # secondary_education_questions = request.data.get('secondary_education_questions')
#             # olympiad_questions = request.data.get('olympiad_questions')
#             # work_experience_questions = request.data.get('work_experience_questions')
#             # special_skills_questions = request.data.get('special_skills_questions')
#             # language_skills_questions = request.data.get('language_skills_questions')
#             # special_skills_certificate_questions = request.data.get('special_skills_certificate_questions')
#             # sport_questions = request.data.get('sport_questions')
#             # program_questions = request.data.get('program_questions')
#             user_info = request.data.get("user_info")
#             for data in user_info:
#                 if data.get("name") =="umumi-suallar":
#                     general_questions = {'formData':data.get('formData')}
#                 if data.get("name") =="orta-texniki-ve-ali-tehsil-suallari":
#                     secondary_education_questions = {'formData':data.get('formData')}
#                 if data.get("name") =="olimpiada-suallar":
#                     olympiad_questions = {'formData':data.get('formData')}
#                 if data.get("name") =="is-tecrubesi-substage":
#                     work_experience_questions = {'formData':data.get('formData')}
#                 if data.get("name") =="xususi-bacariqlar-substage":
#                     special_skills_questions = {'formData':data.get('formData')}
#                 if data.get("name") =="dil-bilikleri-substage":
#                     language_skills_questions = {'formData':data.get('formData')}
#                 if data.get("name") == "elave-dil-bilikleri-substage":
#                     extra_language_skills_questions = {'formData':data.get('formData')}
#                 if data.get("name") == "xususi-bacariqlar-sertifikat-substage":
#                     special_skills_certificate_questions = {'formData':data.get('formData')}
#                 if data.get("name") == "idman-substage":
#                     sport_questions = {'formData':data.get('formData')}
#                 if data.get("name") == "proqram-bilikleri-substage":
#                     program_questions = {'formData':data.get('formData')}

            
#             # Decode the base64 data and validate it
#             bytes_data =base64.b64decode(text_data, validate=True)

#             # Check if the first 4 bytes match the PDF signature
#             # if bytes_data[0:4] != b'%PDF':
#             #     raise ValueError('Missing the PDF file signature')

#             # Create a ContentFile from the decoded bytes
#             pdf_file = ContentFile(bytes_data, name='output.pdf')
#             user_account_file_serializer = UserAccountFilePage(user_id=user.id, file=pdf_file, file_category='REPORT')
#             report = ReportModel(user=user,
#                                  report_file=user_account_file_serializer, 
#                                  general_questions=general_questions,
#                                  secondary_education_questions = secondary_education_questions,
#                                  olympiad_questions = olympiad_questions,
#                                  work_experience_questions = work_experience_questions,
#                                  special_skills_certificate_questions = special_skills_certificate_questions,
#                                  special_skills_questions = special_skills_questions,
#                                  language_skills_questions = language_skills_questions,
#                                  extra_language_skills_questions = extra_language_skills_questions,
#                                  sport_questions = sport_questions,
#                                  program_questions = program_questions)
#             # return Response({'message': 'Report file uploaded successfully.'}, status=status.HTTP_201_CREATED)
#             if user_account_file_serializer and report:
#                 user_account_file_serializer.save()
#                 report.save()
#                 return Response({'message': 'Report file uploaded successfully.'}, status=status.HTTP_201_CREATED)
#             else:
#                 return Response(user_account_file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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