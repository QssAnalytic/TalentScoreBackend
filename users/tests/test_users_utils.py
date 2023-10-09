import pytest
import numpy as np
from users.utils.user_utils import get_master_weight




def test_lokal_imtahan_formula():
    masters_data = {
       
            "criterian": {
                "answer": "Lokal imtahan"
            },
        
        "local": {
            "score": 50,  
            "maxScore": 100  
        }
    }

    expected_result = 1 - (masters_data["local"]["score"] / masters_data["local"]["maxScore"])

    result = get_master_weight(masters_data)
    assert result == expected_result
