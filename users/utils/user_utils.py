from datetime import datetime
from decimal import Decimal, getcontext, ROUND_HALF_UP


def round_to_non_zero(num):
        # Convert the number to a Decimal object
        if num != 1:
        
            num_decimal = Decimal(str(num))
        
            # Initialize the precision with a reasonable maximum value as an integer
            max_precision = 9  # For example, set to 9 for 9 decimal places
        
            while True:
                    # Set the precision for the current iteration
                    getcontext().prec = max_precision
                    # Round the number using ROUND_HALF_UP rounding method
                    rounded_num = num_decimal.quantize(Decimal('1.' + '0' * max_precision), rounding=ROUND_HALF_UP)
                    # Check if the rounded result is non-zero
                    if rounded_num != 0:
                        return rounded_num
                    # Increase the maximum precision (this value should be adjusted based on your needs)
                    max_precision += 1
        return 1
        



def get_date_weight(finnly_date):
        if 0 <= finnly_date < 1:
                finnly_date_weight = 0.9
        elif 1 <= finnly_date < 3:
                finnly_date_weight = 0.7
        elif 3 <= finnly_date < 5:
                finnly_date_weight = 0.5
        elif 5 <= finnly_date <10:
                finnly_date_weight = 0.3
        elif 10 <= finnly_date <20:
                finnly_date_weight = 0.1
        elif 20 <= finnly_date:
                finnly_date_weight = 0.01

        return finnly_date_weight

def calculate_date_difference(data):
        if data["endDate"] == "currently working":
            current_date = datetime.now()
            start_date = datetime.strptime(data["startDate"], "%Y-%m-%d")
            difference = current_date - start_date
        else:
            start_date = datetime.strptime(data["startDate"], "%Y-%m-%d")
            end_date = datetime.strptime(data["endDate"], "%Y-%m-%d")
            difference = end_date - start_date
        return difference

def find_divide(divide):
        if 0<=divide<0.43:
               return 1
        elif 0.43<=divide<0.56:
               return 0.8
        elif 0.56<=divide<0.72:
               return 0.5
        elif 0.72<=divide<0.85:
               return 0.2
        else:
                return 0.05

def get_bachelor_weight(bachelors):
        language_weight = 1
        total_muraciyyet_weight = 1
        total_bachelors_weight = 1
        power_count = 0
        if bachelors['bachelor']['criterion']['criterion_type'] == 'her ikisi':
                local_test_score_divided = bachelors['bachelor']['criterion']['lokal_test']["score"]/bachelors['bachelor']['criterion']['lokal_test']["max_score"]
                lokal_test_weight = find_divide(local_test_score_divided)
                muraciyyet = bachelors['bachelor']['criterion']['muraciyyet']
                for m in muraciyyet:
                        if m['muraciyyet_type'] == 'Atestat':
                                power_count+=1  
                                atestat_score_divided  =  m['score']/300
                                atestat_weight = find_divide(atestat_score_divided)
                                total_muraciyyet_weight *= atestat_weight
                        elif m['muraciyyet_type'] == 'language':
                                for lang in m['language_type']:
                                        power_count+=1
                                        if lang["language_name"] == "IELTS":
                                                ielts_score_divided = lang["language_score"]/9
                                                language_weight *= find_divide(ielts_score_divided)
                                        else:
                                                toefl_score_divided = lang["language_score"]/9
                                                language_weight *= find_divide(toefl_score_divided)
                                language_weight = round(language_weight,3)
                                total_muraciyyet_weight *= language_weight
                        elif m['muraciyyet_type'] == 'SAT':
                               sat_weight = m['answer_weight']
                               total_muraciyyet_weight*=sat_weight
                total_muraciyyet_weight = (total_muraciyyet_weight)**(1/power_count) 
                total_muraciyyet_weight = round(total_muraciyyet_weight,3)
                total_bachelors_weight = round((lokal_test_weight*total_muraciyyet_weight)**(1/2),3)    
                
        elif bachelors['bachelor']['criterion']['criterion_type'] == 'Lokal imtahan': 
                total_bachelors_weight = bachelors['bachelor']['criterion']['lokal_test']['answer_weight']
                
        elif bachelors['bachelor']['criterion']['criterion_type'] == 'Müraciyyət': 
                muraciyyet = bachelors['bachelor']['criterion']['muraciyyet']
                for m in muraciyyet:
                        if m['muraciyyet_type'] == 'Atestat':
                                power_count+=1     
                                atestat_weight = m['answer_weight']
                                total_muraciyyet_weight *= atestat_weight
                        elif m['muraciyyet_type'] == 'language':
                                for lang in m['language_type']:
                                    power_count+=1
                                    language_weight *= lang['answer_weight']
                                language_weight = round(language_weight,3)
                                total_muraciyyet_weight *= language_weight
                        elif m['muraciyyet_type'] == 'SAT':
                               sat_weight = m['answer_weight']
                               total_muraciyyet_weight*=sat_weight
                total_muraciyyet_weight = (total_muraciyyet_weight)**(1/power_count) 
                total_muraciyyet_weight = round(total_muraciyyet_weight,3)
                total_bachelors_weight = round((lokal_test_weight*total_muraciyyet_weight)**(1/2),3)   
                         
        return total_bachelors_weight

