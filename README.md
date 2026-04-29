# KeyGo Internal Task Tracker

Веб-приложение для управления внутренними задачами по бронированиям.

**Ожидаемое время выполнения**: 3–4 часа  
**Статус**: ✅ Полностью реализовано

## 📋 Обзор

Система позволяет:

- Сотрудникам создавать внутренние задачи по проблемам с бронированиями
- Отслеживать статус задач (Open → In Progress → Resolved → Closed)
- Предотвращать дублирование задач
- Логировать все события
- Мониторить метрики в Grafana
- Отправлять ошибки в Sentry

## 🏗️ Архитектура

```text
test_keygo/
├── backend/                    # FastAPI приложение
│   ├── app/
│   │   ├── models/            # SQLAlchemy модели
│   │   ├── schemas/           # Pydantic валидация
│   │   ├── routes/            # API endpoints
│   │   ├── config.py          # Конфигурация
│   │   ├── database.py        # Database setup
│   │   └── main.py            # FastAPI app
│   ├── tests/                 # Pytest тесты (28 тестов)
│   ├── pytest.ini
│   ├── pyproject.toml
│   └── README.md
├── frontend/                   # Next.js приложение
│   ├── app/
│   │   ├── bookings/          # Страница /bookings/[booking_id]
│   │   ├── layout.tsx         # Root layout
│   │   └── globals.css        # Global styles
│   ├── components/            # React компоненты
│   │   └── InternalTasks.jsx  # Основной компонент
│   ├── lib/                   # API client
│   ├── __tests__/             # Jest тесты
│   ├── package.json
│   ├── tsconfig.json
│   ├── jest.config.js
│   └── README.md
├── docs/
│   └── techspec.md            # Техническое задание
└── README.md                  # Этот файл
```

## 🚀 Быстрый старт

### Prerequisites

- Python 3.11+
- Node.js 18+
- Git

### 1. Backend установка

```bash
cd backend

# Установить зависимости
pip install -e . 
# или
uv sync

# (Опционально) Создать .env файл
cp .env.example .env

# Запустить backend
uvicorn app.main:app --reload
```

Backend будет доступен на `http://localhost:8000`

**API Documentation**: `http://localhost:8000/docs`

### 2. Frontend установка (в отдельном терминале)

```bash
cd frontend

# Установить зависимости
npm install
# или
yarn install
# или
pnpm install

# (Опционально) Создать .env.local файл
cp .env.example .env.local

# Запустить dev сервер
npm run dev
# или
yarn dev
```

Frontend будет доступен на `http://localhost:3000`

### 3. Откройте в браузере

```text
http://localhost:3000/bookings/*BOOKING123*
```

Замените `BOOKING123` на любой ID бронирования для тестирования.

## 🧪 Запуск тестов

### Backend тесты (28 тестов)

```bash
cd backend

# Все тесты
pytest

# С подробным выводом
pytest -v

# С покрытием кода
pytest --cov=app --cov-report=html

# Конкретный тест
pytest tests/test_internal_tasks.py::TestInternalTaskAPI::test_create_internal_task_success
```

**Покрытие:**

- ✅ Создание задачи
- ✅ Запрет дубля (UniqueConstraint)
- ✅ Смена статуса
- ✅ Обработка ошибок API (400, 404, 409, 422, 500)
- ✅ Валидация входных данных (Pydantic)
- ✅ Интеграционные тесты
- ✅ Изоляция по бронированиям

## ✨ Реализованные функции

### Backend API

#### Endpoints

| Метод | Endpoint | Описание |
|-------|----------|---------|
| GET | `/api/v1/bookings/{booking_id}/internal-tasks` | Получить все задачи для бронирования |
| POST | `/api/v1/bookings/{booking_id}/internal-tasks` | Создать новую задачу |
| GET | `/api/v1/internal-tasks/{task_id}` | Получить конкретную задачу |
| PATCH | `/api/v1/internal-tasks/{task_id}/status` | Изменить статус задачи |
| DELETE | `/api/v1/internal-tasks/{task_id}` | Удалить задачу |
| GET | `/health` | Health check |

#### Модель данных

```python
class InternalTask:
    id: int                          # Primary key
    booking_id: str (50)             # Foreign key with index
    title: str (255)                 # Unique constraint with booking_id
    description: str (1000)          # Optional
    status: Enum(open|in_progress|resolved|closed)
    created_at: datetime             # Auto timestamp
    updated_at: datetime             # Auto timestamp on update
```

