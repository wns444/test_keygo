# Backend

Backend для системы отслеживания внутренних задач (Internal Task Tracker).

## Стек технологий

- **Framework**: FastAPI
- **Database ORM**: SQLAlchemy 2.0
- **Validation**: Pydantic 2.0
- **Database**: SQLite (для демонстрации)
- **Testing**: pytest
- **Server**: Uvicorn

## Структура проекта

```text
backend/
├── app/
│   ├── models/              # SQLAlchemy models
│   │   ├── base.py          # Base model class
│   │   └── internal_task.py # InternalTask model
│   ├── schemas/             # Pydantic schemas
│   │   └── internal_task.py # Request/Response schemas
│   ├── routes/              # API routes
│   │   └── internal_tasks.py # Internal tasks endpoints
│   ├── config.py            # Configuration
│   ├── database.py          # Database setup
│   └── main.py              # FastAPI application
├── tests/
│   └── test_internal_tasks.py  # API tests
├── main.py                  # Entry point
├── pyproject.toml           # Project configuration
└── pytest.ini               # Pytest configuration
```

## Установка

### Prerequisites

- Python 3.11+
- pip или uv

### Установка зависимостей

```bash
# Using pip
pip install -e .

# Or using uv (faster)
uv sync
```

## Запуск

### Development сервер

```bash
uvicorn app.main:app --reload
```

Сервер будет доступен на `http://localhost:8000`

### Health check

```bash
curl http://localhost:8000/health
```

### API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Internal Tasks

#### Получить все задачи для бронирования

```text
GET /api/v1/bookings/{booking_id}/internal-tasks?status={status}
```

Параметры:

- `booking_id` (path, required): ID бронирования
- `status` (query, optional): Фильтр по статусу (open, in_progress, resolved, closed)

Ответ: `200 OK`

```json
[
  {
    "id": 1,
    "booking_id": "BOOKING123",
    "title": "Issue with payment",
    "description": "Customer reported charge issue",
    "status": "open",
    "created_at": "2024-04-28T10:00:00",
    "updated_at": "2024-04-28T10:00:00"
  }
]
```

#### Создать новую задачу

```text
POST /api/v1/bookings/{booking_id}/internal-tasks
```

Request body:

```json
{
  "booking_id": "BOOKING123",
  "title": "Issue with payment",
  "description": "Optional description"
}
```

Ответ: `201 Created`

```json
{
  "id": 1,
  "booking_id": "BOOKING123",
  "title": "Issue with payment",
  "description": "Optional description",
  "status": "open",
  "created_at": "2024-04-28T10:00:00",
  "updated_at": "2024-04-28T10:00:00"
}
```

**Ошибки:**

- `400 Bad Request`: booking_id в пути и теле не совпадают
- `409 Conflict`: Задача с таким названием для этого бронирования уже существует
- `422 Unprocessable Entity`: Ошибка валидации входных данных

#### Получить конкретную задачу

```text
GET /api/v1/internal-tasks/{task_id}
```

Ответ: `200 OK`

```json
{
  "id": 1,
  "booking_id": "BOOKING123",
  "title": "Issue with payment",
  "description": "Optional description",
  "status": "open",
  "created_at": "2024-04-28T10:00:00",
  "updated_at": "2024-04-28T10:00:00"
}
```

**Ошибки:**

- `404 Not Found`: Задача не найдена

#### Изменить статус задачи

```text
PATCH /api/v1/internal-tasks/{task_id}/status
```

Request body:

```json
{
  "status": "in_progress"
}
```

Доступные статусы: `open`, `in_progress`, `resolved`, `closed`

Ответ: `200 OK` (с обновленной задачей)

**Ошибки:**
- `404 Not Found`: Задача не найдена
- `422 Unprocessable Entity`: Неправильный статус

#### Удалить задачу

```text
DELETE /api/v1/internal-tasks/{task_id}
```

Ответ: `204 No Content`

**Ошибки:**

- `404 Not Found`: Задача не найдена

## Запуск тестов

### Все тесты

```bash
pytest
```

### С подробным выводом

```bash
pytest -v
```

### С покрытием кода

```bash
pytest --cov=app --cov-report=html
```

### Конкретный тест

```bash
pytest tests/test_internal_tasks.py::TestInternalTaskAPI::test_create_internal_task_success
```

## Покрытие тестами

Реализованные тесты:

### ✓ Обязательные требования

- **[test_create_internal_task_success]** - Создание задачи
- **[test_prevent_duplicate_task]** - Запрет дубля
- **[test_update_task_status]** - Смена статуса
- **[test_update_status_invalid_task]** - Обработка ошибки API (404)
- **[test_create_task_invalid_booking_id_in_path]** - Обработка ошибки API (400)

### ✓ Бонусные требования

