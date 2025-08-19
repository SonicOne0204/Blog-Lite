# BlogLite

BlogLite is a simple REST API blog built with Django and Django REST Framework.

## Description

The project provides an API for creating, reading, updating, and deleting posts and their sub-posts.
It includes features such as likes, view counting, and automatically generated API documentation via Swagger UI.

## Technologies

* Python 3.12+
* Django 5.2.5
* Django REST Framework 3.16
* drf-spectacular (OpenAPI/Swagger) 0.28
* PostgreSQL
* Docker & Docker Compose

## Features

* CRUD operations for posts and sub-posts
* Ability to like posts (one like per user per post)
* Tracking of unique post views
* Pagination
* Atomic operations for safe counting of likes and views
* Test coverage over 70%

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/yourusername/bloglite.git
cd bloglite
```

2. Create a `.env` file and add environment variables:

```env
SECRET_KEY=your_secret_key
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=db
DATABASE_PORT=5432
```

3. Run Docker Compose:

```bash
docker-compose up --build
```

4. Open in your browser:
   `http://localhost:8000/api/schema/swagger-ui/` — to view the API documentation.

## Tests

Run tests with:

```bash
pytest
```
?


