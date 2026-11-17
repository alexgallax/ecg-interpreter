import pytest
import allure
from ecg_interpreter.ecg.risk_analyser import risk_score


@allure.feature("Risk Analyzer")
@allure.story("Risk Score Calculation")
class TestRiskScore:

    @allure.title("Риск для нормального измерения (ЧСС=75)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_risk_normal_reading(self, normal_data_ecg):
        score = risk_score(normal_data_ecg)
        assert score == pytest.approx(0.0), (
            f"Для нормального измерения риск должен быть 0.0, получено {score}"
        )

    @allure.title("Риск для измерения с брадикардией (ЧСС=50)")
    def test_risk_bradycardia_reading(self, bradycardia_ecg):
        score = risk_score(bradycardia_ecg)
        assert score >= 0, f"Риск не может быть отрицательным, получено {score}"

    @allure.title("Риск для измерения с тахикардией (ЧСС=120)")
    def test_risk_tachycardia_reading(self, tachycardia_ecg):
        score = risk_score(tachycardia_ecg)
        assert score >= 0, f"Риск не может быть отрицательным, получено {score}"

    @allure.title("Риск для измерения с инфарктом (ЧСС=90)")
    def test_risk_infarction_reading(self, infarction_ecg):
        score = risk_score(infarction_ecg)
        assert score >= 0, f"Риск не может быть отрицательным, получено {score}"