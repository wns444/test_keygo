# Frontend

Frontend приложение для системы отслеживания внутренних задач (Internal Task Tracker).

## Стек технологий

- **Framework**: Next.js 14
- **UI Library**: React 18
- **HTTP Client**: Axios
- **Styling**: CSS Modules
- **Testing**: Jest + React Testing Library
- **Language**: TypeScript / JavaScript

## Структура проекта

```
frontend/
├── app/
│   ├── layout.tsx           # Root layout
│   ├── globals.css          # Global styles
│   ├── bookings/
│   │   └── [booking_id]/
│   │       ├── page.jsx     # Booking page
│   │       └── page.module.css
├── components/
│   ├── InternalTasks.jsx    # Main component
│   └── InternalTasks.module.css
├── lib/
│   └── api.js               # API client
├── __tests__/
│   └── InternalTasks.test.tsx
├── package.json
├── tsconfig.json
├── jest.config.js
├── next.config.js
└── .gitignore
```

## Установка

### Prerequisites
- Node.js 18+
- npm или yarn или pnpm

### Установка зависимостей

```bash
npm install
# или
yarn install
# или
pnpm install
```

## Запуск

### Development сервер

```bash
npm run dev
# или
yarn dev
# или
pnpm dev
```

Сервер будет доступен на `http://localhost:3000`

### Переход на страницу бронирования

```
http://localhost:3000/bookings/BOOKING123
```

### Production build

```bash
npm run build
npm start
```

## API Configuration

По умолчанию приложение подключается к `http://localhost:8000`.

Для изменения URL API установите переменную окружения:

```bash
NEXT_PUBLIC_API_URL=http://your-api-url npm run dev
```

Или создайте `.env.local` файл:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Компоненты

### InternalTasks Component

Основной компонент для управления внутренними задачами.

**Props:**
- `bookingId` (string): ID бронирования

**Features:**
- Отображение списка задач
- Создание новой задачи
- Изменение статуса задачи
- Удаление задачи
- Фильтрация по статусу
- Обработка ошибок
- Успешные сообщения

**Пример использования:**

```jsx
import InternalTasks from '@/components/InternalTasks';

export default function Page() {
  return <InternalTasks bookingId="BOOKING123" />;
}
```

## API Integration

Все запросы к API обрабатываются через модуль `lib/api.js`:

```javascript
import { internalTasksAPI } from '@/lib/api';

// Get tasks
const tasks = await internalTasksAPI.getTasks(bookingId);

// Get tasks with filter
const openTasks = await internalTasksAPI.getTasks(bookingId, 'open');

// Get specific task
const task = await internalTasksAPI.getTask(taskId);

// Create task
const newTask = await internalTasksAPI.createTask(bookingId, {
  title: 'Task title',
  description: 'Optional description'
});

// Update task status
const updatedTask = await internalTasksAPI.updateTaskStatus(taskId, 'resolved');

// Delete task
await internalTasksAPI.deleteTask(taskId);
```

## Обработка ошибок

Компонент показывает соответствующие сообщения об ошибках:

- **API Errors**: Отображаются в красном баннере с деталями ошибки
- **Validation Errors**: Показываются под формой создания задачи
- **Duplicate Task**: Специальное сообщение при попытке создать дубль
- **Not Found**: Сообщение при удалении или обновлении несуществующей задачи

## Стили

Все стили организованы в CSS Modules:

- `InternalTasks.module.css` - Стили компонента внутренних задач
- `globals.css` - Глобальные стили
- `page.module.css` - Стили страницы бронирования

### Палитра цветов

- **Primary**: `#2196f3` (синий)
- **Success**: `#4caf50` (зеленый)
- **Warning**: `#ff9800` (оранжевый)
- **Error**: `#f44336` (красный)
- **Neutral**: `#999` / `#ddd` (серый)

## Тестирование

### Unit тесты компонента

Тесты расположены в `__tests__/InternalTasks.test.tsx` и покрывают:

- ✓ Рендеринг компонента
- ✓ Создание задачи
- ✓ Валидация формы
- ✓ Обновление статуса
- ✓ Удаление задачи
- ✓ Обработка ошибок API
- ✓ Фильтрация по статусу

**Запуск тестов:**

```bash
npm test
npm test -- --coverage
```

## Responsive Design

Компонент адаптивен и работает на:
- Desktop (1200px+)
- Tablet (768px - 1200px)
- Mobile (<768px)

На мобильных устройствах:
- Стоки становятся вертикальными
- Размеры шрифтов уменьшаются
- Кнопки становятся блочными

## Performance Optimizations

- Ленивая загрузка данных с использованием `useEffect`
- Оптимизация повторных рендеров
- Кэширование API клиента
- CSS Modules для изоляции стилей

## Accessibility

- Семантический HTML
- ARIA labels
- Достаточный контраст
- Keyboard navigation support
- Фокусные стили для интерактивных элементов

## Troubleshooting

### Ошибка: "Cannot GET /bookings/..."
Убедитесь, что используете правильный формат URL: `/bookings/BOOKING_ID`

### API не ответил
Проверьте:
1. Backend запущен на порту 8000
2. Переменная `NEXT_PUBLIC_API_URL` правильная
3. CORS включен на backend

### Стили не применяются
Убедитесь, что CSS Modules импортируются с расширением `.module.css`

## Разработка

### Добавление нового компонента

1. Создайте файл компонента в `components/`
2. Создайте файл стилей `ComponentName.module.css`
3. Экспортируйте компонент
4. Напишите тесты в `__tests__/`

### Code Style

- Используйте функциональные компоненты
- Используйте hooks (useState, useEffect)
- Добавляйте type hints (JSDoc или TypeScript)
- Избегайте inline styles
- Используйте CSS Modules для стилей

## License

MIT