**Constraints:**

- `UNIQUE(booking_id, title)` - Запрет дублей
- `INDEX(booking_id, status)` - Оптимизация поиска

#### Validation

- ✅ `booking_id`: 1-50 символов
- ✅ `title`: 1-255 символов (required)
- ✅ `description`: 0-1000 символов (optional)
- ✅ `status`: Enum (open, in_progress, resolved, closed)
- ✅ Consistency check: booking_id в пути === booking_id в теле

### Frontend

#### Страница `/bookings/[booking_id]`

**Блок Internal Tasks:**

- 📝 Список задач с фильтрацией по статусу
- ➕ Форма создания новой задачи
- 🔄 Смена статуса (dropdown)
- 🗑️ Удаление задачи
- ⚠️ Обработка ошибок с красивыми сообщениями
- ✅ Success сообщения при выполнении операций

**Features:**

- Responsive design (Desktop, Tablet, Mobile)
- Real-time updates
- Loading states
- Error handling
- Input validation
- Accessibility (ARIA labels, keyboard navigation)

## 📊 Логирование, Мониторинг и Alerting

### 1️⃣ Логирование (Python logging)

**Реализовано в backend:**

```python
# app/routes/internal_tasks.py
logger = logging.getLogger(__name__)

# Информационные события
logger.info(f"Creating internal task for booking {booking_id}: {task_data.title}")
logger.info(f"Successfully created internal task {db_task.id}")

# Ошибки
logger.error(f"Duplicate task error: {str(e)}")
logger.error(f"Error creating internal task: {str(e)}")

# Предупреждения
logger.warning(f"Booking ID mismatch: {task_data.booking_id} vs {booking_id}")
logger.warning(f"Internal task {task_id} not found")
```

**Примеры логов:**

```text
2024-04-28 10:00:00 - app.routes.internal_tasks - INFO - Creating internal task for booking BOOKING123: Payment issue
2024-04-28 10:00:01 - app.routes.internal_tasks - INFO - Successfully created internal task 1 for booking BOOKING123
2024-04-28 10:00:05 - app.routes.internal_tasks - ERROR - Duplicate task error for booking BOOKING123: UNIQUE constraint failed
2024-04-28 10:00:10 - app.database - ERROR - Database error: connection timeout
```

**Логируемые события:**

- ✅ Запуск и остановка приложения
- ✅ Получение списка задач
- ✅ Успешное создание/обновление/удаление задачи
- ✅ Ошибки БД (IntegrityError, OperationalError, etc)
- ✅ Ошибки валидации
- ✅ API ошибки (400, 404, 409, 422, 500)
- ✅ Health check запросы

### 2️⃣ Grafana Метрики

**Рекомендуемые метрики для отслеживания:**

#### Counter Метрики

```promql
# Всего создано задач
internal_task_total{booking_id="BOOKING123", status="open"}

# Изменения статусов
internal_task_status_change_total{from_status="open", to_status="in_progress"}

# Ошибки создания
internal_task_create_failed_total{error_type="duplicate|validation_error|server_error"}
```

#### Gauge Метрики

```promql
# Количество активных задач
internal_task_active_count{booking_id="BOOKING123"} = 5
```

#### Histogram Метрики

```promql
# Время выполнения операций
internal_task_operation_duration_seconds{operation="create|read|update|delete"}
```

**Примеры dashboards:**

1. **Overview Dashboard**
   - Total tasks created (all time)
   - Active tasks count (gauge)
   - Tasks by status (pie chart)
   - Tasks created per day (line chart)

2. **Performance Dashboard**
   - API response time (histogram)
   - Requests per second (rate)
   - Error rate percentage

3. **Operational Dashboard**
   - Tasks by booking_id (top 10)
   - Status distribution
   - Error types breakdown

### 3️⃣ Sentry Error Tracking

**Отправляемые ошибки:**

#### Severity: WARNING

**Duplicate Task Error**

```json
{
  "error_type": "IntegrityError",
  "message": "Duplicate task for booking",
  "context": {
    "booking_id": "BOOKING123",
    "title": "Payment issue",
    "operation": "create"
  }
}
```

**Validation Error**

```json
{
  "error_type": "ValidationError",
  "message": "Invalid input data",
  "context": {
    "field": "title",
    "error": "min_length",
    "provided_value": ""
  }
}
```

