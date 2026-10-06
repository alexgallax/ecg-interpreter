from ecg_interpreter.consts.consts import LOW_HEART_RATE, HIGH_HEART_RATE
from ecg_interpreter.ecg.validators import validate_dataset, validate_heart_rate
from ecg_interpreter.models.ecg_data import ECGData
from ecg_interpreter.models.interpretation import Diagnosis


def analyze_heart_rate(heart_rate: float) -> Diagnosis:
    """
    Анализ сердечного ритма по значению ЧСС.

    :param heart_rate: значение ЧСС (удары в минуту).
    :return: диагноз на основе анализа ЧСС.
    """
    validate_heart_rate(heart_rate)

    if heart_rate < LOW_HEART_RATE:
        return Diagnosis.BRADYCARDIA
    elif heart_rate <= HIGH_HEART_RATE:
        return Diagnosis.NORMAL
    else:
        return Diagnosis.TACHYCARDIA


def average_heart_rate(dataset: list[ECGData]) -> float:
    """
    Вычисление среднего значения ЧСС.

    :param dataset: список данных ЭКГ.
    :return: среднее значение ЧСС в указанном списке данных ЭКГ.
    """
    validate_dataset(dataset)

    total = sum(d.heart_rate for d in dataset)
    return total / len(dataset)


def heart_rate_range(dataset: list[ECGData]) -> tuple[float, float]:
    """
    Нахождения минимального и макксимального значений ЧСС.

    :param dataset: список данных ЭКГ.
    :return: минимальное и макксимальное значения ЧСС в указанном списке данных ЭКГ.
    """
    heart_rates = [d.heart_rate for d in dataset]
    return min(heart_rates), max(heart_rates)
