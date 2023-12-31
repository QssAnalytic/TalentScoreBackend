from functools import reduce
from pprint import pprint

import math, time
import ast
from typing import TypeVar
from users.utils.user_utils import *
from users.models import ReportModel
from users.utils.hash_utils import decrypt_string

from django.contrib.auth import get_user_model

UserAccount = get_user_model()
user_account_type = TypeVar('user_account_type', bound=UserAccount)

def check(data, key):

        if data.get(key) is not None:
                if data[key] !={}:
                        decoded_data = decrypt_string(ast.literal_eval(data[key]["answer_weight"]))
                        return float(decoded_data)
        return 1

def get_education_score(request):
        # report = ReportModel.objects.filter(user=user).last()
        user_info = request.data.get('user_info')
        umumi_stage = None
        education_stage = None
        olimpia_stage = None
        max_bachelor_weight = 1
        max_master_weight = 1
        max_phd_weight = 1
        education_degree_weight = 1
        for stage in user_info:
            if stage['name'] == 'umumi-suallar':
                umumi_stage = stage
                
            if stage['name'] == 'orta-texniki-ve-ali-tehsil-suallari':
                education_stage = stage
                
            if stage['name'] == 'olimpiada-suallari':
                olimpia_stage = stage
                
        
        if umumi_stage != None:
                work_activite_weight = check(data = umumi_stage["formData"], key = "curOccupation")
                education_weight = check(umumi_stage["formData"]["education"], key = "master")
                education_grand_weight = check(data = umumi_stage["formData"], key = "educationGrant")
        if olimpia_stage !=None:
                olimp_highest_weight = check(data = olimpia_stage["formData"], key = "highestOlympiad")
                olimp_rank_weight = check(data = olimpia_stage["formData"], key = "rankOlympiad")
        if education_stage !=None:
                userdata = education_stage["formData"]["education"]
                bachelor_weight_list = []
                master_weight_list = []
                phd_weight_list = []
                for edu in userdata:
                        if edu.get("bachelor") is not None:
                                if edu["bachelor"] != {}:
                                        bachelor_weight = get_bachelor_weight(edu)
                                        bachelor_weight_list.append(bachelor_weight)
                        if edu.get("master") is not None:
                                if edu["master"] != {}:
                                        master_weight = get_master_weight(edu)
                                        master_weight_list.append(master_weight)

                        if edu.get("phd") is not None:
                                if edu["phd"] != {}:
                                        phd_weight = get_phd_weight(edu)
                                        phd_weight_list.append(phd_weight)
                if bachelor_weight_list!=[]:
                        max_bachelor_weight = max(bachelor_weight_list)
                        max_master_weight = max(master_weight_list)
                if phd_weight_list != []:
                        max_phd_weight = max(master_weight_list)
                education_degree_weight = round(max_bachelor_weight*max_master_weight*max_phd_weight,3)

        total_education_weight = work_activite_weight*education_weight*(education_grand_weight*education_degree_weight*olimp_highest_weight*olimp_rank_weight)**(1/3)
        total_education_weight = round(total_education_weight,7)
        return total_education_weight
        


def get_experience_score(stagedata):
    userdata = stagedata["formData"]["experiences"]
    experiance_score = 1
    if len(userdata) > 0:
        workingform = {"Fiziki əmək": 1, "Sənət": 2, "Ali ixtisas": 3, "Sahibkar": 4}
        max_working_form_weight = 0
        profession_degree_weight = 0
        if len(userdata) > 1:
            max = 0
            for data in userdata:
                if workingform[data["workingActivityForm"]["answer"]] > max:
                    max = workingform[data["workingActivityForm"]["answer"]]
                    max_working_form_weight = float(decrypt_string(ast.literal_eval(data["workingActivityForm"]["answer_weight"])))
                    profession_degree_weight = float(decrypt_string(ast.literal_eval(data["degreeOfProfes"]["answer_weight"])))
                    difference = calculate_date_difference(data)

            finnly_date = difference.days / 365.25
            finnly_date_weight = get_date_weight(finnly_date=finnly_date)
            experiance_score = max_working_form_weight * profession_degree_weight * finnly_date_weight
        else:
            max_working_form_weight = float(decrypt_string(ast.literal_eval(userdata[0]["workingActivityForm"]["answer_weight"])))
            profession_degree_weight = float(decrypt_string(ast.literal_eval(userdata[0]["degreeOfProfes"]["answer_weight"])))
            difference = calculate_date_difference(userdata[0])
            finnly_date = difference.days / 365.25
            finnly_date_weight = get_date_weight(finnly_date=finnly_date)
            experiance_score = max_working_form_weight * profession_degree_weight * finnly_date_weight

        return experiance_score
    return 0