#### Severity: ERROR

**Database Error**

```json
{
  "error_type": "DatabaseError",
  "message": "Database connection failed",
  "context": {
    "operation": "create",
    "error": "connection_timeout",
    "query": "INSERT INTO internal_tasks..."
  }
}
```

**API Error (500)**

```json
{
  "error_type": "InternalServerError",
  "message": "Internal server error",
  "context": {
    "endpoint": "POST /api/v1/bookings/BOOKING123/internal-tasks",
    "status_code": 500,
    "error": "Unexpected exception"
  }
}
```

### 4️⃣ Alerts (Recommended)

**Setup в Grafana:**

```text
1. Create alert rule
   Name: internal_task_create_failed_rate
   Condition: rate(internal_task_create_failed_total[10m]) > 5
   Severity: warning
   Notification: Slack #ops-alerts
   Message: "High failure rate for internal task creation: {{value}} errors/10min"

2. Create alert rule
   Name: internal_task_p95_latency
   Condition: histogram_quantile(0.95, internal_task_operation_duration_seconds{operation="create"}) > 1
   Severity: warning
   Notification: Slack #performance
   Message: "Slow task creation detected: p95={{value}}s"

3. Create alert rule
   Name: internal_task_high_active_count
   Condition: sum(internal_task_active_count) > 100
   Severity: info
   Notification: Slack #tasks
   Message: "High number of active tasks: {{value}}"

4. Create alert rule
   Name: internal_task_db_errors
   Condition: increase(internal_task_db_error_total[5m]) > 10
   Severity: critical
   Notification: PagerDuty, Slack #critical
   Message: "Database errors detected: {{value}} in 5 minutes"
```

## 🔌 Конфигурация Sentry (Пример кода)

### Backend

```python
# app/main.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN", ""),
    integrations=[
        FastApiIntegration(),
        SqlalchemyIntegration(),
    ],
    traces_sample_rate=0.1,
    profiles_sample_rate=0.1,
    environment=os.getenv("ENVIRONMENT", "development"),
    release=os.getenv("VERSION", "0.1.0"),
)

app = FastAPI()
# ... rest of app configuration
```

### Frontend

```javascript
// lib/sentry.js
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 0.1,
});
```

## 🔧 Configuration

### Backend (.env)

```env
DATABASE_URL=sqlite:///./test_keygo.db
DEBUG=True
LOG_LEVEL=INFO
SENTRY_DSN=https://your-sentry-dsn@sentry.io/123456
ENVIRONMENT=development
VERSION=0.1.0
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SENTRY_DSN=https://your-sentry-dsn@sentry.io/123456
```

## 📦 Production Deployment

### Backend (Docker)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY backend/pyproject.toml .
RUN pip install -e .

COPY backend/app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t keygo-backend .
docker run -p 8000:8000 keygo-backend
```

### Frontend (Vercel/Docker)

```bash
# Build
npm run build

# Run
npm start
```

## 🎯 Quality Checklist

- ✅ **Backend**: FastAPI + SQLAlchemy + Pydantic + Alembic
- ✅ **Frontend**: React + Next.js
- ✅ **Database**: SQLite (demo) / MongoDB compatible
- ✅ **Tests**: 28 backend + 7+ frontend tests
- ✅ **Validation**: Pydantic schemas + Frontend validation
- ✅ **Error Handling**: Try-catch blocks, proper HTTP status codes
- ✅ **Logging**: Python logging module
- ✅ **Documentation**: Comprehensive READMEs
- ✅ **Code Quality**: Type hints, docstrings, clean code
- ✅ **Git**: Proper repository structure

## 📚 Additional Resources

- [Backend README](./backend/README.md) - Детальная документация backend
- [Frontend README](./frontend/README.md) - Детальная документация frontend
- [Tech Spec](./docs/techspec.md) - Исходное техническое задание

## 🐛 Troubleshooting

### Backend issues

```bash
# Очистить БД
rm backend/test_keygo.db

# Переустановить зависимости
pip uninstall -y backend && pip install -e backend/

# Запустить с debug логами
DEBUG=True python backend/main.py
```

### Frontend issues

```bash
# Очистить cache
rm -rf frontend/.next frontend/node_modules package-lock.json
npm install

# Проверить API connection
curl -s http://localhost:8000/health
```
