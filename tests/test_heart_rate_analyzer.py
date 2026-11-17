import pytest
import allure
from ecg_interpreter.consts.consts import LOW_HEART_RATE, HIGH_HEART_RATE
from ecg_interpreter.ecg.heart_rate_analyser import (
    analyze_heart_rate,
    average_heart_rate,
    heart_rate_range,
)
from ecg_interpreter.models.interpretation import Diagnosis


@pytest.mark.parametrize(
    "heart_rate, expected",
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


@allure.feature("Heart Rate Analyzer")
@allure.story("Average Heart Rate")
class TestAverageHeartRate:

    @allure.title("Средний пульс для валидного набора измерений")
    @allure.severity(allure.severity_level.NORMAL)
    def test_average_positive(self, valid_ecg_dataset):
        result = average_heart_rate(valid_ecg_dataset)
        assert result == pytest.approx(75.0), (
            f"Средний пульс должен быть 75.0, получено {result}"
        )

    @allure.title("Средний пульс для одного измерения (граничное значение)")
    def test_average_single_interval(self, single_ecg_dataset):
        result = average_heart_rate(single_ecg_dataset)
        assert result == pytest.approx(75.0), (
            f"Для одного измерения с ЧСС=75 средний пульс должен быть 75, получено {result}"
        )

    @allure.title("Пустой список вызывает ValueError")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_average_empty_raises(self, empty_ecg_dataset):
        with pytest.raises(ValueError, match="не может быть пустым"):
            average_heart_rate(empty_ecg_dataset)

    @allure.title("None вызывает ValueError")
    def test_average_none_raises(self):
        with pytest.raises(ValueError, match="не может быть пустым"):
            average_heart_rate(None)


@allure.feature("Heart Rate Analyzer")
@allure.story("Heart Rate Range")
class TestHeartRateRange:

    @allure.title("Диапазон пульса для валидного набора измерений")
    def test_range_positive(self, valid_ecg_dataset):
        min_hr, max_hr = heart_rate_range(valid_ecg_dataset)
        assert min_hr == pytest.approx(74.0), (
            f"Минимальная ЧСС должна быть 74.0, получено {min_hr}"
        )
        assert max_hr == pytest.approx(76.0), (
            f"Максимальная ЧСС должна быть 76.0, получено {max_hr}"
        )

    @allure.title("Пустой список вызывает ValueError")
    def test_range_empty_raises(self, empty_ecg_dataset):
        with pytest.raises(ValueError):
            heart_rate_range(empty_ecg_dataset)

    @allure.title("None вызывает TypeError")
    def test_range_none_raises(self):
        with pytest.raises(TypeError):
            heart_rate_range(None)