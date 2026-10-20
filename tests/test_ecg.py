import pytest
from ecg_interpreter.ecg.interpreter import interpret_ecg
from ecg_interpreter.models.interpretation import Interpretation, Diagnosis, Urgency



#проверять граничные значения, в основном позитивные сценарии

@pytest.mark.parametrize("fixture_name, expected", [
    ("normal_data_ecg", Interpretation(Diagnosis.NORMAL, Urgency.NONE)),
    ("infarction_ecg", Interpretation(Diagnosis.INFARCTION, Urgency.URGENT)),
    ("ischemia_ecg", Interpretation(Diagnosis.ISCHEMIA, Urgency.PLANNED)),
    ("infarction_risk_ecg", Interpretation(Diagnosis.SUSPECTED_INFARCTION, Urgency.URGENT)),
    ("previous_infarction_ecg", Interpretation(Diagnosis.PREVIOUS_INFARCTION, Urgency.PLANNED)),
    ("arrhythmia_ecg", Interpretation(Diagnosis.ARRHYTHMIA, Urgency.PLANNED)),
    ("bradycardia_ecg", Interpretation(Diagnosis.BRADYCARDIA, Urgency.PLANNED)),
    ("tachycardia_ecg", Interpretation(Diagnosis.TACHYCARDIA, Urgency.PLANNED)),
],
    ids=["normal", "infarction", "ischemia", "infarction_risk", "previous_infarction", "arrythmia", "bradycardia", "tachycardia"]
) 


def test_interpret_ecg(request: pytest.FixtureRequest, fixture_name, expected) :
        data = request.getfixturevalue(fixture_name)
        result = interpret_ecg(data)
        assert result == expected, (
        f"На входе {fixture_name} ожидали {expected}, а получили {result}"
    )