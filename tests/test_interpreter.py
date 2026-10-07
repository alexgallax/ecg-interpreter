from ecg_interpreter.ecg.interpreter import interpret_ecg
from ecg_interpreter.models.interpretation import Diagnosis, Urgency
from ecg_interpreter.models.ecg_data import STSegment, Rhythm

def test_interpret_ecg_infarction(infarction_ecg_data):
    """Тест: ST + Q = Инфаркт (urgent)"""
    result = interpret_ecg(infarction_ecg_data)

    assert result.diagnosis == Diagnosis.INFARCTION, "Ожидался диагноз инфаркт"
    assert result.urgency == Urgency.URGENT, "должен иметь срочность urgent"


def test_interpret_ecg_suspected_infarction(normal_ecg_data):
    """Тест: ST без Q = Подозрение на инфаркт (urgent)."""

    normal_ecg_data.st_segment = STSegment.ELEVATION
    normal_ecg_data.q_wave = False
    
    result = interpret_ecg(normal_ecg_data)
    
    assert result.diagnosis == Diagnosis.SUSPECTED_INFARCTION, "Ожидалось подозрение на инфаркт"
    assert result.urgency == Urgency.URGENT, "должен иметь срочность urgent"

def test_interpret_ecg_ischemia(ischemia_ecg_data):
    """Тест: Депрессия ST = Ишемия (планово)"""
    result = interpret_ecg(ischemia_ecg_data)
    
    assert result.diagnosis == Diagnosis.ISCHEMIA, "Ожидалась Ишемия"
    assert result.urgency == Urgency.PLANNED, "Ишемия должна быть в плановом порядке"


def test_interpret_ecg_arrhythmia(arrhythmia_ecg_data):
    """Тест: Нерегулярный ритм = Аритмия (Планово)"""
    result = interpret_ecg(arrhythmia_ecg_data)
    
    assert result.diagnosis == Diagnosis.ARRHYTHMIA, "Ожидался диагноз 'Аритмия'"
    assert result.urgency == Urgency.PLANNED, "Аритмия должна быть в плановом порядке"

def test_interpret_ecg_previous_infarction(normal_ecg_data):
    """Тест: Зубец Q без ST = Перенесенный инфаркт (планово)"""
    normal_ecg_data.q_wave = True
    normal_ecg_data.st_segment = STSegment.NORMAL
    
    result = interpret_ecg(normal_ecg_data)
    
    assert result.diagnosis == Diagnosis.PREVIOUS_INFARCTION, "Ожидался перенесенный инфаркт"
    assert result.urgency == Urgency.PLANNED, "Перенесенный инфаркт должен быть в плановом порядке"


def test_interpret_ecg_fallback_normal(normal_ecg_data):
    """Тест: Обычные данные ЭКГ передаются в analyze_heart_rate. (норма)"""
    # Убеждаемся, что данные норм, без патологий
    normal_ecg_data.heart_rate = 75.0
    normal_ecg_data.st_segment = STSegment.NORMAL
    normal_ecg_data.q_wave = False
    normal_ecg_data.rhythm = Rhythm.REGULAR
    
    result = interpret_ecg(normal_ecg_data)
    
    assert result.diagnosis == Diagnosis.NORMAL, "Ожидался нормальный диагноз"
    assert result.urgency == Urgency.NONE, "Для нормы срочность не требуется (NONE)"

def test_interpret_ecg_fallback_tachycardia(normal_ecg_data):
    """Тест: Обычные данные ЭКГ передаются в analyze_heart_rate. (тахикардия)"""
    # Меняем только ЧСС на высокую, оставляя остальные данные нормальными
    normal_ecg_data.heart_rate = 120.0
    
    result = interpret_ecg(normal_ecg_data)
    
    assert result.diagnosis == Diagnosis.TACHYCARDIA, "Ожидалась тахикардия"
    assert result.urgency == Urgency.PLANNED, "Тахикардияв плановом порядке"
