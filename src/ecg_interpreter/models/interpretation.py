from dataclasses import dataclass
from enum import Enum


class Diagnosis(str, Enum):
    NORMAL = "normal"
    BRADYCARDIA = "bradycardia"
    TACHYCARDIA = "tachycardia"
    ARRHYTHMIA = "arrhythmia"
    PREVIOUS_INFARCTION = "previous_infarction"
    ISCHEMIA = "ischemia"
    SUSPECTED_INFARCTION = "suspected_infarction"
    INFARCTION = "infarction"


class Urgency(str, Enum):
    NONE = "none"
    PLANNED = "planned"
    URGENT = "urgent"


@dataclass
class Interpretation:
    diagnosis: Diagnosis
    urgency: Urgency