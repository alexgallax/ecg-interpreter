from dataclasses import dataclass
from enum import Enum


@dataclass
class Interpretation:
    """
    Интерпретация данных ЭКГ
    """
    diagnosis: Diagnosis
    urgency: Urgency


class Diagnosis(str, Enum):
    """
    Диагноз
    """
    NORMAL = "normal"
    BRADYCARDIA = "bradycardia"
    TACHYCARDIA = "tachycardia"
    ARRHYTHMIA = "arrhythmia"
    ISCHEMIA = "ischemia"
    INFARCTION = "infarction"
    SUSPECTED_INFARCTION = "suspected infarction"
    PREVIOUS_INFARCTION = "previous infarction"


class Urgency(str, Enum):
    """
    Степень срочности
    """
    NONE = "none"
    PLANNED = "planned"
    URGENT = "urgent"
