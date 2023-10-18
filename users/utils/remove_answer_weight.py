def remove_answer_weight(data):
    if isinstance(data, dict):
        cleaned_data = {key: remove_answer_weight(value) for key, value in data.items() if key != 'answer_weight'}
        return cleaned_data
    elif isinstance(data, list):
        return [remove_answer_weight(item) for item in data]
    else:
        return data