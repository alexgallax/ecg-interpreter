import math

from ecg_interpreter.consts.consts import MAX_HEART_RATE
from ecg_interpreter.models.ecg_data import ECGData


def validate_dataset(dataset: list[ECGData]):
    """
    Валидания списка данных ЭКГ.

    Выбрасывает исключения в случаях, если вадидация не пройдена.

    :param dataset: Список данных ЭКГ.
    """
    if not dataset:
        raise ValueError("Список измерений не может быть пустым")


def validate_data(data: ECGData):
    """
    Валидания данных ЭКГ.

    Выбрасывает исключения в случаях, если вадидация не пройдена.

    :param data: Данные ЭКГ.
    """
    if not data:
        raise ValueError("Данные ЭКГ не могут быть пустыми")


def validate_heart_rate(heart_rate: float):
    """
    Валидания значения ЧСС.

    Выбрасывает исключения в случаях, если вадидация не пройдена.

    :param heart_rate: Значение ЧСС.
    """
    if heart_rate is None:
        raise ValueError("Значение ЧСС не может быть пустыми")

    if heart_rate < 0.0:
        raise ValueError("Значение ЧСС не может быть отрицательным")

    if heart_rate > MAX_HEART_RATE:
        raise ValueError("Значение ЧСС физиологически невозможно")\

    if math.isnan(heart_rate) or math.isinf(heart_rate):
        raise ValueError("Значение ЧСС должно быть конечным числом")
