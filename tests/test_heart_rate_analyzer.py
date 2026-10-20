import pytest
from ecg_interpreter.consts.consts import LOW_HEART_RATE, HIGH_HEART_RATE
from ecg_interpreter.ecg.heart_rate_analyser import analyze_heart_rate
from ecg_interpreter.models.interpretation import Diagnosis

@pytest.mark.parametrize("heart_rate, expected",
 [
     (30, Diagnosis.BRADYCARDIA),
     (59, Diagnosis.BRADYCARDIA),
     (LOW_HEART_RATE, Diagnosis.NORMAL),
     (85, Diagnosis.NORMAL),
     (HIGH_HEART_RATE, Diagnosis.NORMAL),
     (101, Diagnosis.TACHYCARDIA),
     (150, Diagnosis.TACHYCARDIA),
                             
],
ids=[
    "30_bradycardia",
    "59_boundary_bradycardia",
    "60_normal_low",
    "85_normal_middle",
    "100_normal_high",
    "101_boundary_tachycardia",
    "150_tachycardia",
],                       
)

def test_analyze_heart_rate(heart_rate, expected): 
     
    result = analyze_heart_rate(heart_rate)

    assert result == expected, (
        f"Когда ЧСС={heart_rate}: ожидали {expected}, получили {result}"
    )