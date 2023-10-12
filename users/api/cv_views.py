import math, base64, openai, environ, json
from rest_framework.views import APIView
from users.models import ReportModel
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
env = environ.Env()
environ.Env.read_env()

class JobTitleAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        openai.api_key = env("api_key")
        
        
        def generate_summary_job_title(i = 0, print_response = True, temperature = 0.7):
    
            report_data = ReportModel.objects.filter(user=request.user).first()
            ######################
            ##  Create Prompt   ##
            ######################

            umumi_suallar = report_data.general_questions
            orta_texniki_suallar = report_data.secondary_education_questions
            olimpiada_suallar = report_data.olympiad_questions
            is_tecrubesi = report_data.work_experience_questions
            xususi_bacariqlar = report_data.special_skills_questions
            dil_bilikleri = report_data.language_skills_questions
            idman_substage = report_data.sport_questions
            proqram_bilikleri_substage = report_data.program_questions
            idman_substage_2 = report_data.sport2_questions

            prompt = ''
            # prompt += f'Hello, my name is {df.iloc[i].name_surname}. I am {df.iloc[i].age} years old. I am {df.iloc[i].gender}. '
            prompt += f"I have education level of {umumi_suallar['formData']['education']['answer']}. "
            to_be_form =   'were' if umumi_suallar['formData']['education']['answer'] != 'Orta təhsil' else 'are'
            prompt += f"My high school grades {to_be_form} excellent. " if umumi_suallar['formData']['educationGrant']['answer'] == 'Əlaçı' else f"My high school grades {to_be_form} competent. " if umumi_suallar['formData']['educationGrant']['answer'] == 'Zərbəçi' else f"My high school grades {to_be_form} average. "
            prompt += "" if umumi_suallar['formData']['education']['answer'] == 'Orta təhsil' else f"Here is detailed information about my education: {orta_texniki_suallar['formData']['education']}. "
            prompt += "" if olimpiada_suallar['formData']['wonOlympics']['answer'] == 'Xeyr' else f" I have participated in {olimpiada_suallar['formData']['subjectOlympiad']['answer']} subject which was in {olimpiada_suallar['formData']['highestOlympiad']['answer']} level and got {olimpiada_suallar['formData']['rankOlympiad']['answer']}. "
            prompt += "I have had no work experience. " if is_tecrubesi['formData']['haveJobExperience']['answer'] == 'Xeyr' else f"Here is detailed information about my work experience: {is_tecrubesi['formData']['experiences']}. "
            prompt += f"I have no other language knowledge" if dil_bilikleri['formData']['haveLanguageSkills']['answer'] != "Var" else f"""Here is detailed information about my language knowledge: {dil_bilikleri['formData']['languageSkills']}. """

            if idman_substage_2 != None:
                prompt += "" if idman_substage['formData']['haveSport']['answer'] != 'Var' else f"Here is detailed information about my sport background {idman_substage['formData']} and my achievements {idman_substage_2['formData']['professionalSports']}. "
            else:
                prompt += "" if idman_substage['formData']['haveSport']['answer'] != 'Var' else f"Here is detailed information about my sport background {idman_substage['formData']}. "
            prompt += "" if xususi_bacariqlar['formData']['haveSpecialSkills']['answer'] != 'Var' else f"Here is detailed information about my background on other skills: {xususi_bacariqlar['formData']['skills']} + {xususi_bacariqlar['formData']['specialSkills']}. "

            prompt += "" if proqram_bilikleri_substage['formData']['haveProgramSkills']['answer'] != 'Var' else f"Here is detailed information about my background on programming skills: {proqram_bilikleri_substage['formData']['programSkills']} and programs {proqram_bilikleri_substage['formData']['whichProgram']}. "
            prompt = prompt.replace("'", "").replace('"', "").replace("{", "").replace("}", "").replace("_", " ").replace('\n', " ").replace('                         ', " ")

            ################################
            ##  Assign test system info   ##
            ################################
            testing_system_info = '''
                                Having excellent grades in high school means having all grades of best grades (such as A). Having competent grades in high school means having all grades of best and good grades (such as A and B).
                                Having average grades in high school means having different grades - A, B, C, D, etc.
                                DIM is an abbreviation for State Examination Center in Azerbaijan, where most students choose this center's exams to get admission for high educational institutes.
                                Bachelor's Education entrance exam points range is 0-700. Having high score is associated with high level of industriousness and may signal higher level of IQ.
                                Score range of 600-700 is considered exceptionally good and only 5-10% of students can score that much. To be in this interval, students should score at least 80% in each test subjects.
                                Score range of 500-600 is considered good and only 10-15% of students can score in this interval. To be in this interval, students should score at least 60%-70% in each test subjects.
                                Score range of 350-500 is considered normal and only 20-25% of students can score in this interval.
                                Score range of 200-350 is considered bad and range of 0-200 is considered that the person has failed to demonstrate good score.

                                Master's Education entrance exam score range is 0-100. Having high score is associated with high level of industriousness and may signal higher level of IQ.
                                Score range of 80-100 is considered exceptionally good and only 5-10% of students can achieve this.
                                Score range of 50-80  is considered good and only 10-15% of students can score this.
                                Score range of 40-50  is considered normal and only 20-25% of students can score this.
                                Score range of 0-40   is considered bad and it means that the person has failed.

                                PhD Education entrance exam score range is 0-100. Having high score is associated with high level of industriousness and may signal higher level of IQ.
                                Score range of 80-100 is considered exceptionally good and only 5-10% of students can achieve this.
                                Score range of 50-80  is considered good and only 10-15% of students can score this.
                                Score range of 30-50  is considered normal and only 20-25% of students can score this.
                                Score range of 0-30   is considered bad and it means that the person has failed.'''


            # Example OpenAI Python library request
            # desired_job_vacancy = df.iloc[i].desired_job
            # x = '' if desired_job_vacancy else "I want to apply for the position: " + desired_job_vacancy
            MODEL = "gpt-3.5-turbo"
            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": f"""You are a helpful AI tool which can create Job Title of people (such as 'Manager', 'Data Scientist') for CV professionally.
                                                    The user may give extra prompt such as 'I want to apply for this job', etc.
                                                    User data is this: {prompt}. You may also need to know that {testing_system_info}.
                                                    The response you give will be written into CV pdf file, so that do not indicate any redundant and irrelevant things in your response.
                                                    """},
                    {"role": "user", "content": f"""Please create me a Job title for me based on the information of me professionally and in a formal way.
                                                 The response  will be automatically written to CV. Do not indicate things like 'Job title:' or date ranges, company name, etc. Write only one job.
                                                 """},
                    # {"role": "assistant", "content": "Who's there?"},
                    # {"role": "user", "content": "Orange."},
                ],
                temperature = temperature,
                # max_tokens = 100
            )

            # response.choices[0].message.content

               
            return response.choices[0].message.content
        sample_job_title = generate_summary_job_title()
        return Response({"sample_job_title": sample_job_title})

class SummryPromptAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        openai.api_key = env("api_key")

        def generate_cv_summary(i = 1,  print_response = True, 
                               temperature = 0.7):
            report_data = ReportModel.objects.filter(user=request.user).first()
            ######################
            ##  Create Prompt   ##
            ######################

            umumi_suallar = report_data.general_questions
            orta_texniki_suallar = report_data.secondary_education_questions
            olimpiada_suallar = report_data.olympiad_questions
            is_tecrubesi = report_data.work_experience_questions
            xususi_bacariqlar = report_data.special_skills_questions
            dil_bilikleri = report_data.language_skills_questions
            idman_substage = report_data.sport_questions
            proqram_bilikleri_substage = report_data.program_questions
            idman_substage_2 = report_data.sport2_questions

            prompt = ''
            # prompt += f'Hello, my name is {df.iloc[i].name_surname}. I am {df.iloc[i].age} years old. I am {df.iloc[i].gender}. '
            prompt += f"I have education level of {umumi_suallar['formData']['education']['answer']}. "
            to_be_form =   'were' if umumi_suallar['formData']['education']['answer'] != 'Orta təhsil' else 'are'
            prompt += f"My high school grades {to_be_form} excellent. " if umumi_suallar['formData']['educationGrant']['answer'] == 'Əlaçı' else f"My high school grades {to_be_form} competent. " if umumi_suallar['formData']['educationGrant']['answer'] == 'Zərbəçi' else f"My high school grades {to_be_form} average. "
            prompt += "" if umumi_suallar['formData']['education']['answer'] == 'Orta təhsil' else f"Here is detailed information about my education: {orta_texniki_suallar['formData']['education']}. "
            prompt += "" if olimpiada_suallar['formData']['wonOlympics']['answer'] == 'Xeyr' else f" I have participated in {olimpiada_suallar['formData']['subjectOlympiad']['answer']} subject which was in {olimpiada_suallar['formData']['highestOlympiad']['answer']} level and got {olimpiada_suallar['formData']['rankOlympiad']['answer']}. "
            prompt += "I have had no work experience. " if is_tecrubesi['formData']['haveJobExperience']['answer'] == 'Xeyr' else f"Here is detailed information about my work experience: {is_tecrubesi['formData']['experiences']}. "
            prompt += f"I have no other language knowledge" if dil_bilikleri['formData']['haveLanguageSkills']['answer'] != "Var" else f"""Here is detailed information about my language knowledge: {dil_bilikleri['formData']['languageSkills']}. """
            if idman_substage_2 != None:
                prompt += "" if idman_substage['formData']['haveSport']['answer'] != 'Var' else f"Here is detailed information about my sport background {idman_substage['formData']} and my achievements {idman_substage_2['formData']['professionalSports']}. "
            else:
                prompt += "" if idman_substage['formData']['haveSport']['answer'] != 'Var' else f"Here is detailed information about my sport background {idman_substage['formData']}. "
            prompt += "" if xususi_bacariqlar['formData']['haveSpecialSkills']['answer'] != 'Var' else f"Here is detailed information about my background on other skills: {xususi_bacariqlar['formData']['skills']} + {xususi_bacariqlar['formData']['specialSkills']}. "

            prompt += "" if proqram_bilikleri_substage['formData']['haveProgramSkills']['answer'] != 'Var' else f"Here is detailed information about my background on programming skills: {proqram_bilikleri_substage['formData']['programSkills']} and programs {proqram_bilikleri_substage['formData']['whichProgram']}. "
            prompt = prompt.replace("'", "").replace('"', "").replace("{", "").replace("}", "").replace("_", " ").replace('\n', " ").replace('                         ', " ")

            ################################
            ##  Assign test system info   ##
            ################################
            testing_system_info = '''
                                Having excellent grades in high school means having all grades of best grades (such as A). Having competent grades in high school means having all grades of best and good grades (such as A and B).
                                Having average grades in high school means having different grades - A, B, C, D, etc.
                                DIM is an abbreviation for State Examination Center in Azerbaijan, where most students choose this center's exams to get admission for high educational institutes.
                                Bachelor's Education entrance exam points range is 0-700. Having high score is associated with high level of industriousness and may signal higher level of IQ.
                                Score range of 600-700 is considered exceptionally good and only 5-10% of students can score that much. To be in this interval, students should score at least 80% in each test subjects.
                                Score range of 500-600 is considered good and only 10-15% of students can score in this interval. To be in this interval, students should score at least 60%-70% in each test subjects.
                                Score range of 350-500 is considered normal and only 20-25% of students can score in this interval.
                                Score range of 200-350 is considered bad and range of 0-200 is considered that the person has failed to demonstrate good score.

                                Master's Education entrance exam score range is 0-100. Having high score is associated with high level of industriousness and may signal higher level of IQ.
                                Score range of 80-100 is considered exceptionally good and only 5-10% of students can achieve this.
                                Score range of 50-80  is considered good and only 10-15% of students can score this.
                                Score range of 40-50  is considered normal and only 20-25% of students can score this.
                                Score range of 0-40   is considered bad and it means that the person has failed.

                                PhD Education entrance exam score range is 0-100. Having high score is associated with high level of industriousness and may signal higher level of IQ.
                                Score range of 80-100 is considered exceptionally good and only 5-10% of students can achieve this.
                                Score range of 50-80  is considered good and only 10-15% of students can score this.
                                Score range of 30-50  is considered normal and only 20-25% of students can score this.
                                Score range of 0-30   is considered bad and it means that the person has failed.'''


            MODEL = "gpt-3.5-turbo"
            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": f"""You are a helpful AI tool which can create only summary part of CV professionally. User data is this: {prompt}. You may also need to know that {testing_system_info}.
                                                    The response you give will be written into CV pdf file, so that do not indicate any redundant and irrelevant things in your response.
                                                    """},
                    {"role": "user", "content": """Please create me a short summary (max 100 words) part for the CV based on the information of me professionally and in a formal way. 
                                                 Add some extra explanations as needed. Do not indicate something like 'Summary:' etc. The response  will be automatically written to CV.
                                                 Write it in first personal singular"""},

                ],
                temperature = temperature,
                # max_tokens = 100
            )

 
            return response.choices[0].message.content
        sample_summary = generate_cv_summary()
        sample_summary.replace("\n\n", "\n")

        return Response({"sample_summary": sample_summary})


class ExperiancePromptAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # df = pd.read_excel("sample_df.xlsx")

        openai.api_key = env("api_key")



        def generate_summary_job_experience(i = 1,  job_no = 1,
                               temperature = 0.7):

            ######################
            ##  Create Prompt   ##
            ######################
            report_data = ReportModel.objects.filter(user=request.user).first()
            umumi_suallar = report_data.general_questions
            orta_texniki_suallar = report_data.secondary_education_questions
            olimpiada_suallar = report_data.olympiad_questions
            is_tecrubesi = report_data.work_experience_questions
            xususi_bacariqlar = report_data.special_skills_questions
            dil_bilikleri = report_data.language_skills_questions
            idman_substage = report_data.sport_questions
            proqram_bilikleri_substage = report_data.program_questions
            idman_substage_2 = report_data.sport2_questions
            prompt = ''
            # prompt += f'Hello, my name is {df.iloc[i].name_surname}. I am {df.iloc[i].age} years old. I am {df.iloc[i].gender}. '
            prompt += f"I have education level of {umumi_suallar['formData']['education']['answer']}. "
            to_be_form =   'were' if umumi_suallar['formData']['education']['answer'] != 'Orta təhsil' else 'are'
            prompt += f"My high school grades {to_be_form} excellent. " if umumi_suallar['formData']['educationGrant']['answer'] == 'Əlaçı' else f"My high school grades {to_be_form} competent. " if umumi_suallar['formData']['educationGrant']['answer'] == 'Zərbəçi' else f"My high school grades {to_be_form} average. "
            prompt += "" if umumi_suallar['formData']['education']['answer'] == 'Orta təhsil' else f"Here is detailed information about my education: {orta_texniki_suallar['formData']['education']}. "
            prompt += "" if olimpiada_suallar['formData']['wonOlympics']['answer'] == 'Xeyr' else f" I have participated in {olimpiada_suallar['formData']['subjectOlympiad']['answer']} subject which was in {olimpiada_suallar['formData']['highestOlympiad']['answer']} level and got {olimpiada_suallar['formData']['rankOlympiad']['answer']}. "
            prompt += "I have had no work experience. " if is_tecrubesi['formData']['haveJobExperience']['answer'] == 'Xeyr' else f"Here is detailed information about my work experience: {is_tecrubesi['formData']['experiences']}. "
            prompt += f"I have no other language knowledge" if dil_bilikleri['formData']['haveLanguageSkills']['answer'] != "Var" else f"""Here is detailed information about my language knowledge: {dil_bilikleri['formData']['languageSkills']}. """

            if idman_substage_2 != None:
                prompt += "" if idman_substage['formData']['haveSport']['answer'] != 'Var' else f"Here is detailed information about my sport background {idman_substage['formData']} and my achievements {idman_substage_2['formData']['professionalSports']}. "
            else:
                prompt += "" if idman_substage['formData']['haveSport']['answer'] != 'Var' else f"Here is detailed information about my sport background {idman_substage['formData']}. "
            prompt += "" if xususi_bacariqlar['formData']['haveSpecialSkills']['answer'] != 'Var' else f"Here is detailed information about my background on other skills: {xususi_bacariqlar['formData']['skills']} + {xususi_bacariqlar['formData']['specialSkills']}. "

            prompt += "" if proqram_bilikleri_substage['formData']['haveProgramSkills']['answer'] != 'Var' else f"Here is detailed information about my background on programming skills: {proqram_bilikleri_substage['formData']['programSkills']} and programs {proqram_bilikleri_substage['formData']['whichProgram']}. "
            prompt = prompt.replace("'", "").replace('"', "").replace("{", "").replace("}", "").replace("_", " ").replace('\n', " ").replace('                         ', " ")

            ################################
            ##  Assign test system info   ##
            ################################
            testing_system_info = '''
                                Having excellent grades in high school means having all grades of best grades (such as A). Having competent grades in high school means having all grades of best and good grades (such as A and B).
                                Having average grades in high school means having different grades - A, B, C, D, etc.
                                DIM is an abbreviation for State Examination Center in Azerbaijan, where most students choose this center's exams to get admission for high educational institutes.
                                Bachelor's Education entrance exam points range is 0-700. Having high score is associated with high level of industriousness and may signal higher level of IQ.
                                Score range of 600-700 is considered exceptionally good and only 5-10% of students can score that much. To be in this interval, students should score at least 80% in each test subjects.
                                Score range of 500-600 is considered good and only 10-15% of students can score in this interval. To be in this interval, students should score at least 60%-70% in each test subjects.
                                Score range of 350-500 is considered normal and only 20-25% of students can score in this interval.
                                Score range of 200-350 is considered bad and range of 0-200 is considered that the person has failed to demonstrate good score.

                                Master's Education entrance exam score range is 0-100. Having high score is associated with high level of industriousness and may signal higher level of IQ.
                                Score range of 80-100 is considered exceptionally good and only 5-10% of students can achieve this.
                                Score range of 50-80  is considered good and only 10-15% of students can score this.
                                Score range of 40-50  is considered normal and only 20-25% of students can score this.
                                Score range of 0-40   is considered bad and it means that the person has failed.

                                PhD Education entrance exam score range is 0-100. Having high score is associated with high level of industriousness and may signal higher level of IQ.
                                Score range of 80-100 is considered exceptionally good and only 5-10% of students can achieve this.
                                Score range of 50-80  is considered good and only 10-15% of students can score this.
                                Score range of 30-50  is considered normal and only 20-25% of students can score this.
                                Score range of 0-30   is considered bad and it means that the person has failed.'''


            MODEL = "gpt-3.5-turbo"
            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": f"""You are a helpful AI tool which can create summary and details part of job experience parts of CV professionally. 
                                                    User data is this: {prompt}. You may also need to know that {testing_system_info}.
                                                    The response you give will be written into CV pdf file, so that do not indicate any redundant and irrelevant things in your response.
                                                    """},
                    {"role": "user", "content": f"""Please create me a short summary (max 100 words) part of my job experience {job_no} based on the information of me professionally and in a formal way. 
                                                 Add some extra explanations as needed. Do not indicate something like 'Summary:' etc. The response  will be automatically written to CV.
                                                 Use bullet points as needed. Do not indicate job name, positions, date range, only some info about job. Do not write any job experience if it is not available, just write something like No work experience available at this time
                                                 """},
                       ],
                temperature = temperature,
                # max_tokens = 100
            )

            # response.choices[0].message.content

            

            return response.choices[0].message.content
        job_experience = generate_summary_job_experience()
        job_experience = job_experience.split("\n")
        return Response({"job_experience": job_experience})
    
class CvContentPromptAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
    
        openai.api_key = env("api_key")
        def generate_cv_content(i = 0, print_response = True, 
                       temperature = 0.7):
    
            ######################
            ##  Create Prompt   ##
            ######################
            report_data = ReportModel.objects.filter(user=request.user).first()
            umumi_suallar = report_data.general_questions
            orta_texniki_suallar = report_data.secondary_education_questions
            olimpiada_suallar = report_data.olympiad_questions
            is_tecrubesi = report_data.work_experience_questions
            xususi_bacariqlar = report_data.special_skills_questions
            dil_bilikleri = report_data.language_skills_questions
            idman_substage = report_data.sport_questions
            proqram_bilikleri_substage = report_data.program_questions
            idman_substage_2 = report_data.sport2_questions

            prompt = ''
            # prompt += f'Hello, my name is {df.iloc[i].name_surname}. I am {df.iloc[i].age} years old. I am {df.iloc[i].gender}. '
            prompt += f"I have education level of {umumi_suallar['formData']['education']['answer']}. "
            to_be_form =   'were' if umumi_suallar['formData']['education']['answer'] != 'Orta təhsil' else 'are'
            prompt += f"My high school grades {to_be_form} excellent. " if umumi_suallar['formData']['educationGrant']['answer'] == 'Əlaçı' else f"My high school grades {to_be_form} competent. " if umumi_suallar['formData']['educationGrant']['answer'] == 'Zərbəçi' else f"My high school grades {to_be_form} average. "
            prompt += "" if umumi_suallar['formData']['education']['answer'] == 'Orta təhsil' else f"Here is detailed information about my education: {orta_texniki_suallar['formData']['education']}. "
            prompt += "" if olimpiada_suallar['formData']['wonOlympics']['answer'] == 'Xeyr' else f" I have participated in {olimpiada_suallar['formData']['subjectOlympiad']['answer']} subject which was in {olimpiada_suallar['formData']['highestOlympiad']['answer']} level and got {olimpiada_suallar['formData']['rankOlympiad']['answer']}. "
            prompt += "I have had no work experience. " if is_tecrubesi['formData']['haveJobExperience']['answer'] == 'Xeyr' else f"Here is detailed information about my work experience: {is_tecrubesi['formData']['experiences']}. "
            prompt += f"I have no other language knowledge" if dil_bilikleri['formData']['haveLanguageSkills']['answer'] != "Var" else f"""Here is detailed information about my language knowledge: {dil_bilikleri['formData']['languageSkills']}. """

            if idman_substage_2 != None:
                prompt += "" if idman_substage['formData']['haveSport']['answer'] != 'Var' else f"Here is detailed information about my sport background {idman_substage['formData']} and my achievements {idman_substage_2['formData']['professionalSports']}. "
            else:
                prompt += "" if idman_substage['formData']['haveSport']['answer'] != 'Var' else f"Here is detailed information about my sport background {idman_substage['formData']}. "

            prompt += "" if xususi_bacariqlar['formData']['haveSpecialSkills']['answer'] != 'Var' else f"Here is detailed information about my background on other skills: {xususi_bacariqlar['formData']['skills']} + {xususi_bacariqlar['formData']['specialSkills']}. "

            prompt += "" if proqram_bilikleri_substage['formData']['haveProgramSkills']['answer'] != 'Var' else f"Here is detailed information about my background on programming skills: {proqram_bilikleri_substage['formData']['programSkills']} and programs {proqram_bilikleri_substage['formData']['whichProgram']}. "
            prompt = prompt.replace("'", "").replace('"', "").replace("{", "").replace("}", "").replace("_", " ").replace('\n', " ").replace('                         ', " ")

            ################################
            ##  Assign test system info   ##
            ################################
            testing_system_info = '''
                                Having excellent grades in high school means having all grades of best grades (such as A). Having competent grades in high school means having all grades of best and good grades (such as A and B).
                                Having average grades in high school means having different grades - A, B, C, D, etc.
                                DIM is an abbreviation for State Examination Center in Azerbaijan, where most students choose this center's exams to get admission for high educational institutes.
                                Bachelor's Education entrance exam points range is 0-700. Having high score is associated with high level of industriousness and may signal higher level of IQ.
                                Score range of 600-700 is considered exceptionally good and only 5-10% of students can score that much. To be in this interval, students should score at least 80% in each test subjects.
                                Score range of 500-600 is considered good and only 10-15% of students can score in this interval. To be in this interval, students should score at least 60%-70% in each test subjects.
                                Score range of 350-500 is considered normal and only 20-25% of students can score in this interval.
                                Score range of 200-350 is considered bad and range of 0-200 is considered that the person has failed to demonstrate good score.

                                Master's Education entrance exam score range is 0-100. Having high score is associated with high level of industriousness and may signal higher level of IQ.
                                Score range of 80-100 is considered exceptionally good and only 5-10% of students can achieve this.
                                Score range of 50-80  is considered good and only 10-15% of students can score this.
                                Score range of 40-50  is considered normal and only 20-25% of students can score this.
                                Score range of 0-40   is considered bad and it means that the person has failed.

                                PhD Education entrance exam score range is 0-100. Having high score is associated with high level of industriousness and may signal higher level of IQ.
                                Score range of 80-100 is considered exceptionally good and only 5-10% of students can achieve this.
                                Score range of 50-80  is considered good and only 10-15% of students can score this.
                                Score range of 30-50  is considered normal and only 20-25% of students can score this.
                                Score range of 0-30   is considered bad and it means that the person has failed.'''


            MODEL = "gpt-3.5-turbo"
            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": f"""You are a helpful AI tool which can create CV based on the user data. User data is this: {prompt}. You may also need to know that {testing_system_info}.
                                                    Do not indicate any redundant and irrelevant things in your response. Do nit write any information which is not related to the CV, write the CV content only.
                                                    Do not write something like `Note`                           
                     """},
                    {"role": "user", "content": "Please create CV based on the information of the user. Add some extra explanations and summaries as needed. Indicate the e summary on the top."},

                ],
                temperature = temperature,
            )


            

            return response.choices[0].message.content
    
        cv_content = generate_cv_content().split("\n")
        if "Note" in cv_content[-1]:
            cv_content.pop()
        return Response({"cv_content": cv_content})