def get_skills_score(stagedata):

    if stagedata['formData']['haveSpecialSkills']['answer'] == "Var":

        userdata = stagedata["formData"]["skills"]
        lst = []
        heveskar_count = 0
        pesekar_count = 0
        formula_result = 1
        pesekar_answer_weight = 1
        heveskar_answer_weight = 1
        for data in userdata:
            lst.append(data['value']['answer'])

            if data['value']['answer'] == 'Həvəskar':
                heveskar_answer_weight = float(decrypt_string(ast.literal_eval(data['value']['answer_weight'])))

            elif data['value']['answer'] == 'Peşəkar':
                pesekar_answer_weight = float(decrypt_string(ast.literal_eval(data['value']['answer_weight'])))

        for value in lst:
            if value == 'Həvəskar':
                heveskar_count += 1

            elif value == 'Peşəkar':
                pesekar_count += 1


        formula_result = (heveskar_answer_weight ** heveskar_count) * (pesekar_answer_weight ** pesekar_count)

        return formula_result

    else:
        return 0


def get_language_score(stagedata):
        if stagedata['formData'] != {}:
                language_skills:bool = stagedata['formData']['haveLanguageSkills']['answer']
                total_language_weight = 1
                if language_skills != 'Var':
                        return 0

                userdata = stagedata["formData"]["languageSkills"]
                for data in userdata:
                        
                        if data['language']['answer'] == "Ingilis dili":
                                if data['engLangCert']['answer'] == "İELTS" or data['engLangCert']['answer'] == "TOEFL":
                                        total_language_weight*=float(decrypt_string(ast.literal_eval(data['engCertResult']['answer_weight'])))
                                else:
                                        total_language_weight*=float(decrypt_string(ast.literal_eval(data['langLevel']['answer_weight'])))
                        else:
                                total_language_weight*=float(decrypt_string(ast.literal_eval(data['langLevel']['answer_weight'])))
                return total_language_weight


def get_sport_skills_score(sport_stage = None, sport_stage2 = None):
        
        heveskar_weight = 0.3
        pesekar_weight = 0.03
        pesekar_total_score = 1
        heveskar_total_score = 1
        heveskar_data = [data for data in sport_stage if data['value']['answer'] == 'Həvəskar']
        heveskar_total_score = reduce(lambda x, y: x * float(decrypt_string(ast.literal_eval(y['value']['answer_weight']))), heveskar_data, 1)
        if sport_stage2 != None:
                for data in sport_stage2:
                        pesekar_total_score*=float(decrypt_string(ast.literal_eval(data['value']['whichScore']['answer_weight'])))*float(decrypt_string(ast.literal_eval(data['value']['whichPlace']['answer_weight'])))*pesekar_weight
                total_score = pesekar_total_score*heveskar_total_score
                return total_score
        return heveskar_total_score


