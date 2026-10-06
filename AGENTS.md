# AGENTS.md

## Назначение проекта

Это учебный проект по курсу **«Автоматизация и Тестирование программного обеспечения»**.

Проект предназначен для изучения и практики:

- основ тестирования программного обеспечения;
- техник тест-дизайна: граничные значения, классы эквивалентности, таблицы решений;
- написания unit-тестов на Python с использованием `pytest`;
- работы с фикстурами;
- параметризации тестов;
- проверки исключений;
- работы с `dataclass` и `Enum`;
- использования GitHub для сдачи и проверки заданий.

Проект реализует упрощённую модель автоматической интерпретации ЭКГ.

> Важно: проект не является медицинским изделием и не предназначен для реальной диагностики, лечения или принятия клинических решений.

---

## Основная цель проекта

Целевой код приложения находится в модуле:

```text
src/ecg_interpreter/
```

Основные функции для тестирования:

- `analyze_heart_rate` — классификация ЧСС;
- `interpret_ecg` — интерпретация измерения ЭКГ по правилам;
- `average_heart_rate` — расчёт средней ЧСС по списку измерений;
- `heart_rate_range` — поиск минимальной и максимальной ЧСС;
- `filter_by_urgency` — фильтрация измерений по срочности;
- `filter_by_diagnosis` — фильтрация измерений по диагнозу;
- `risk_score` — расчёт учебного показателя риска;
- `validate_dataset`, `validate_data`, `validate_heart_rate` — валидация входных данных.

Все изменения и новые задания должны быть связаны с этими функциями, моделями, константами и их тестированием. Функции `find_critical` нет: срочные измерения отбираются через `filter_by_urgency(dataset, Urgency.URGENT)`.

---

## Технологический стек

- Язык: **Python**, в `pyproject.toml` заявлено **3.10+**; текущий код проверен на **3.14.5**
- Тестирование: **pytest**
- Типы данных: `dataclass`, `Enum`
- Организация проекта: `src`-layout
- Система контроля версий: **Git / GitHub**

Не добавлять новые внешние зависимости без явной учебной необходимости.

Известное ограничение: модели используют Enum в аннотациях до объявления этих Enum, без `from __future__ import annotations`. На Python 3.10–3.13 это приводит к `NameError` при импорте. Пока это не исправлено и не проверено тестами совместимости, для запуска текущего кода использовать Python 3.14.

---

## Структура проекта

Текущая структура репозитория (без служебных файлов окружения):

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
├── AGENTS.md
└── README.md
```

Импортировать из пакета `ecg_interpreter`, без префикса `src`. Файлы `__init__.py` сейчас пустые и не реэкспортируют функции. Примеры корректных импортов:

```python
from ecg_interpreter.ecg.heart_rate_analyser import analyze_heart_rate
from ecg_interpreter.ecg.interpreter import interpret_ecg
from ecg_interpreter.models.ecg_data import ECGData
```

Общие валидаторы импортировать напрямую из `ecg_interpreter.ecg.validators`, а не через `interpreter`: это предотвращает циклические зависимости.

---

## Запуск тестов

Тесты должны запускаться из корня проекта.

Следующие команды предполагают активированное виртуальное окружение с установленным test extra (`python -m pip install -e ".[test]"`). На Linux/macOS без активации можно использовать `.venv/bin/python -m pytest -v`; на Windows — `.venv\Scripts\python.exe -m pytest -v`.

Базовый запуск:

```bash
python -m pytest
```

или:

```bash
pytest
```

Подробный запуск:

```bash
python -m pytest -v
```

Запуск конкретного файла:

```bash
python -m pytest tests/test_ecg.py -v
```

Запуск тестов по имени:

```bash
python -m pytest -k "analyze_heart_rate" -v
python -m pytest -k "interpret_ecg" -v
python -m pytest -k "average_heart_rate" -v
python -m pytest -k "heart_rate_range" -v
python -m pytest -k "filter_by_urgency" -v
python -m pytest -k "filter_by_diagnosis" -v
python -m pytest -k "risk_score" -v
```

Если импорты вида `ecg_interpreter...` не работают, проверить:

1. наличие корректного `pyproject.toml`;
2. запуск из корня проекта;
3. наличие `pythonpath` в настройках pytest.

Пример минимальной настройки:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
```

