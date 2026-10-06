from ecg_interpreter.ecg.heart_rate_analyser import analyze_heart_rate
from ecg_interpreter.ecg.validators import validate_dataset, validate_data
from ecg_interpreter.models.ecg_data import ECGData, STSegment, Rhythm
from ecg_interpreter.models.interpretation import Interpretation, Diagnosis, Urgency


def interpret_ecg(data: ECGData) -> Interpretation:
    """
    Интерпретация данных ЭКГ и получение диагноза и степени срочности.

    :param data: Данные ЭКГ.
    :return: Результат интерпретации входных данных - диагноз и степень срочности.
    """
    validate_data(data)

    if data.st_segment == STSegment.ELEVATION and data.q_wave:
        return Interpretation(Diagnosis.INFARCTION, Urgency.URGENT)

    if data.st_segment == STSegment.ELEVATION:
        return Interpretation(Diagnosis.SUSPECTED_INFARCTION, Urgency.URGENT)

    if data.st_segment == STSegment.DEPRESSION:
        return Interpretation(Diagnosis.ISCHEMIA, Urgency.PLANNED)

    if data.rhythm == Rhythm.IRREGULAR:
        return Interpretation(Diagnosis.ARRHYTHMIA, Urgency.PLANNED)

    if data.q_wave:
        return Interpretation(Diagnosis.PREVIOUS_INFARCTION, Urgency.PLANNED)

    hr_analysis = analyze_heart_rate(data.heart_rate)
    return Interpretation(
        hr_analysis,
        Urgency.NONE if hr_analysis == Diagnosis.NORMAL else Urgency.PLANNED,
    )


def filter_by_urgency(dataset: list[ECGData], urgency: Urgency) -> list[ECGData]:
    """
    Фильтрация списка данных ЭКГ по указанной степени срочности.

    :param dataset: список данных ЭКГ.
    :param urgency: степень срочности.
    :return: список данных ЭКГ с указанной степенью срочности.
    """
    validate_dataset(dataset)

    return [d for d in dataset if interpret_ecg(d).urgency == urgency]


def filter_by_diagnosis(dataset: list[ECGData], diagnosis: Diagnosis) -> list[ECGData]:
    """
    Фильтрация списка данных ЭКГ по указанному диагнозу.

    :param dataset: список данных ЭКГ.
    :param diagnosis: диагноз.
    :return: список данных ЭКГ с указанным диагнозом.
    """
    validate_dataset(dataset)
    return [d for d in dataset if interpret_ecg(d).diagnosis == diagnosis]