def get_programming_skills_score(stagedata):
    userdata = stagedata["formData"]

    result = {
        'msOfficeScore': 1,
        'designScore': 1,
        'programsScore': 1,
        'othersScore': 1,
    }

    if userdata['haveProgramSkills']['answer'] == "Var":
        # Calculating officeScore
        word_score = 0
        excel_score = 0
        pp_score = 0

        if userdata['programSkills'] and userdata['programSkills'] != [] and userdata['programSkills'] != 0 and userdata['programSkills'] != '0':
            for answer in userdata['programSkills']:
                for program in answer['whichLevel']:
                    if program['name'] == 'Word' and program['answer_weight'] is not None and program['value']['answer_weight'] is not None:
                        word_score = float(decrypt_string(ast.literal_eval(program['answer_weight']))) * float(decrypt_string(ast.literal_eval(program['value']['answer_weight'])))
                    if program['name'] == 'Excel' and program['answer_weight'] is not None and program['value']['answer_weight'] is not None:
                        excel_score = float(decrypt_string(ast.literal_eval(program['answer_weight']))) * float(decrypt_string(ast.literal_eval(program['value']['answer_weight'])))
                    if program['name'] == 'PowerPoint' and program['answer_weight'] is not None and program['value']['answer_weight'] is not None:
                        pp_score = float(decrypt_string(ast.literal_eval(program['answer_weight']))) * float(decrypt_string(ast.literal_eval(program['value']['answer_weight'])))

            weight_list = {
                'Excel': excel_score,
                'Word': word_score,
                "PowerPoint": pp_score,
            }
            for value in weight_list.values():
                if value != 0:
                    result['msOfficeScore'] *= value
        else:
            result["msOfficeScore"] = 1


        level_scores_mapping = {
            "programs": {"Junior": {1: 0.3, 2: 0.2, 3: 0.1, 4: 0.05}, 'Middle': {1: 0.05, 2: 0.03, 3: 0.01, 4: 0.005}, 'Senior': {1: 0.005, 2: 0.003, 3: 0.001, 4: 0.0005}},
            "design": {"Junior": {1: 0.4, 2: 0.3, 3: 0.2, 4: 0.1}, 'Middle': {1: 0.1, 2: 0.05, 3: 0.01, 4: 0.005}, 'Senior': {1: 0.01, 2: 0.005, 3: 0.001, 4: 0.0005}},
            "others": {"Junior": {1: 0.4, 2: 0.3, 3: 0.2, 4: 0.1}, 'Middle': {1: 0.1, 2: 0.05, 3: 0.01, 4: 0.005}, 'Senior': {1: 0.01, 2: 0.005, 3: 0.001, 4: 0.0005}}
        }

        lst = {
            'design': [0, 0, 0],
            'programs': [0, 0, 0],
            'others': [0, 0, 0]
        }

        for program in userdata['programSkills']:
            if program['whichProgram'] == 'Dizayn Proqramları' and program['whichProgram'] != [] and program['whichProgram'] != '' and program['whichProgram'] != 0:
                
                for data in program['whichLevel']:
                    if data['value']['answer'] == 'İlkin':
                        lst['design'][0] += 1
                    if data['value']['answer'] == 'Orta':
                        
                        lst['design'][1] += 1
                    if data['value']['answer'] == 'İrəli':
                        lst['design'][2] += 1

            if program['whichProgram'] == 'Proqramlaşdırma dilləri' and program['whichProgram'] != [] and program['whichProgram'] != 0:
                
                for data in program['whichLevel']:
                    if data['value']['answer'] == 'Junior':
                        lst['programs'][0] += 1
                    if data['value']['answer'] == 'Middle':
                        lst['programs'][1] += 1
                    if data['value']['answer'] == 'Senior':
                        lst['programs'][2] += 1

            if userdata['whichProgram'] == 'others' and userdata['whichProgram'] != []:
                for data in userdata['whichProgram']:
                    if data['value']['answer'] == 'Junior':
                        lst['others'][0] += 1
                    if data['value']['answer'] == 'Middle':
                        lst['others'][1] += 1
                    if data['value']['answer'] == 'Senior':
                        lst['others'][2] += 1

        levels = ['Junior', 'Middle', 'Senior']

        for i, level in enumerate(levels):
            if lst['design'] != [0, 0, 0]:
                count = lst['design'][i]
                if count != 0:
                    if count > 4:
                        level_score = level_scores_mapping['design'][level].get(4)
                        result['designScore'] *= level_score
                    elif count <= 4:
                        level_score = level_scores_mapping['design'][level].get(count)
                        result['designScore'] *= level_score
            else:
                result['designScore'] = 1

            if lst['programs'] != [0, 0, 0]:
                count = lst['programs'][i]
                if count != 0:
                    if count > 4:
                        level_score = level_scores_mapping['programs'][level].get(4)
                        result['programsScore'] *= level_score
                    elif count <= 4:
                        level_score = level_scores_mapping['programs'][level].get(count)
                        result['programsScore'] *= level_score
            else:
                result['programsScore'] = 1

            if lst['others'] != [0, 0, 0]:
                count = lst['others'][i]
                if count != 0:
                    if count > 4:
                        level_score = level_scores_mapping['others'][level].get(4)
                        result['othersScore'] *= level_score
                    elif count <= 4:
                        level_score = level_scores_mapping['others'][level].get(count)
                        result['othersScore'] *= level_score
            else:
                result['othersScore'] = 1

        category_scores = []

        for category in result:
            result[category] = round(result[category], 4)
            category_score = result[category]
            category_scores.append(category_score)

        if len(set(category_scores)) == 1:
            # print(f"All category scores are the same. min is {min(category_scores)}")
            pass
        else:
            minimum_score = min(category_scores)
            category_scores.remove(minimum_score)
            programming_skills_score = 1

            if category_scores != []:
                for score in category_scores:
                    if 0.5 < score <= 1:
                        programming_skills_score *= 0.9
                    elif 0.3 < score <= 0.5:
                        programming_skills_score *= 0.8
                    elif 0.1 < score <= 0.3:
                        programming_skills_score *= 0.7
                    elif 0.01 < score <= 0.1:
                        programming_skills_score *= 0.5
                    elif 0.001 < score <= 0.01:
                        programming_skills_score *= 0.3
                    elif 0.0001 < score <= 0.001:
                        programming_skills_score *= 0.2
                    else:
                        programming_skills_score *= 0.1

                programming_skills_score *= minimum_score
            else:
                programming_skills_score = 0

            return programming_skills_score

    return 0
