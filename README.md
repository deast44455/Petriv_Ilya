# Система учёта оборудования — ООО "Команда Ф5"

Веб-приложение для учёта материальных активов на базе Django + PostgreSQL + Django REST Framework.

## Быстрый старт

```bash
cp .env.example .env
docker compose up --build
```

После запуска доступны:
- **Административная панель**: http://localhost:8000/admin/
- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **REST API**: http://localhost:8000/api/

## Создание суперпользователя

```bash
docker compose exec web python manage.py createsuperuser
```

## Запуск тестов

```bash
docker compose exec web python manage.py test
```

## Команды Makefile

| Команда         | Описание                          |
|-----------------|-----------------------------------|
| `make up`       | Запустить в фоне                  |
| `make down`     | Остановить контейнеры             |
| `make build`    | Собрать и запустить               |
| `make migrate`  | Применить миграции                |
| `make superuser`| Создать суперпользователя         |
| `make test`     | Запустить тесты                   |
| `make shell`    | Django shell                      |

## Структура API

| Endpoint                  | Описание              |
|---------------------------|-----------------------|
| `/api/categories/`        | Категории активов     |
| `/api/locations/`         | Локации               |
| `/api/departments/`       | Подразделения         |
| `/api/suppliers/`         | Поставщики            |
| `/api/assets/`            | Активы                |
| `/api/operations/`        | Операции с активами   |

## Роли пользователей

- **admin** — полный доступ
- **storekeeper** — кладовщик (управление операциями)
- **manager** — руководитель (просмотр и отчёты)
- **employee** — сотрудник (просмотр)