---

## Доменная модель

### `ECGData`

Одно измерение ЭКГ.

Поля:

```python
heart_rate: float
rhythm: Rhythm
st_segment: STSegment
q_wave: bool
```

Важно:

- `q_wave` — это `bool`, а не отдельный `Enum`;
- `heart_rate` — числовое значение ЧСС;
- `rhythm` и `st_segment` — перечисления.

`ECGData` и `Interpretation` — изменяемые `dataclass` без значений по умолчанию и без автоматической валидации типов. `Interpretation` содержит поля `diagnosis: Diagnosis` и `urgency: Urgency`. Все четыре Enum наследуются от `str` и `Enum`.

---

### `Rhythm`

```python
REGULAR = "regular"
IRREGULAR = "irregular"
```

---

### `STSegment`

```python
NORMAL = "normal"
ELEVATION = "elevation"
DEPRESSION = "depression"
```

---

### `Diagnosis`

```python
NORMAL = "normal"
BRADYCARDIA = "bradycardia"
TACHYCARDIA = "tachycardia"
ARRHYTHMIA = "arrhythmia"
ISCHEMIA = "ischemia"
INFARCTION = "infarction"
SUSPECTED_INFARCTION = "suspected infarction"
PREVIOUS_INFARCTION = "previous infarction"
```

---

### `Urgency`

```python
NONE = "none"
PLANNED = "planned"
URGENT = "urgent"
```

---

## Правила интерпретации ЭКГ

Функция `interpret_ecg` реализует упрощённую таблицу решений.

Порядок правил важен. Более приоритетные правила проверяются раньше.

### Приоритет правил

1. Если `STSegment.ELEVATION` и `q_wave` истинно:

   ```text
   Diagnosis.INFARCTION
   Urgency.URGENT
   ```

2. Если `STSegment.ELEVATION`:

   ```text
   Diagnosis.SUSPECTED_INFARCTION
   Urgency.URGENT
   ```

3. Если `STSegment.DEPRESSION`:

   ```text
   Diagnosis.ISCHEMIA
   Urgency.PLANNED
   ```

4. Если `Rhythm.IRREGULAR`:

   ```text
   Diagnosis.ARRHYTHMIA
   Urgency.PLANNED
   ```

5. Если `q_wave` истинно:

   ```text
   Diagnosis.PREVIOUS_INFARCTION
   Urgency.PLANNED
   ```

6. Иначе результат зависит от `analyze_heart_rate`:

   - `BRADYCARDIA` → `Urgency.PLANNED`
   - `TACHYCARDIA` → `Urgency.PLANNED`
   - `NORMAL` → `Urgency.NONE`

---

## Правила ЧСС

Функция `analyze_heart_rate` классифицирует ЧСС так:

```text
heart_rate < 60      -> Diagnosis.BRADYCARDIA
60 <= heart_rate <= 100 -> Diagnosis.NORMAL
heart_rate > 100     -> Diagnosis.TACHYCARDIA
```

Ограничения:

```text
None      -> ValueError
< 0       -> ValueError
> 300     -> ValueError
nan       -> ValueError
inf       -> ValueError
-inf      -> ValueError
```

Граничные значения:

| ЧСС       | Ожидаемый диагноз |
|-----------|-------------------|
| `0`       | `BRADYCARDIA`     |
| `59.9`    | `BRADYCARDIA`     |
| `60`      | `NORMAL`          |
| `100`     | `NORMAL`          |
| `100.1`   | `TACHYCARDIA`     |
| `300`     | `TACHYCARDIA`     |
| `300.001` | `ValueError`      |

---

## Валидация, агрегаты и фильтры