def get_master_weight(masters):
        language_weight = 1
        total_muraciyyet_weight = 1
        total_masters_weight = 1
        power_count = 0
        if masters['master']['criterion']['criterion_type'] == 'her ikisi':
                lokal_test_weight = masters['master']['criterion']['lokal_test']['answer_weight']
                
                muraciyyet = masters['master']['criterion']['muraciyyet']
                for m in muraciyyet:
                        if m['muraciyyet_type'] == 'Atestat':
                                power_count+=1     
                                atestat_weight = m['answer_weight']
                                total_muraciyyet_weight *= atestat_weight
                        elif m['muraciyyet_type'] == 'language':
                                for lang in m['language_type']:
                                    power_count+=1
                                    language_weight *= lang['answer_weight']
                                language_weight = round(language_weight,3)
                                total_muraciyyet_weight *= language_weight
                        elif m['muraciyyet_type'] == 'SAT':
                               sat_weight = m['answer_weight']
                               total_muraciyyet_weight*=sat_weight
                total_muraciyyet_weight = (total_muraciyyet_weight)**(1/power_count) 
                total_muraciyyet_weight = round(total_muraciyyet_weight,3)
                total_masters_weight = round((lokal_test_weight*total_muraciyyet_weight)**(1/2),3)    
                
        elif masters['master']['criterion']['criterion_type'] == 'Lokal imtahan': 
                total_masters_weight = masters['master']['criterion']['lokal_test']['answer_weight']
                
        elif masters['master']['criterion']['criterion_type'] == 'Müraciyyət': 
                muraciyyet = masters['master']['criterion']['muraciyyet']
                total_masters_weight = 1
                for m in muraciyyet:
                        if m['muraciyyet_type'] == 'Atestat':
                                power_count+=1     
                                atestat_weight = m['answer_weight']
                                total_masters_weight *= atestat_weight
                        elif m['muraciyyet_type'] == 'language':
                                for lang in m['language_type']:
                                    power_count+=1
                                    language_weight *= lang['answer_weight']
                                language_weight = round(language_weight,3)
                                total_masters_weight *= language_weight
                        elif m['muraciyyet_type'] == 'SAT':
                               sat_weight = m['answer_weight']
                               total_masters_weight*=sat_weight
                total_masters_weight = (total_masters_weight)**(1/power_count) 
                total_masters_weight = round(total_masters_weight,3)
                              
        return total_masters_weight

def get_phd_weight(phds):
        language_weight = 1
        total_muraciyyet_weight = 1
        total_phds_weight = 1
        power_count = 0
        if phds['phd']['criterion']['criterion_type'] == 'her ikisi':
                lokal_test_weight = phds['phd']['criterion']['lokal_test']['answer_weight']
                
                muraciyyet = phds['phd']['criterion']['muraciyyet']
                for m in muraciyyet:
                        if m['muraciyyet_type'] == 'Atestat':
                                power_count+=1     
                                atestat_weight = m['answer_weight']
                                total_muraciyyet_weight *= atestat_weight
                        elif m['muraciyyet_type'] == 'language':
                                for lang in m['language_type']:
                                    power_count+=1
                                    language_weight *= lang['answer_weight']
                                language_weight = round(language_weight,3)
                                total_muraciyyet_weight *= language_weight
                        elif m['muraciyyet_type'] == 'SAT':
                               sat_weight = m['answer_weight']
                               total_muraciyyet_weight*=sat_weight
                total_muraciyyet_weight = (total_muraciyyet_weight)**(1/power_count) 
                total_muraciyyet_weight = round(total_muraciyyet_weight,3)
                total_phds_weight = round((lokal_test_weight*total_muraciyyet_weight)**(1/2),3)    
                
        elif phds['phd']['criterion']['criterion_type'] == 'Lokal imtahan': 
                total_phds_weight = phds['phd']['criterion']['lokal_test']['answer_weight']
                
        elif phds['phd']['criterion']['criterion_type'] == 'Müraciyyət': 
                muraciyyet = phds['phd']['criterion']['muraciyyet']
                total_phds_weight = 1
                for m in muraciyyet:
                        if m['muraciyyet_type'] == 'Atestat':
                                power_count+=1     
                                atestat_weight = m['answer_weight']
                                total_phds_weight *= atestat_weight
                        elif m['muraciyyet_type'] == 'language':
                                for lang in m['language_type']:
                                    power_count+=1
                                    language_weight *= lang['answer_weight']
                                language_weight = round(language_weight,3)
                                total_phds_weight *= language_weight
                        elif m['muraciyyet_type'] == 'SAT':
                               sat_weight = m['answer_weight']
                               total_phds_weight*=sat_weight
                total_phds_weight = (total_phds_weight)**(1/power_count) 
                total_phds_weight = round(total_phds_weight,3)
                              
        return total_phds_weight