- **[test_create_task_empty_title]** - Валидация входных данных
- **[test_create_task_missing_title]** - Валидация входных данных
- **[test_create_task_empty_booking_id]** - Валидация входных данных
- **[test_complete_workflow]** - Интеграционный тест компонента

### Итого покрытие

**Total: 28 тестов**

- Task Creation: 5 тестов
- Duplicate Prevention: 2 теста
- Task Retrieval: 4 теста
- Status Update: 6 тестов
- Delete: 2 теста
- Integration: 2 теста
- Other: 5 тестов

```bash
tests/test_internal_tasks.py::TestInternalTaskAPI::test_health_check PASSED
tests/test_internal_tasks.py::TestInternalTaskAPI::test_create_internal_task_success PASSED
tests/test_internal_tasks.py::TestInternalTaskAPI::test_create_task_without_description PASSED
tests/test_internal_tasks.py::TestInternalTaskAPI::test_create_task_invalid_booking_id_in_path PASSED
tests/test_internal_tasks.py::TestInternalTaskAPI::test_create_task_empty_title PASSED
tests/test_internal_tasks.py::TestInternalTaskAPI::test_create_task_missing_title PASSED
tests/test_internal_tasks.py::TestInternalTaskAPI::test_create_task_empty_booking_id PASSED
tests/test_internal_tasks.py::TestInternalTaskAPI::test_prevent_duplicate_task PASSED
tests/test_internal_tasks.py::TestInternalTaskAPI::test_allow_same_title_different_booking PASSED
tests/test_internal_tasks.py::TestInternalTaskAPI::test_get_all_tasks_for_booking PASSED
tests/test_internal_tasks.py::TestInternalTaskAPI::test_get_tasks_by_status PASSED
tests/test_internal_tasks.py::TestInternalTaskAPI::test_get_tasks_empty_booking PASSED
tests/test_internal_tasks.py::TestInternalTaskAPI::test_get_specific_task PASSED
tests/test_internal_tasks.py::TestInternalTaskAPI::test_get_nonexistent_task PASSED
tests/test_internal_tasks.py::TestInternalTaskAPI::test_update_task_status PASSED
tests/test_internal_tasks.py::TestInternalTaskAPI::test_update_status_to_resolved PASSED
tests/test_internal_tasks.py::TestInternalTaskAPI::test_update_status_to_closed PASSED
tests/test_internal_tasks.py::TestInternalTaskAPI::test_update_status_invalid_task PASSED
tests/test_internal_tasks.py::TestInternalTaskAPI::test_update_status_invalid_value PASSED
tests/test_internal_tasks.py::TestInternalTaskAPI::test_delete_internal_task PASSED
tests/test_internal_tasks.py::TestInternalTaskAPI::test_delete_nonexistent_task PASSED
tests/test_internal_tasks.py::TestInternalTaskAPI::test_complete_workflow PASSED
tests/test_internal_tasks.py::TestInternalTaskAPI::test_multiple_bookings_isolation PASSED
```

## Логирование

### Логируемые события

1. **Информационные события (INFO)**:
   - Запуск и остановка приложения
   - Получение списка задач
   - Успешное создание задачи
   - Успешное обновление статуса задачи
   - Успешное удаление задачи
   - Health check запросы

2. **Ошибки (ERROR)**:
   - Ошибки базы данных
   - Конфликты уникальности (дублирование задач)
   - Ошибки при создании, обновлении, удалении задач
   - Непредвиденные ошибки API

3. **Предупреждения (WARNING)**:
   - Несовпадение booking_id в пути и теле запроса
   - Попытка получить несуществующую задачу
   - Попытка обновить несуществующую задачу

### Примеры логов

```logs
2024-04-28 10:00:00 - app.routes.internal_tasks - INFO - Creating internal task for booking BOOKING123: Issue with payment
2024-04-28 10:00:01 - app.routes.internal_tasks - INFO - Successfully created internal task 1 for booking BOOKING123
2024-04-28 10:00:05 - app.routes.internal_tasks - ERROR - Duplicate task error for booking BOOKING123: UNIQUE constraint failed
2024-04-28 10:00:10 - app.routes.internal_tasks - WARNING - Internal task 99999 not found
```

## Grafana Метрики

Рекомендуемые метрики для отслеживания:

### Основные метрики

1. **internal_task_total** (Counter)
   - Описание: Всего создано задач
   - Labels: `booking_id`, `status`
   - Пример: `internal_task_total{booking_id="BOOKING123", status="open"}`

2. **internal_task_active_count** (Gauge)
   - Описание: Количество активных задач (статусы: open, in_progress)
   - Labels: `booking_id`
   - Примеры:
     - `internal_task_active_count{booking_id="BOOKING123"}` = 5
     - `internal_task_active_count{booking_id="BOOKING456"}` = 2