- `validate_dataset` отклоняет пустой набор и другие falsy-входы, включая `None`; элементы и тип контейнера не проверяет.
- `validate_data` отклоняет falsy-входы, включая `None`; тип объекта и поля не проверяет.
- `validate_heart_rate` последовательно проверяет `None`, отрицательное значение, превышение `300`, затем `nan`/`inf`. Поэтому `-inf` получает сообщение об отрицательной ЧСС, `inf` — о физиологически невозможной, а `nan` — о конечном числе.
- Валидаторы при успехе возвращают `None`.
- `average_heart_rate` проверяет набор через `validate_dataset`, затем вычисляет `sum(d.heart_rate for d in dataset) / len(dataset)`. ЧСС отдельных измерений не валидируется.
- `heart_rate_range` возвращает `(min(heart_rates), max(heart_rates))` без вызова валидаторов. Пустой набор вызывает нативный `ValueError` из `min`; `None` вместо набора вызывает `TypeError`. При `nan` результат может зависеть от порядка элементов.
- `filter_by_urgency` и `filter_by_diagnosis` проверяют набор и отбирают измерения по результату `interpret_ecg`. Пустой набор вызывает `ValueError`, отсутствие совпадений в непустом наборе возвращает `[]`.
- Фильтры возвращают новый список исходных объектов, сохраняют порядок и повторы. Критерий фильтра не валидируется; неизвестный критерий даёт `[]` при корректных измерениях. Ошибки интерпретации элементов распространяются вызывающему коду.
- Функции приложения не изменяют входные измерения и наборы.

## Расчёт риска: текущее поведение

`risk_score` сначала вызывает `validate_data` и `validate_heart_rate`, поэтому проверяет ЧСС даже при ранних диагностических правилах. Затем получает интерпретацию, компонент ЧСС и коэффициент диагноза из таблиц в `consts/consts.py`.

Фактическая формула:

```text
base_by_urgency * heart_rate_component * multiplier_by_diagnosis
```

База: `NONE=0.0`, `PLANNED=25.0`, `URGENT=80.0`. При нормальной ЧСС компонент равен `0.0`, а при бради-/тахикардии значения `5.0` из таблицы заменяются на `0.2`.

Множители: `NORMAL=1.0`, `BRADYCARDIA=1.2`, `TACHYCARDIA=1.2`, `ARRHYTHMIA=1.4`, `PREVIOUS_INFARCTION=1.45`, `ISCHEMIA=1.5`, `SUSPECTED_INFARCTION=1.8`, `INFARCTION=2.0`.

Известное несоответствие: docstring обещает сложение базы и компонента ЧСС, но код их перемножает. При нормальной ЧСС риск равен нулю даже для инфаркта. Не исправлять формулу молча: изменение требует отдельного решения, тестов и обновления документации. Тесты текущего поведения должны явно отличаться от требований к предполагаемой исправленной формуле.

## Текущее покрытие тестами

В `tests/test_ecg.py` один параметризованный тест проверяет три случая `interpret_ecg`: норму, брадикардию и тахикардию, включая срочность. Границы, исключения, приоритеты, агрегаты, фильтры и риск пока не покрыты.

В `tests/conftest.py` есть фикстуры `normal_reading`, `infarction_reading`, `bradycardia_reading`, `tachycardia_reading`, `arrhythmia_reading`, `ischemia_reading`. Фабрика и наборы измерений ниже описаны как рекомендации, а не как существующие фикстуры.

---

## Общие правила для агента

### Можно и нужно

- писать и улучшать тесты;
- использовать фикстуры;
- использовать параметризацию;
- проверять граничные значения;
- проверять исключения;
- проверять приоритеты правил;
- улучшать читаемость тестов;
- добавлять понятные `id` для `pytest.param`;
- сохранять учебный характер проекта.

### Нельзя

