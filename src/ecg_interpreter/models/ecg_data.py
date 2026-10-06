from dataclasses import dataclass
from enum import Enum


@dataclass
class ECGData:
    """
    Данные ЭКГ
    """
    heart_rate: float
    rhythm: Rhythm
    st_segment: STSegment
    q_wave: bool


class Rhythm(str, Enum):
    """
    Сердечный ритм
    """
    REGULAR = "regular"
    IRREGULAR = "irregular"


class STSegment(str, Enum):
    """
    Сегмент ST
    """
    NORMAL = "normal"
    ELEVATION = "elevation"
    DEPRESSION = "depression"
