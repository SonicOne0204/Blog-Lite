# BlogLite

BlogLite — это простой REST API блог, написанный на Django и Django REST Framework.

## Описание

Проект предоставляет API для создания, чтения, обновления и удаления постов и их под-постов (subposts).
Реализованы функции лайков и подсчёта просмотров.
Документация API доступна через Swagger UI.

## Технологии

* Python 3.12+
* Django 5.2.5
* Django REST Framework 3.16
* drf-spectacular (OpenAPI/Swagger) 0.28
* PostgreSQL
* Docker и Docker Compose

## Функционал

* CRUD операции с постами и под-постами
* Возможность ставить лайки (один лайк от пользователя на пост)
* Учёт уникальных просмотров постов
* Пагинация
* Атомарные операции для безопасного подсчёта лайков и просмотров
* Тесты с покрытием более 70%

## Запуск проекта

1. Скопируйте репозиторий:

```bash
git clone https://github.com/yourusername/bloglite.git
cd bloglite
```

2. Создайте файл `.env` и добавьте переменные окружения:

```env
SECRET_KEY=your_secret_key
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=db
DATABASE_PORT=5432
```

3. Запустите Docker Compose:

```bash
docker-compose up --build
```

4. Перейдите в браузере по адресу:
   `http://localhost:8000/api/schema/swagger-ui/` — для просмотра документации API.

## Тесты

Запуск тестов:

```bash
pytest
```

