# Автоматическая интерпретация ЭКГ — учебный проект по тестированию и автоматизации

Учебный проект для курса **«Автоматизация и тестирование программного обеспечения»**.

Проект предназначен для изучения:

- основ тестирования ПО;
- техник тест-дизайна;
- написания unit-тестов на Python;
- работы с `pytest`;
- использования фикстур;
- параметризации тестов;
- проверки исключений;
- работы с `dataclass` и `Enum`;
- взаимодействия с Git и GitHub.

Проект реализует упрощённую модель автоматической интерпретации ЭКГ.

> **Важно:** проект является учебным и не предназначен для медицинской диагностики, лечения или принятия клинических решений.

---

## Содержание

- [Цель проекта](#цель-проекта)
- [Технологии](#технологии)
- [Структура проекта](#структура-проекта)
- [Быстрый старт](#быстрый-старт)
- [Запуск тестов](#запуск-тестов)
- [Пример использования](#пример-использования)
- [Функции приложения](#функции-приложения)
- [Правила интерпретации ЭКГ](#правила-интерпретации-экг)
- [Правила анализа ЧСС](#правила-анализа-чсс)
- [Тестирование](#тестирование)
- [Фикстуры](#фикстуры)
- [Параметризация](#параметризация)
- [Работа с GitHub](#работа-с-github)
- [Требования к тестам](#требования-к-тестам)
- [Дисклеймер](#дисклеймер)

---

## Цель проекта

Проект создан для практического освоения автоматизации тестирования на примере небольшого предметного модуля.

В процессе работы с проектом студенты учатся:

- писать модульные тесты для отдельных функций;
- применять граничные значения и классы эквивалентности;
- проверять таблицы решений;
- использовать фикстуры для устранения дублирования;
- параметризовать тесты;
- проверять исключения через `pytest.raises`;
- сравнивать числа с плавающей точкой через `pytest.approx`;
- оформлять тестовую структуру проекта;
- сдавать задания через Git/GitHub.

---

## Технологии

- **Язык:** Python 3.10+
- **Тестирование:** pytest
- **Модели данных:** `dataclass`, `Enum`
- **Контроль версий:** Git / GitHub

Проект намеренно имеет минимальное количество зависимостей.

---

## Структура проекта

```text
.
├── src/
│   └── ecg_interpreter/
│       ├── ecg.py
│       └── models/
│           ├── ecg_data.py
│           └── interpretation.py
├── tests/
│   ├── conftest.py
│   └── test_ecg.py
├── pyproject.toml
├── README.md
└── AGENTS.md
```

Основные модули:

- `src/ecg_interpreter/ecg.py` — основная логика интерпретации ЭКГ;
- `src/ecg_interpreter/models/ecg_data.py` — модель измерения ЭКГ;
- `src/ecg_interpreter/models/interpretation.py` — модели результата интерпретации;
- `tests/conftest.py` — фикстуры для тестов;
- `tests/test_ecg.py` — unit-тесты.

---

## Быстрый старт

### 1. Клонируйте репозиторий

```bash
git clone <url-репозитория>
cd <имя-репозитория>
```

### 2. Создайте виртуальное окружение

```bash
python -m venv .venv
```

Активация для Linux/macOS:

```bash
source .venv/bin/activate
```

Активация для Windows:

```bash
.venv\Scripts\activate
```

### 3. Установите зависимости

Для проекта достаточно установить `pytest`:

```bash
pip install pytest
```

---

## Запуск тестов

Запуск всех тестов:

```bash
pytest
```

Подробный вывод:

```bash
pytest -v
```

Запуск только тестов для конкретной функции:

```bash
pytest -k analyze_heart_rate -v
pytest -k interpret_ecg -v
pytest -k average_heart_rate -v
pytest -k find_critical -v
```

Запуск конкретного тестового файла:

```bash
pytest tests/test_ecg.py -v
```

---

## Пример использования

Пример создания измерения ЭКГ и его интерпретации:

```python
from src.ecg_interpreter.models.ecg_data import (
    ECGData,
    Rhythm,
    STSegment,
)
from src.ecg_interpreter.ecg import interpret_ecg

reading = ECGData(
    heart_rate=75,
    rhythm=Rhythm.REGULAR,
    st_segment=STSegment.NORMAL,
    q_wave=False,
)

result = interpret_ecg(reading)

print(result.diagnosis)
print(result.urgency)
```

Ожидаемый результат для нормы:

```text
Diagnosis.NORMAL
Urgency.NONE
```

---

## Функции приложения

### `analyze_heart_rate`

Классифицирует ЧСС по порогам:

```text
< 60       -> BRADYCARDIA
60 - 100   -> NORMAL
> 100      -> TACHYCARDIA
```

Также функция выбрасывает `ValueError` для некорректных значений:

```text
None   -> ValueError
< 0    -> ValueError
> 300  -> ValueError
```

---

### `interpret_ecg`

Интерпретирует одно измерение ЭКГ по упрощённой таблице решений.

Возвращает объект `Interpretation`, содержащий:

- диагноз;
- уровень срочности.

---

### `average_heart_rate`

Вычисляет среднюю ЧСС по списку измерений.

Для пустого списка выбрасывает:

```text
ValueError
```

---

### `find_critical`

Возвращает список измерений, для которых интерпретация имеет статус:

```text
Urgency.URGENT
```

---

## Правила интерпретации ЭКГ

Правила применяются по приоритету. Более приоритетные правила проверяются раньше.

| Приоритет | Условие                                               | Диагноз                                | Срочность            |
|-----------|-------------------------------------------------------|----------------------------------------|----------------------|
| 1         | `ST elevation` + `q_wave == True`                     | `INFARCTION`                           | `URGENT`             |
| 2         | `ST elevation` без `q_wave`                           | `SUSPECTED_INFARCTION`                 | `URGENT`             |
| 3         | `ST depression`                                       | `ISCHEMIA`                             | `PLANNED`            |
| 4         | Нерегулярный ритм                                     | `ARRHYTHMIA`                           | `PLANNED`            |
| 5         | `q_wave == True` при нормальном ST и регулярном ритме | `PREVIOUS_INFARCTION`                  | `PLANNED`            |
| 6         | Анализ ЧСС                                            | `NORMAL`, `BRADYCARDIA`, `TACHYCARDIA` | `NONE` или `PLANNED` |

---

## Правила анализа ЧСС

| ЧСС       | Результат     |
|-----------|---------------|
| `0`       | `BRADYCARDIA` |
| `59.9`    | `BRADYCARDIA` |
| `60`      | `NORMAL`      |
| `75`      | `NORMAL`      |
| `100`     | `NORMAL`      |
| `100.1`   | `TACHYCARDIA` |
| `101`     | `TACHYCARDIA` |
| `300`     | `TACHYCARDIA` |
| `300.001` | `ValueError`  |
| `-1`      | `ValueError`  |
| `None`    | `ValueError`  |

---

## Тестирование

Проект покрыт тестами на `pytest`.

Тесты проверяют:

- нормальные сценарии;
- граничные значения;
- исключения;
- приоритеты правил интерпретации;
- работу со списками измерений;
- корректность возвращаемых диагнозов и уровней срочности;
- поведение функций при пустых и некорректных входных данных.

Рекомендуемая структура тестов:

```text
tests/
├── conftest.py
└── test_ecg.py
```

---

## Фикстуры

Фикстуры используются для создания повторяющихся тестовых данных.

Примеры фикстур:

```python
normal_reading
bradycardia_reading
tachycardia_reading
arrhythmia_reading
ischemia_reading
suspected_infarction_reading
infarction_reading
previous_infarction_reading
critical_dataset
non_critical_dataset
empty_dataset
```

Пример использования фикстуры:

```python
def test_interpret_normal(normal_reading):
    result = interpret_ecg(normal_reading)

    assert result.diagnosis == Diagnosis.NORMAL
    assert result.urgency == Urgency.NONE
```

Также рекомендуется использовать фабрику фикстур:

```python
@pytest.fixture
def make_reading():
    def _make(
        *,
        heart_rate: float = 75.0,
        rhythm: Rhythm = Rhythm.REGULAR,
        st_segment: STSegment = STSegment.NORMAL,
        q_wave: bool = False,
    ) -> ECGData:
        return ECGData(
            heart_rate=heart_rate,
            rhythm=rhythm,
            st_segment=st_segment,
            q_wave=q_wave,
        )

    return _make
```

---

## Параметризация

Для проверки нескольких входных значений используется `@pytest.mark.parametrize`.

Пример:

```python
import pytest

from src.ecg_interpreter.ecg import analyze_heart_rate
from src.ecg_interpreter.models.interpretation import Diagnosis


@pytest.mark.parametrize(
    ("heart_rate", "expected"),
    [
        (59, Diagnosis.BRADYCARDIA),
        (60, Diagnosis.NORMAL),
        (100, Diagnosis.NORMAL),
        (101, Diagnosis.TACHYCARDIA),
    ],
)
def test_analyze_heart_rate(heart_rate, expected):
    assert analyze_heart_rate(heart_rate) == expected
```

Для передачи фикстур в параметризованный тест можно использовать имя фикстуры и `request.getfixturevalue`:

```python
@pytest.mark.parametrize(
    ("reading_fixture", "expected_diagnosis"),
    [
        ("normal_reading", Diagnosis.NORMAL),
        ("infarction_reading", Diagnosis.INFARCTION),
    ],
)
def test_interpret(request, reading_fixture, expected_diagnosis):
    reading = request.getfixturevalue(reading_fixture)

    result = interpret_ecg(reading)

    assert result.diagnosis == expected_diagnosis
```

---

## Работа с GitHub

Для сдачи заданий рекомендуется использовать следующий процесс:

1. Создать ветку от основной ветки репозитория.
2. Выполнить задание.
3. Написать тесты.
4. Запустить тесты локально.
5. Сделать коммит с понятным сообщением.
6. Открыть pull request.
7. Дождаться проверки преподавателем или автоматической проверки.

Примеры названий веток:

```text
lab/unit-tests
lab/pytest-fixtures
feature/add-decision-table-tests
fix/boundary-values
```

Примеры сообщений коммитов:

```text
Add tests for analyze_heart_rate
Add fixtures for ECG readings
Fix boundary tests for heart rate
Update interpretation decision table tests
```

---

## Требования к тестам

При написании тестов необходимо соблюдать следующие требования:

- тесты должны быть изолированными;
- тесты должны быть детерминированными;
- тесты не должны зависеть от сети, времени или случайных данных;
- повторяющиеся объекты следует выносить в фикстуры;
- граничные значения следует выносить в параметризацию;
- исключения следует проверять через `pytest.raises`;
- числа с плавающей точкой следует сравнивать через `pytest.approx`;
- имена тестов должны описывать проверяемое поведение.

Хорошие имена тестов:

```python
test_analyze_heart_rate_boundary_60_returns_normal
test_interpret_ecg_elevation_with_q_wave_returns_infarction
test_average_heart_rate_empty_dataset_raises_error
test_find_critical_returns_only_urgent_readings
```

### Настройка `pytest`

Для корректной работы импортов из `src` рекомендуется добавить в `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
```

---

### `q_wave`

В текущей версии модели `ECGData` поле `q_wave` имеет тип `bool`:

```python
q_wave: bool
```

В тестах следует использовать:

```python
q_wave=True
q_wave=False
```

---

## Дисклеймер

Проект носит исключительно учебный характер.

Логика интерпретации ЭКГ намеренно упрощена. Проект не заменяет медицинские алгоритмы, клинические рекомендации и профессиональную врачебную оценку.

Не используйте данный проект для принятия решений, связанных со здоровьем, диагностикой или лечением людей.