A backend API for a healthcare application built with Django, Django REST Framework (DRF), PostgreSQL, and JWT authentication. Users can register, log in, and securely manage patients, doctors, and patient-doctor assignments.

Features
JWT authentication with access/refresh tokens

Patient CRUD scoped to creator (ownership)

Doctor CRUD (read open; write requires auth)

Patient–Doctor mapping (assign/remove doctors to/from patients)

PostgreSQL via Django ORM

Robust validation and error handling

Environment-based configuration (.env)

Production-ready settings structure

Tech Stack
Python 3.11+

Django 5.x

Django REST Framework

djangorestframework-simplejwt

PostgreSQL 14+

django-environ

Project Structure
healthcare/ — Django project settings and URLs

core/ — app with models, serializers, views, permissions, admin

manage.py — Django entry point

.env — environment variables (not committed)

Quick Start
Clone and enter the project

git clone <repo-url>

cd healthcare

Create virtual environment

python -m venv venv

source venv/bin/activate # Windows: venv\Scripts\activate

Install dependencies

pip install -r requirements.txt
If requirements.txt is not present, install:

pip install django djangorestframework djangorestframework-simplejwt psycopg2-binary django-environ

Configure environment
Create a .env file in the same folder as manage.py:

DEBUG=True

SECRET_KEY=your-super-secret-key

DB_NAME=healthcare_db

DB_USER=postgres

DB_PASSWORD=yourpassword

DB_HOST=localhost

DB_PORT=5432

Create PostgreSQL database

psql -U postgres -h localhost -p 5432

CREATE DATABASE healthcare_db;

(Optional) GRANT ALL PRIVILEGES ON DATABASE healthcare_db TO postgres;

Run migrations and start server

python manage.py makemigrations

python manage.py migrate

python manage.py runserver

API base URL: http://127.0.0.1:8000/api/

Environment Variables
DEBUG: True/False

SECRET_KEY: Django secret key

DB_NAME: Postgres database name

DB_USER: Postgres user

DB_PASSWORD: Postgres password

DB_HOST: Database host

DB_PORT: Database port

Ensure .env is in .gitignore.

Authentication
JWT (Bearer) tokens using access/refresh pair.

Token endpoints:

POST /api/auth/login/ — obtain tokens

POST /api/auth/refresh/ — refresh access token

Note: If using the default SimpleJWT view, login expects username and password. This project aliases /api/auth/login/ to the token obtain view; adjust to accept email if desired.

API Endpoints
Authentication

POST /api/auth/register/ — Register with username/email/password

POST /api/auth/login/ — Obtain access/refresh tokens

POST /api/auth/refresh/ — Refresh access token

Patients (Authenticated)

POST /api/patients/ — Create patient (owned by requester)

GET /api/patients/ — List own patients

GET /api/patients/<id>/ — Retrieve own patient

PUT /api/patients/<id>/ — Update own patient

DELETE /api/patients/<id>/ — Delete own patient

Doctors

POST /api/doctors/ — Create doctor (auth required)

GET /api/doctors/ — List all doctors

GET /api/doctors/<id>/ — Retrieve doctor

PUT /api/doctors/<id>/ — Update doctor (auth required)

DELETE /api/doctors/<id>/ — Delete doctor (auth required)

Patient–Doctor Mappings (Authenticated)

POST /api/mappings/ — Assign doctor to patient (only for own patients)

GET /api/mappings/ — List mappings for own patients

GET /api/mappings/<patient_id>/ — List doctors assigned to a patient (own patient)

DELETE /api/mappings/<id>/ — Remove assignment

Example Requests (curl)
Register:

curl -X POST http://127.0.0.1:8000/api/auth/register/ -H "Content-Type: application/json" -d '{"username":"ab","email":"a@b.com","password":"StrongPass123!"}'

Login (token):

curl -X POST http://127.0.0.1:8000/api/auth/login/ -H "Content-Type: application/json" -d '{"username":"ab","password":"StrongPass123!"}'

Authenticated header:

Authorization: Bearer <ACCESS_TOKEN>

Create patient:

curl -X POST http://127.0.0.1:8000/api/patients/ -H "Authorization: Bearer <ACCESS_TOKEN>" -H "Content-Type: application/json" -d '{"first_name":"Jon","last_name":"Doe","email":"jon@example.com","dob":"1990-01-01","notes":"N/A"}'

List own patients:

curl -H "Authorization: Bearer <ACCESS_TOKEN>" http://127.0.0.1:8000/api/patients/

Create doctor:

curl -X POST http://127.0.0.1:8000/api/doctors/ -H "Authorization: Bearer <ACCESS_TOKEN>" -H "Content-Type: application/json" -d '{"first_name":"Alice","last_name":"Smith","email":"alice@clinic.com","specialization":"Cardiology"}'

Assign doctor to patient:

curl -X POST http://127.0.0.1:8000/api/mappings/ -H "Authorization: Bearer <ACCESS_TOKEN>" -H "Content-Type: application/json" -d '{"patient":1,"doctor":2}'

Delete mapping:

curl -X DELETE http://127.0.0.1:8000/api/mappings/3/ -H "Authorization: Bearer <ACCESS_TOKEN>"

Key Implementation Notes
Ownership: Patients are filtered by creator; only the owner can view/update/delete.

Doctors: Read is open; write operations require authentication.

Mappings: Only allow assigning/removing doctors for patients owned by the requester.

Validation: Unique emails for Patient and Doctor; mapping uniqueness enforced per patient–doctor pair.

Performance: Use select_related on mappings to reduce queries.

Security: Keep SECRET_KEY and DB credentials in .env; use strong passwords; consider rotating keys.

Running Tests
Create tests in core/tests/ (suggested)

Run: python manage.py test

Linting and Formatting (optional)
pip install black isort flake8

black .

isort .

flake8

Deployment Notes
Set DEBUG=False, configure ALLOWED_HOSTS

Provide DATABASE_URL or individual DB_* vars on the host

Run migrations on deploy

Serve with a WSGI server (gunicorn/uvicorn with ASGI if using Channels)

Add CORS, HTTPS, secure cookies, and proper logging for production

Extending
Add pagination, filtering, and search

Add audit trails for sensitive actions

Introduce rate limiting/throttling

Add OpenAPI/Swagger via drf-spectacular or drf-yasg

License
MIT (or update as needed)