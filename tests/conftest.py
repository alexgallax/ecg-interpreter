import pytest
from ecg_interpreter.models.ecg_data import ECGData, STSegment, Rhythm


@pytest.fixture
def normal_ecg_data():
    """Фикстура с валидными данными ЭКГ без патологий."""
    return ECGData(
        heart_rate=75.0,
        rhythm=Rhythm.REGULAR,
        st_segment=STSegment.NORMAL,
        q_wave=False
    )

@pytest.fixture
def infarction_ecg_data():
    """Фикстура с данными ЭКГ для инфаркта (ST + Q)"""
    return ECGData(
        heart_rate = 90.0,
        rhythm = Rhythm.REGULAR,
        st_segment = STSegment.ELEVATION,
        q_wave = True,
    )

@pytest.fixture
def ischemia_ecg_data():
    """Фикстура с данными ЭКГ для ишемии (депрессия ST)."""
    return ECGData(
        heart_rate=80.0,
        rhythm=Rhythm.REGULAR,
        st_segment=STSegment.DEPRESSION,
        q_wave=False
    )


@pytest.fixture
def arrhythmia_ecg_data():
    """Фикстура с данными ЭКГ для аритмии (нерегулярный ритм)."""
    return ECGData(
        heart_rate=70.0,
        rhythm=Rhythm.IRREGULAR,
        st_segment=STSegment.NORMAL,
        q_wave=False
    )