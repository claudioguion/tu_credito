# Tu Crédito API

Tu Crédito API is a Django-based REST API for managing Banks, Clients, and Credits. The project is built using Python 3.11+, Django 5.x, Django REST Framework, and PostgreSQL, and is fully Dockerized for local development. It includes JWT authentication, filtering, searching, pagination, automatic API documentation, and basic security hardening suitable for an assessment submission.

The project follows a modular architecture with one Django app per domain entity, making it easy to extend and maintain.

---

## Features

- CRUD operations for Banks, Clients, and Credits
- RESTful API built with Django REST Framework
- JWT authentication using djangorestframework-simplejwt
- Filtering, searching, and pagination on all list endpoints
- Model-level data validation (credit minimum ≤ maximum, client age vs birth date)
- Centralized API security headers (CSP, Permissions Policy, XSS protection)
- Automatic API documentation with drf-spectacular (Swagger / Redoc)
- Dockerized development environment
- Automated tests using pytest and pytest-django

---

## Tech Stack

- Python 3.11+
- Django 5.x
- Django REST Framework
- PostgreSQL 13+
- Docker & Docker Compose
- djangorestframework-simplejwt
- django-filter
- drf-spectacular
- pytest + pytest-django

---

## Project Structure

tu_credito/
├── apps/
│   ├── banks/
│   ├── clients/
│   ├── credits/
│   ├── users/
│   └── utils/
├── tu_credito/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── requirements.txt
├── .env
└── README.md

---

## Environment Variables

DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_NAME=tu_credito
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=db
DATABASE_PORT=5432

---

## Docker Setup

docker-compose build
docker-compose up -d

Stop containers:

docker-compose down

---

## Database Setup

docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --noinput

---

## API Endpoints

Banks: /api/bancos
Clients: /api/clientes
Credits: /api/creditos
Register: /api/auth/register
Login: /api/auth/login
Logout: /api/auth/logout

---

## Authentication

JWT authentication is required for write operations.
Use Authorization: Bearer <token>

---

## API Documentation

http://localhost:8000/api/docs/
http://localhost:8000/api/schema/

---

## Testing

docker-compose exec web pytest

---

## Security

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = DENY

---

## License

MIT License
