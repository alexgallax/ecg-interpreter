from ecg_interpreter.consts.consts import RISK_BY_URGENCY, RISK_BY_HEART_RATE, RISK_BY_DIAGNOSIS
from ecg_interpreter.ecg.heart_rate_analyser import analyze_heart_rate
from ecg_interpreter.ecg.interpreter import validate_data, interpret_ecg
from ecg_interpreter.ecg.validators import validate_heart_rate
from ecg_interpreter.models.ecg_data import ECGData
from ecg_interpreter.models.interpretation import Diagnosis


def risk_score(data: ECGData) -> float:
    """
    Анализ риска по данным ЭКГ.

    Формула:
        (базовое значение по срочности + значение по ЧСС) * множитель по диагнозу

    :param data: Данные ЭКГ.
    :return: показатель риска.
    """
    validate_data(data)

    validate_heart_rate(data.heart_rate)
    interpretation = interpret_ecg(data)

    base = RISK_BY_URGENCY[interpretation.urgency]

    heart_rate_analysis = analyze_heart_rate(data.heart_rate)
    heart_rate_component = RISK_BY_HEART_RATE[heart_rate_analysis]

    if heart_rate_analysis == Diagnosis.BRADYCARDIA or heart_rate_analysis == Diagnosis.TACHYCARDIA:
        heart_rate_component = 0.2

    multiplier = RISK_BY_DIAGNOSIS[interpretation.diagnosis]

    return (base * heart_rate_component) * multiplier
