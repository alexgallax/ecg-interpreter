from ecg_interpreter.models.interpretation import Diagnosis, Urgency


"""
Пороговые значения ЧСС
"""
LOW_HEART_RATE = 60.0
HIGH_HEART_RATE = 100.0
MAX_HEART_RATE = 300.0


"""
Показатель риска по срочности
"""
RISK_BY_URGENCY: dict[Urgency, float] = {
    Urgency.NONE: 0.0,
    Urgency.PLANNED: 25.0,
    Urgency.URGENT: 80.0,
}


"""
Показатель риска по значению ЧСС
"""
RISK_BY_HEART_RATE: dict[Diagnosis, float] = {
    Diagnosis.NORMAL: 0.0,
    Diagnosis.BRADYCARDIA: 5.0,
    Diagnosis.TACHYCARDIA: 5.0,
}


"""
Показатель риска по диагнозу
"""
RISK_BY_DIAGNOSIS: dict[Diagnosis, float] = {
    Diagnosis.NORMAL: 1.0,
    Diagnosis.BRADYCARDIA: 1.2,
    Diagnosis.TACHYCARDIA: 1.2,
    Diagnosis.ARRHYTHMIA: 1.4,
    Diagnosis.PREVIOUS_INFARCTION: 1.45,
    Diagnosis.ISCHEMIA: 1.5,
    Diagnosis.SUSPECTED_INFARCTION: 1.8,
    Diagnosis.INFARCTION: 2.0,
}
