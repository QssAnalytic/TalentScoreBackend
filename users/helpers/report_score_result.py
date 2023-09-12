def get_report_score(float_value):
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
    return result