- превращать проект в реальную медицинскую систему;
- добавлять реальные данные пациентов;
- использовать внешние API без разрешения;
- добавлять базу данных, веб-интерфейс или тяжелые зависимости без отдельной задачи;
- менять диагностическую логику без обновления тестов;
- удалять существующие тесты без причины;
- менять сообщения об ошибках без обновления тестов;
- молча переименовывать модули, если это ломает импорты;
- использовать `print` вместо ассертов;
- писать тесты, зависящие от времени, сети, случайности или внешнего окружения.

---

## Требования к тестам

Все тесты должны быть:

- детерминированными;
- изолированными;
- читаемыми;
- быстрыми;
- ориентированными на поведение функции;
- не зависящими от порядка выполнения.

---

## Обязательное использование фикстур

В проекте принято использовать фикстуры для:

- одиночных измерений ЭКГ;
- наборов измерений;
- фабрики объектов `ECGData`.

Пример фабрики:

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

Не следует создавать одинаковые объекты `ECGData` напрямую во многих тестах. Лучше вынести их в фикстуры.

---

## Обязательное использование параметризации

Параметризация должна использоваться для:

- граничных значений ЧСС;
- таблицы решений;
- наборов данных;
- проверки исключений;
- проверки разных фикстур через имена.

Пример параметризации имени фикстуры:

```python
@pytest.mark.parametrize(
    ("reading_fixture", "expected_diagnosis"),
    [
        ("normal_reading", Diagnosis.NORMAL),
        ("infarction_reading", Diagnosis.INFARCTION),
    ],
)
def test_interpret(request: pytest.FixtureRequest, reading_fixture, expected_diagnosis):
    reading = request.getfixturevalue(reading_fixture)

    result = interpret_ecg(reading)

    assert result.diagnosis == expected_diagnosis
```

---

## Требования к именам тестов

Имя теста должно описывать поведение.

Хорошие примеры:

```python
def test_analyze_heart_rate_boundary_60_returns_normal():
    ...


def test_interpret_ecg_elevation_with_q_wave_returns_infarction():
    ...


def test_average_heart_rate_empty_dataset_raises_error():
    ...


def test_filter_by_urgency_returns_only_urgent_readings():
    ...
```

Плохие примеры:

```python
def test_1():
    ...


def test_ecg():
    ...


def test_function():
    ...
```

---

## Требования к именам фикстур

Имена фикстур должны быть понятными и предметными.

Хорошие примеры:

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

Плохие примеры:

```python
data
fixture1
obj
tmp
x
```

---

## Требования к ассертам

Предпочтительно проверять конкретное поведение.

Хорошо:

```python
assert result == Interpretation(Diagnosis.INFARCTION, Urgency.URGENT)
```

Для чисел с плавающей точкой использовать:

```python
assert average_heart_rate(dataset) == pytest.approx(83.75)
```

Для исключений использовать:

```python
with pytest.raises(ValueError, match="Список измерений не может быть пустым"):
    average_heart_rate([])
```

---

## Работа с исключениями

Если функция должна бросать исключение, тест обязан проверить:

1. тип исключения;
2. сообщение или его часть.

Пример:

```python
with pytest.raises(ValueError, match="физиологически невозможно"):
    analyze_heart_rate(301)
```

Если сообщение об ошибке меняется, нужно обновить соответствующие тесты.

---

## Работа с сообщениями об ошибках

Текущие сообщения об ошибках являются частью контракта; новые тесты исключений должны их проверять.

Например:

```python
"Данные ЭКГ не могут быть пустыми"
"Список измерений не может быть пустым"
"Значение ЧСС не может быть пустыми"
"Значение ЧСС не может быть отрицательным"
"Значение ЧСС физиологически невозможно"
"Значение ЧСС должно быть конечным числом"
```

Если агент меняет текст сообщения, он обязан обновить все тесты, которые используют `match=...`.

---

## Особенности текущей реализации

### `q_wave` — булево значение

В текущей версии:

```python
q_wave: bool
```

Не следует без необходимости заменять `bool` на `Enum`.

