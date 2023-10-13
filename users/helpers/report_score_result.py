def get_report_score(float_value):
    
    result = ''
    if 0 <= float_value <= 0.2:
            result = 'limited'
    elif 0.21 <= float_value <= 0.4:
        result = 'decent'
    elif 0.41 <= float_value <= 0.6:
        result = 'moderate'
    elif 0.61 <= float_value <= 0.8:
        result = 'solid'
    elif 0.81 <= float_value <= 1:
        result = 'extensive'
    return result