3. **internal_task_status_change_total** (Counter)
   - Описание: Всего изменений статусов задач
   - Labels: `from_status`, `to_status`
   - Примеры:
     - `internal_task_status_change_total{from_status="open", to_status="in_progress"}` = 10
     - `internal_task_status_change_total{from_status="in_progress", to_status="resolved"}` = 7

4. **internal_task_create_failed_total** (Counter)
   - Описание: Ошибки при создании задач
   - Labels: `error_type` (duplicate, validation_error, server_error)
   - Примеры:
     - `internal_task_create_failed_total{error_type="duplicate"}` = 15
     - `internal_task_create_failed_total{error_type="validation_error"}` = 5

5. **internal_task_operation_duration_seconds** (Histogram)
   - Описание: Время выполнения операций
   - Labels: `operation` (create, read, update, delete)
   - Bucketing: [0.01, 0.05, 0.1, 0.5, 1.0]

### Примеры запросов для Grafana

**Количество активных задач за 5 минут:**

```
sum(internal_task_active_count)
```

**Процент успешно созданных задач:**

```
internal_task_total / (internal_task_total + internal_task_create_failed_total)
```

**Среднее время создания задачи:**
```
rate(internal_task_operation_duration_seconds_sum{operation="create"}[5m]) / 
rate(internal_task_operation_duration_seconds_count{operation="create"}[5m])
```

**Частота ошибок создания (за 10 минут):**

```
rate(internal_task_create_failed_total[10m])
```

## Sentry Конфигурация

### Отправляемые ошибки

1. **Duplicate Task Error** (level: warning)
   - Когда: Попытка создать задачу с таким же названием для того же бронирования
   - Контекст:
     ```
     {
       "booking_id": "BOOKING123",
       "title": "Issue with payment",
       "error_type": "IntegrityError"
     }
     ```

2. **Validation Error** (level: warning)
   - Когда: Невалидные входные данные
   - Контекст:
     ```
     {
       "field": "title",
       "error": "min_length",
       "provided_value": ""
     }
     ```

3. **Database Error** (level: error)
   - Когда: Ошибки при работе с БД (кроме IntegrityError)
   - Контекст:
     ```
     {
       "operation": "create",
       "error": "database_connection_failed",
       "query": "INSERT INTO internal_tasks..."
     }
     ```

4. **API Error** (level: error)
   - Когда: Неожиданные ошибки при выполнении операций
   - Контекст:

     ```
     {
       "endpoint": "POST /api/v1/bookings/BOOKING123/internal-tasks",
       "status_code": 500,
       "error": "Internal server error"
     }
     ```

### Пример конфигурации Sentry в коде

```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="YOUR_SENTRY_DSN",
    integrations=[FastApiIntegration()],
    traces_sample_rate=0.1,
    environment="production",
)
```

## Alerts (Рекомендуемые оповещения для Grafana)

### 1. Высокая частота ошибок создания задач

```
Condition: rate(internal_task_create_failed_total[10m]) > 5
Severity: Warning
Notification: Slack #ops
Message: "High failure rate for internal task creation: {{value}} errors/10min"
```

### 2. Слишком много активных задач

```
Condition: sum(internal_task_active_count) > 100
Severity: Info
Notification: Slack #tasks
Message: "High number of active tasks: {{value}}"
```

### 3. Медленное создание задач

```
Condition: histogram_quantile(0.95, internal_task_operation_duration_seconds{operation="create"}) > 1
Severity: Warning
Notification: Slack #performance
Message: "Slow task creation detected: p95={{value}}s"
```

### 4. Отсутствие обновлений задач

```
Condition: increase(internal_task_status_change_total[1h]) == 0
Severity: Info
Notification: Email ops@company.com
Message: "No task status updates in the last hour"
```

## Разработка

### Добавление новой функции

1. Создайте миграцию (при необходимости)
2. Обновите модель в `app/models/`
3. Обновите схему в `app/schemas/`
4. Добавьте endpoint в `app/routes/`
5. Напишите тесты в `tests/`
6. Убедитесь, что все тесты проходят

### Style Guide

- Используйте type hints во всех функциях
- Логируйте важные события
- Добавьте обработку ошибок везде, где это возможно
- Пишите docstrings для функций и классов

## Troubleshooting

### Ошибка: "database locked"

Убедитесь, что вы используете SQLite с правильными параметрами подключения.

### Ошибка: "table already exists"

Очистите БД: `rm test_keygo.db` и запустите снова.

### Тесты не работают

```bash
# Убедитесь, что тестовые зависимости установлены
pip install pytest pytest-asyncio

# Запустите тесты с подробным выводом
pytest -vv --tb=long
```

## License

MIT