Реализация проверяет truthiness `q_wave`, а не `q_wave is True`. Тип поля автоматически не проверяется; в обычных предметных сценариях использовать `True` и `False`.

---

### Приоритеты правил важны

Например, если есть:

```python
st_segment = STSegment.ELEVATION
q_wave = True
rhythm = Rhythm.IRREGULAR
```

ожидаемый результат:

```python
Diagnosis.INFARCTION
Urgency.URGENT
```

потому что правило инфаркта имеет более высокий приоритет, чем аритмия.

Тесты должны явно проверять такие приоритеты.

---

### Анализ ЧСС вызывается не всегда

Функция `interpret_ecg` вызывает `analyze_heart_rate` только если доходит до правил, связанных с ЧСС.

Например, при элевации ST результат может быть получен до анализа ЧСС.

Это поведение может быть покрыто отдельными тестами.

---

## Как добавлять новую функцию

Если добавляется новая функция, агент должен:

1. Понять её назначение.
2. Определить входные и выходные данные.
3. Определить нормальные сценарии.
4. Определить граничные значения.
5. Определить ошибочные сценарии.
6. Написать тесты.
7. При необходимости добавить фикстуры.
8. Запустить тесты.
9. Обновить документацию, если поведение влияет на правила проекта.

---

## Как изменять существующую логику

Перед изменением логики нужно:

1. Запустить существующие тесты.
2. Понять, какие тесты описывают текущее поведение.
3. Изменить код.
4. Обновить тесты, если поведение меняется намеренно.
5. Добавить новые тесты для изменённого поведения.
6. Убедиться, что все тесты проходят.
7. Обновить `AGENTS.md`, если изменились правила, структура или контракты.

Запрещено менять логику так, чтобы тесты падали, без явного объяснения причины.

---

## Как писать тесты для таблицы решений

Для `interpret_ecg` желательно покрывать каждое правило отдельно.

Минимальный набор сценариев:

- норма;
- брадикардия;
- тахикардия;
- аритмия;
- ишемия;
- подозрение на инфаркт;
- инфаркт;
- возможный перенесённый инфаркт;
- приоритет инфаркта над другими правилами;
- приоритет ишемии над аритмией и `q_wave`;
- приоритет аритмии над `q_wave`;
- `None` вместо `ECGData`;
- некорректная ЧСС, если управление доходит до `analyze_heart_rate`.

---

## Рекомендованный стиль кода

- использовать английский язык для идентификаторов;
- использовать русский язык в документации и комментариях, если это удобно для учебного процесса;
- использовать type hints;
- использовать `Enum` вместо магических строк;
- использовать `dataclass` для простых структур данных;
- не использовать глобальное состояние;
- не использовать побочные эффекты в чистых функциях;
- не мутировать входные данные без необходимости.

---

## Работа с фикстурами и типизацией

Для типизации встроенной фикстуры `request` использовать:

```python
import pytest


def test_example(request: pytest.FixtureRequest):
    reading = request.getfixturevalue("normal_reading")
```

Если нужен более строгий тип, можно использовать `typing.cast`:

```python
from typing import cast

reading = cast(ECGData, request.getfixturevalue("normal_reading"))
```

---

## Требования к `conftest.py`

В файле `tests/conftest.py` рекомендуется хранить:

- фабрику измерений `make_reading`;
- часто используемые одиночные измерения;
- наборы измерений;
- пустые наборы;
- вспомогательные фикстуры для тестов.

Не следует дублировать одни и те же объекты в разных тестовых файлах.

---

## Организация тестовых файлов

При написании автотестов рекомендуется разделение по модулям приложения:

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

Внутри файла можно группировать тесты по функциям:

```python
class TestAnalyzeHeartRate:
    ...


class TestInterpretEcg:
    ...


class TestAverageHeartRate:
    ...


class TestHeartRateRange:
    ...


class TestFilterByUrgency:
    ...


class TestFilterByDiagnosis:
    ...


class TestRiskScore:
    ...
```

