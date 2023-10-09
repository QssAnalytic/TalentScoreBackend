import pytest
from datetime import datetime, timedelta
from users.utils.user_utils import calculate_date_difference, find_divide, get_bachelor_weight, get_phd_weight
@pytest.mark.parametrize("data, expected_difference", [
    ({"startDate": "2022-01-01", "endDate": "2022-12-31"}, timedelta(days=364)),  # Test with specific end date
    ({"startDate": "2022-01-01", "endDate": "currently working"}, (datetime.now()-datetime(2022, 1, 1))),  # Test with "currently working"
])
def test_calculate_date_difference(data, expected_difference):
    result = calculate_date_difference(data)
    result_days = result.days
    expected_days = expected_difference.days
    assert result_days == expected_days

@pytest.mark.parametrize("data, non_expected_difference", [
    ({"startDate": "2022-01", "endDate": "2022-12-31"}, timedelta(days=360)),  # Test with specific end date
    ({"startDate": "2022-01", "endDate": "currently working"}, timedelta(days=364)),  # Test with "currently working"
])

def test_invalid_date_difference(data, non_expected_difference):
    with pytest.raises(ValueError):
        result = calculate_date_difference(data)
        result_days = result.days
        expected_days = non_expected_difference.days
        assert result_days == expected_days

@pytest.mark.parametrize("divide, expected_result", [
    (0.42, 1),   # Test with divide just below the first threshold
    (0.43, 0.8),  # Test with divide exactly at the first threshold
    (0.55, 0.8),  # Test with divide within the first range
    (0.56, 0.5),  # Test with divide exactly at the second threshold
    (0.71, 0.5),  # Test with divide within the second range
    (0.72, 0.2),  # Test with divide exactly at the third threshold
    (0.84, 0.2),  # Test with divide within the third range
    (0.85, 0.05),  # Test with divide exactly at the fourth threshold
    (0.86, 0.05),  # Test with divide above the fourth threshold
])
def test_find_divide(divide, expected_result):
    result = find_divide(divide)
    assert result == expected_result

@pytest.mark.parametrize("bachelors, expected_weight", [
    # Test case 1: Criterion type 'her ikisi' with Atestat, IELTS, and SAT
    # (
    #     {
    #         "criterian": {"answer": "her ikisi"},
    #         "local": {"score": 70, "maxScore": 100},
    #         "attestat": {"score": 270},
    #         "languages": [
    #             {"language_name": "IELTS", "language_score": 6.5},
    #             {"language_name": "TOEFL", "language_score": 90}
    #         ],
    #         "sat": {"answer_weight": 0.7},
    #         "application": ["Attestat", "language", "SAT"]
    #     },
    #     0.679  # Expected result for the given input
    # ),

    # Test case 2: Criterion type 'Lokal imtahan' with score
    (
        {
            "criterian": {"answer": "Lokal imtahan"},
            "local": {"score": 60, "maxScore": 100}
        },
        0.4  # Expected result for the given input
    ),

    # Test case 3: Criterion type 'Müraciyyət' with Atestat, language, and SAT
    # (
    #     {
    #         "criterian": {"answer": "Müraciyyət"},
    #         "Bakalavr": {
    #             "criterian": {
    #                 "muraciyyet": [
    #                     {"muraciyyet_type": "Atestat", "answer_weight": 0.8},
    #                     {"muraciyyet_type": "language", "language_type": [{"language_name": "IELTS", "answer_weight": 0.9}]},
    #                     {"muraciyyet_type": "SAT", "answer_weight": 0.7}
    #                 ]
    #             }
    #         }
    #     },
    #     0.836  # Expected result for the given input
    # ),
])

def test_get_bachelor_weight(bachelors, expected_weight):
    result = get_bachelor_weight(bachelors)
    assert result == expected_weight

@pytest.mark.parametrize("phds, expected_weight", [
    # Test case 1: Criterion type 'her ikisi' with Atestat, IELTS, and SAT
    # (
    #     {
    #         "criterian": {"answer": "her ikisi"},
    #         "local": {"score": 70, "maxScore": 100},
    #         "attestat": {"score": 270},
    #         "languages": [
    #             {"language_name": "IELTS", "language_score": 6.5},
    #             {"language_name": "TOEFL", "language_score": 90}
    #         ],
    #         "sat": {"answer_weight": 0.7},
    #         "application": ["Attestat", "language", "SAT"]
    #     },
    #     0.679  # Expected result for the given input
    # ),

    # Test case 2: Criterion type 'Lokal imtahan' with score
    (
        {
            "criterian": {"answer": "Lokal imtahan"},
            "local": {"score": 60, "maxScore": 100}
        },
        0.4  # Expected result for the given input
    ),

    # Test case 3: Criterion type 'Müraciyyət' with Atestat, language, and SAT
    # (
    #     {
    #         "criterian": {"answer": "Müraciyyət"},
    #         "Bakalavr": {
    #             "criterian": {
    #                 "muraciyyet": [
    #                     {"muraciyyet_type": "Atestat", "answer_weight": 0.8},
    #                     {"muraciyyet_type": "language", "language_type": [{"language_name": "IELTS", "answer_weight": 0.9}]},
    #                     {"muraciyyet_type": "SAT", "answer_weight": 0.7}
    #                 ]
    #             }
    #         }
    #     },
    #     0.836  # Expected result for the given input
    # ),
])

def test_get_bachelor_weight(phds, expected_weight):
    result = get_phd_weight(phds)
    assert result == expected_weight