import pytest
from ecg_interpreter.models.ecg_data import ECGData, Rhythm, STSegment

@pytest.fixture
def normal_data_ecg() -> ECGData:
    return ECGData(
        heart_rate = 75,
        rhythm = Rhythm.REGULAR,
        st_segment = STSegment.NORMAL,
        q_wave = False,
    ) 

@pytest.fixture
def infarction_ecg() -> ECGData:
    return ECGData(
        heart_rate = 90,
        rhythm = Rhythm.REGULAR,
        st_segment = STSegment.ELEVATION,
        q_wave = True,
    )

@pytest.fixture
def ischemia_ecg() -> ECGData:
    return ECGData(
        heart_rate = 80,
        rhythm = Rhythm.REGULAR,
        st_segment = STSegment.DEPRESSION,
        q_wave = False,
    )

@pytest.fixture
def infarction_risk_ecg() -> ECGData:
    return ECGData(
        heart_rate = 85,
        rhythm = Rhythm.REGULAR,
        st_segment = STSegment.ELEVATION,
        q_wave = False,
    )

@pytest.fixture
def previous_infarction_ecg() -> ECGData:
    return ECGData(
        heart_rate = 70,
        rhythm = Rhythm.REGULAR,
        st_segment = STSegment.NORMAL,
        q_wave = True,
    )

@pytest.fixture
def arrhythmia_ecg() -> ECGData:
    return ECGData(
        heart_rate = 75,
        rhythm = Rhythm.IRREGULAR,
        st_segment = STSegment.NORMAL,
        q_wave = False,
    )

@pytest.fixture
def bradycardia_ecg() -> ECGData:
    return ECGData(
        heart_rate = 50,
        rhythm = Rhythm.REGULAR,
        st_segment = STSegment.NORMAL,
        q_wave = False,
    )

@pytest.fixture
def tachycardia_ecg() -> ECGData:
    return ECGData(
        heart_rate = 120,
        rhythm = Rhythm.REGULAR,
        st_segment = STSegment.NORMAL,
        q_wave = False,
    )

