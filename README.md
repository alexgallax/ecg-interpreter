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
- [Известные ограничения](#известные-ограничения)
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

- **Язык:** Python; в `pyproject.toml` заявлено 3.10+, текущий код проверен на 3.14.5
- **Тестирование:** pytest
- **Модели данных:** `dataclass`, `Enum`
- **Контроль версий:** Git / GitHub

Проект намеренно имеет минимальное количество зависимостей.

Для запуска текущей реализации используйте Python 3.14. Модели содержат аннотации с Enum, объявленными ниже, без `from __future__ import annotations`; на Python 3.10–3.13 это приводит к `NameError` при импорте. Заявленная совместимость требует исправления и отдельной проверки.

---

## Структура проекта

```text
.
├── src/
│   └── ecg_interpreter/
│       ├── __init__.py
│       ├── consts/
│       │   ├── __init__.py
│       │   └── consts.py
│       ├── ecg/
│       │   ├── __init__.py
│       │   ├── heart_rate_analyser.py
│       │   ├── interpreter.py
│       │   ├── risk_analyser.py
│       │   └── validators.py
│       └── models/
│           ├── __init__.py
│           ├── ecg_data.py
│           └── interpretation.py
├── pyproject.toml
├── requirements.txt
├── README.md
└── AGENTS.md
```

Основные модули:

- `src/ecg_interpreter/ecg/interpreter.py` — интерпретация и фильтрация измерений;
- `src/ecg_interpreter/ecg/heart_rate_analyser.py` — классификация ЧСС, среднее и диапазон;
- `src/ecg_interpreter/ecg/risk_analyser.py` — учебный показатель риска;
- `src/ecg_interpreter/ecg/validators.py` — проверки входных данных;
- `src/ecg_interpreter/consts/consts.py` — пороги ЧСС и таблицы коэффициентов риска;
- `src/ecg_interpreter/models/ecg_data.py` — модель измерения ЭКГ;
- `src/ecg_interpreter/models/interpretation.py` — модели результата интерпретации;
- `tests/conftest.py` — фикстуры для тестов;
- `tests/test_ecg.py` — unit-тесты.

Пакет импортируется как `ecg_interpreter`, без префикса `src`. Файлы `__init__.py` пустые: функции нужно импортировать из конкретных модулей, например `ecg_interpreter.ecg.interpreter`.

---

## Быстрый старт

### 1. Клонируйте репозиторий

```bash
git clone <url-репозитория>
cd <имя-репозитория>
```

### 2. Создайте виртуальное окружение

```bash
python3.14 -m venv .venv
```

На Windows можно использовать `py -3.14 -m venv .venv`.

Активация для Linux/macOS:

```bash
source .venv/bin/activate
```

Активация для Windows:

```bash
.venv\Scripts\activate
```

### 3. Установите зависимости

Установите пакет в editable-режиме вместе с зависимостями для тестов из `pyproject.toml`:

```bash
python -m pip install -e ".[test]"
```

Это обеспечивает импорты приложения вне pytest, в том числе для примера ниже. `requirements.txt` содержит фиксированные версии тестового окружения; при необходимости вместо test extra можно выполнить `python -m pip install -r requirements.txt` и `python -m pip install -e .`.

---

## Запуск тестов

Команды выполнять из корня проекта в активированном виртуальном окружении. Без активации на Linux/macOS можно запустить `.venv/bin/python -m pytest -v`, на Windows — `.venv\Scripts\python.exe -m pytest -v`.

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
pytest -k heart_rate_range -v
pytest -k filter_by_urgency -v
pytest -k filter_by_diagnosis -v
pytest -k risk_score -v
```

Сейчас тесты есть только для `interpret_ecg`. Остальные фильтры `-k` пока не выбирают тестов и пригодятся при расширении покрытия.

Запуск конкретного тестового файла:

```bash
pytest tests/test_ecg.py -v
```

---

## Пример использования

Пример создания измерения ЭКГ и его интерпретации:

```python
from ecg_interpreter.models.ecg_data import (
    ECGData,
    Rhythm,
    STSegment,
)
from ecg_interpreter.ecg.interpreter import interpret_ecg

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
nan    -> ValueError
inf    -> ValueError
-inf   -> ValueError
```

---

### `interpret_ecg`

Интерпретирует одно измерение ЭКГ по упрощённой таблице решений.

Возвращает объект `Interpretation`, содержащий:

- диагноз;
- уровень срочности.

`None` вызывает `ValueError("Данные ЭКГ не могут быть пустыми")`. ЧСС проверяется только при переходе к последнему правилу; первые пять правил возвращают результат без её анализа.

---

### `average_heart_rate`

Вычисляет среднюю ЧСС по списку измерений.

Для пустого списка и `None` выбрасывает:

```text
ValueError("Список измерений не может быть пустым")
```

ЧСС отдельных измерений не валидируется: отрицательные значения и значения выше `300` участвуют в среднем, `nan` и бесконечности обрабатываются обычной арифметикой Python.

---

### `heart_rate_range`

Возвращает пару `(минимальная ЧСС, максимальная ЧСС)`. Не вызывает валидаторы: пустой список вызывает нативный `ValueError` из `min`, `None` вместо списка — `TypeError`. ЧСС элементов не проверяется; при `nan` результат может зависеть от порядка измерений.

---

### `filter_by_urgency` и `filter_by_diagnosis`

Отбирают измерения по срочности или диагнозу, полученным через `interpret_ecg`. Возвращают новый список исходных объектов, сохраняя порядок и повторы. Исходные данные не изменяются.

Пустой набор и `None` вызывают `ValueError("Список измерений не может быть пустым")`. Если в непустом наборе нет совпадений, возвращается `[]`. Критерий фильтра не валидируется, ошибки интерпретации элементов распространяются вызывающему коду.

Отбор срочных измерений:

```python
from ecg_interpreter.ecg.interpreter import filter_by_urgency
from ecg_interpreter.models.interpretation import Urgency

critical_readings = filter_by_urgency(dataset, Urgency.URGENT)
```

В этом фрагменте `dataset` — заранее созданный непустой список `ECGData`. Отдельной функции `find_critical` в проекте нет.

---

### `risk_score`

Вычисляет учебный показатель риска. Проверяет наличие измерения и допустимость ЧСС до интерпретации, в том числе при признаках инфаркта.

Текущая формула реализации:

```text
base_by_urgency * heart_rate_component * multiplier_by_diagnosis
```

База по срочности: `NONE=0.0`, `PLANNED=25.0`, `URGENT=80.0`. Компонент ЧСС равен `0.0` для нормы и `0.2` для бради-/тахикардии: значения `5.0` из `RISK_BY_HEART_RATE` заменяются в коде.

Множители диагноза: `NORMAL=1.0`, `BRADYCARDIA=1.2`, `TACHYCARDIA=1.2`, `ARRHYTHMIA=1.4`, `PREVIOUS_INFARCTION=1.45`, `ISCHEMIA=1.5`, `SUSPECTED_INFARCTION=1.8`, `INFARCTION=2.0`.

При нормальной ЧСС результат сейчас равен нулю даже для инфаркта. Формула расходится с docstring; это известное несоответствие, а не подтверждённое требование к алгоритму.

---

### `validate_dataset`, `validate_data`, `validate_heart_rate`

- `validate_dataset` проверяет только непустоту набора, без проверки элементов или типа контейнера.
- `validate_data` проверяет только истинность входного значения, без проверки типа объекта и его полей.
- `validate_heart_rate` проверяет `None`, нижнюю и верхнюю границы, затем конечность числа.
- При успешной проверке валидаторы возвращают `None`.

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

Для корректного булева `q_wave` таблица описывает поведение полностью. Реализация использует truthiness, а не строгое сравнение с `True`. Модели `ECGData` и `Interpretation` — изменяемые `dataclass` с обязательными полями, без автоматической проверки типов. Перечисления наследуются от `str` и `Enum`.

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
| `nan`     | `ValueError`  |
| `inf`     | `ValueError`  |
| `-inf`    | `ValueError`  |

Сообщения ошибок:

| Значение | Сообщение |
|----------|-----------|
| `None` | `Значение ЧСС не может быть пустыми` |
| Отрицательное, включая `-inf` | `Значение ЧСС не может быть отрицательным` |
| Выше `300`, включая `inf` | `Значение ЧСС физиологически невозможно` |
| `nan` | `Значение ЧСС должно быть конечным числом` |

## Известные ограничения

- Заявленная поддержка Python 3.10+ пока не соответствует аннотациям моделей; текущий запуск проверен на Python 3.14.5.
- Docstring `risk_score` описывает `(база + компонент ЧСС) * множитель`, но реализация выполняет умножение базы на компонент. Формулу нужно согласовать перед исправлением и закреплением ожидаемых результатов тестами.
- Валидация различается между функциями: агрегаты не проверяют ЧСС элементов, `interpret_ecg` проверяет её только в последней ветви, а `risk_score` — всегда.
- Проверки типов моделей и критериев фильтрации отсутствуют. Аннотации типов не являются runtime-валидацией.

---

## Тестирование

Рекомендуемая структура для автотестов:

```text
tests/
├── conftest.py
├── test_validators.py
├── test_heart_rate_analyser.py
├── test_interpreter.py
├── test_risk_analyser.py
├── test_models.py
└── test_consts.py
```

Разделение соответствует модулям приложения.

---

## Фикстуры

Фикстуры используются для создания повторяющихся тестовых данных.

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

from ecg_interpreter.ecg.heart_rate_analyser import analyze_heart_rate
from ecg_interpreter.models.interpretation import Diagnosis


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
test_filter_by_urgency_returns_only_urgent_readings
```

### Настройка `pytest`

В `pyproject.toml` уже настроены поиск тестов и путь импорта пакета из `src`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
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
