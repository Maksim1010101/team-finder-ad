```markdown
# TeamFinder — платформа для поиска команды над pet-проектами

**Вариант 1** – избранное + фильтрация пользователей.

## 🚀 Быстрый старт

### 1. Клонирование репозитория
```bash
git clone <url-репозитория>
cd team-finder-ad
```

### 2. Настройка окружения

Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

Установите зависимости:
```bash
pip install -r requirements.txt
```

### 3. Переменные окружения

Скопируйте `.env_example` в `.env` и заполните:
```bash
cp .env_example .env
```

Обязательные переменные:

| Переменная          | Значение                                       |
|---------------------|------------------------------------------------|
| DJANGO_SECRET_KEY   | Сгенерируйте командой `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| DJANGO_DEBUG        | `True` (для разработки)                        |
| POSTGRES_DB         | `teamfinder`                                   |
| POSTGRES_USER       | `postgres` (или свой пользователь)             |
| POSTGRES_PASSWORD   | пароль                                         |
| POSTGRES_HOST       | `localhost`                                    |
| POSTGRES_PORT       | `5432` (или `5436`, если Docker использует другой порт) |
| TASK_VERSION        | `1`                                            |

### 4. Запуск базы данных PostgreSQL

**С помощью Docker** (рекомендуется):
```bash
docker-compose up -d
```

**Локально** – убедитесь, что PostgreSQL запущен и соответствует переменным в `.env`.

### 5. Применение миграций

```bash
python manage.py migrate
```

### 6. Создание суперпользователя

```bash
python manage.py createsuperuser
```

### 7. Запуск сервера разработки

```bash
python manage.py runserver
```

Приложение станет доступно по адресу: [http://localhost:8000](http://localhost:8000)



---




Проект выполнен в рамках учебного задания.
```