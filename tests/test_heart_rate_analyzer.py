import pytest
from ecg_interpreter.ecg.heart_rate_analyser import analyze_heart_rate
from ecg_interpreter.models.interpretation import Diagnosis
from ecg_interpreter.consts.consts import LOW_HEART_RATE, HIGH_HEART_RATE


@pytest.mark.parametrize(
    "heart_rate, expected_diagnosis",
    [
        (LOW_HEART_RATE - 0.1, Diagnosis.BRADYCARDIA),  # 59.9 - Брадикардия
        (LOW_HEART_RATE, Diagnosis.NORMAL),           # 60.0 - Нижняя граница нормы
        (HIGH_HEART_RATE, Diagnosis.NORMAL),          # 100.0 - Верхняя граница нормы
        (HIGH_HEART_RATE + 1, Diagnosis.TACHYCARDIA), # 100.1 - Тахикардия
        (50.0, Diagnosis.BRADYCARDIA),                # Явная брадикардия
        (120.0, Diagnosis.TACHYCARDIA),               # Явная тахикардия
    ]
)
def test_analyze_heart_rate_positive(heart_rate, expected_diagnosis):
    """Позитивные тесты для analyze_heart_rate с проверкой граничных значений."""
    actual_diagnosis = analyze_heart_rate(heart_rate)
    
    assert actual_diagnosis == expected_diagnosis, (
        f"При ЧСС {heart_rate} ожидали диагноз '{expected_diagnosis.value}', "
        f"но получили '{actual_diagnosis.value}'"
    )