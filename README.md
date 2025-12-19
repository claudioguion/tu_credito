# Tu Crédito API

Tu Crédito API es una REST API basada en Django para la gestión de Bancos, Clientes y Creditos. El proyecto está construido utilizando Python 3.11+, Django 5.x, Django REST Framework y PostgreSQL, y se encuentra completamente containerizado con Docker para el desarrollo local. Incluye JWT authentication, filtering, searching, pagination,
documentacion automatica, y un conjunto básico de mecanismos de seguridad, adecuado para un assessment técnico.

El proyecto sigue una arquitectura modular, con una aplicación de Django por cada entidad de dominio, lo que facilita su extensión, mantenimiento y escalabilidad.

---

## Features

- Operaciones CRUD para Bancos, Clientes y Creditos
- RESTful API construida con Django REST Framework
- JWT authentication utilizando djangorestframework-simplejwt
- Filtering, searching y pagination en todos los endpoints de listado
- Validaciones de datos a nivel de Modelo y Serializers
- Security headers centralizados (CSP, Permissions Policy, XSS protection)
- Documentacion automatica de la API con drf-spectacular (Swagger / Redoc)
- Entorno de desarrollo con Docker-compose (Web y Base de datos)
- Tests Automatizados utilizando pytest y pytest-django

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

## Estructura del proyecto

```text
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
```

---

## Variables de Entorno

Asegurarse de tener un archivo .env con las siguientes variables:

DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_NAME=tu_credito
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=db
DATABASE_PORT=5432

---

## Docker Setup para iniciar el proyecto

docker-compose build
docker-compose up -d

Borrar containers:

docker-compose down

---

## Django setup

docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --noinput

---

## API Endpoints

Bancos: /api/bancos
Clientes: /api/clientes
Creditos: /api/creditos
Registro de Usuario: /api/auth/register
Login: /api/auth/login
Logout: /api/auth/logout  # No funciona correctamente

---

## Authentication

Autenticacion via JWT token es requerida para operaciones de creacion, edicion, y borrado.
Las operaciones Read-Only no requieren token.

Usar Authorization: Bearer <token>

---

## Documentacion de la API

Ubicada en estas URLs

http://localhost:8000/api/docs/
http://localhost:8000/api/schema/

---

## API Collection

Se incluye una coleccion Postman para ahorrar tiempo al evaluador.
Copia el siguiente código JavaScript en la pestaña 'settings' del request de Login, para que los tokens se almacenen automáticamente:

const json = pm.response.json();

pm.collectionVariables.set("access_token", json.access);
pm.collectionVariables.set("refresh_token", json.refresh);

---

## Testing

docker-compose exec web pytest

---

## Seguridad

Se desarrollo un middleware a medida para gestionar Content Security Policy (CSP) y Permissions Policy. Este middleware se ubica en el directorio 'apps\utils\middleware.py'.

Tambien se incluyen las siguientes configuraciones en los settings de Django:

- SECURE_BROWSER_XSS_FILTER = True
- SECURE_CONTENT_TYPE_NOSNIFF = True
- X_FRAME_OPTIONS = DENY

---

## Fallas y comportamientos extraños

Se intento implementar un mecanismo de logout utilizando 'rest_framework_simplejwt.token_blacklist' para deshabilitar el access_token desde el backend, sin embargo, el endpoint no esta funcional por el momento.

Tambien, la API es extremadamente sensible con los trailing slash ('/') en los endpoints (Ej: /api/bancos/). Especialmente, las operaciones de escritura necesariamente siempre deben llevar slash al final de la URL.

---

## Uso de IA

Se utilizo ChatGPT en los siguientes escenarios:

- Agilizar la puesta a punto de los containers con Docker
- Compañero de Code Review, especialmente durante el debug
- Implementar Content Security Policy (CSP) y Permissions Policy
- Acelerar el desarrollo de los Tests

---

## Licencia

MIT License