Допустимо использовать отдельные функции вместо классов, если тестов немного.

---

## Работа с GitHub

### Имена веток

Рекомендуемые форматы:

```text
lab/unit-tests
lab/pytest-fixtures
feature/add-filter-by-urgency-tests
fix/heart-rate-boundary
docs/update-agents-md
```

### Имена коммитов

Коммиты должны быть понятными.

Хорошо:

```text
Add boundary tests for analyze_heart_rate
Fix expected urgency for tachycardia
Add fixture for suspected infarction
Update decision table tests
```

Плохо:

```text
fix
tests
lab
update code
```

---

## Требования к pull request

Pull request должен содержать:

- понятное название;
- описание изменений;
- результаты запуска тестов или подтверждение, что тесты пройдены;
- ссылку на задание, если есть;
- список изменённых файлов, если менялась логика.

Желательный шаблон описания:

```text
## Что сделано

- Добавлены тесты для ...
- Исправлена ошибка в ...
- Обновлены фикстуры ...

## Как проверял

- [ ] Запустил `pytest -v`
- [ ] Все тесты проходят
- [ ] Новые тесты покрывают изменения
```

---

## Минимальные критерии готовности

Задача считается выполненной, если:

- код запускается;
- тесты написаны для всех изменённых или добавленных функций;
- используются фикстуры;
- используется параметризация там, где это уместно;
- проверены граничные значения;
- проверены исключения;
- нет падающих тестов;
- нет несвязанных изменений;
- сообщения об ошибках согласованы с тестами;
- проект запускается командой `pytest` из корня репозитория.

---

## Типичные ошибки

### 1. Тест пытается передать фикстуру напрямую в `parametrize`

Неправильно:

```python
@pytest.mark.parametrize("reading", [normal_reading])
```

Правильно:

```python
@pytest.mark.parametrize("reading_fixture", ["normal_reading"])
def test_example(request, reading_fixture):
    reading = request.getfixturevalue(reading_fixture)
```

---

### 2. Тесты используют строки вместо `Enum`

Плохо:

```python
assert result.diagnosis == "infarction"
```

Хорошо:

```python
assert result.diagnosis == Diagnosis.INFARCTION
```

---

### 3. Тесты сравнивают float напрямую

Плохо:

```python
assert average == 83.75
```

Хорошо:

```python
assert average == pytest.approx(83.75)
```

---

### 4. Исключение проверяется без сообщения

Менее предпочтительно:

```python
with pytest.raises(ValueError):
    analyze_heart_rate(-1)
```

Лучше:

```python
with pytest.raises(ValueError, match="отрицательным"):
    analyze_heart_rate(-1)
```

---

### 5. Дублирование создания объектов

Плохо:

```python
reading = ECGData(
    heart_rate=75,
    rhythm=Rhythm.REGULAR,
    st_segment=STSegment.NORMAL,
    q_wave=False,
)
```

в каждом тесте.

Хорошо:

```python
def test_normal(normal_reading):
    result = interpret_ecg(normal_reading)
    assert result.diagnosis == Diagnosis.NORMAL
```

---

## Медицинская оговорка

Проект является учебным.

Логика интерпретации ЭКГ намеренно упрощена. Она не заменяет:

- врача;
- медицинские алгоритмы;
- клинические рекомендации;
- сертификационные требования;
- валидацию медицинских изделий.

Не использовать проект для принятия решений о здоровье людей.

---

## Краткая инструкция агенту

Если агент получает задачу по этому репозиторию:

1. Прочитать `AGENTS.md`.
2. Посмотреть структуру проекта.
3. Запустить тесты.
4. Найти функцию, к которой относится задача.
5. Изучить существующие тесты.
6. Добавить или изменить тесты.
7. При необходимости изменить код.
8. Запустить:

   ```bash
   python -m pytest -v
   ```

9. Убедиться, что все тесты проходят.
10. Не менять поведение проекта без обновления тестов и документации.
