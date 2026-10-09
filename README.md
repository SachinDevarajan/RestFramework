# Django REST Framework – Student & Course Management API

A learning-focused REST API built with **Django REST Framework (DRF)** and **PostgreSQL**. This project demonstrates model serialization, API validation, authentication with DRF tokens and JSON Web Tokens (JWT), paginated responses, and generic class-based views using a simple student and course management domain.

## Tech Stack

- Python & Django
- Django REST Framework
- PostgreSQL
- Django REST Framework Token Authentication
- Simple JWT (`djangorestframework-simplejwt`)
- Postman (for API testing)

## Features

- **Students:** student records with name, age, and place; list, create, retrieve, update, and delete using generic API views.
- **Courses:** list courses and create courses through JWT-protected endpoints.
- **Enrollments:** database model linking Django users to courses.
- **Serialization:** `ModelSerializer`, serializer inheritance (`CourseDetailSerializer`), and fee validation.
- **Authentication:** DRF token issuance, JWT token issuance, and custom JWT claims.
- **Pagination:** page-number pagination with five student records per page.
- **Permissions:** authentication required on selected endpoints.

> This is a practice project. Some endpoints illustrate concepts rather than a complete production-ready workflow. The enrollment model exists, but enrollment API routes are not yet provided.

## Project Structure

```text
RestFramework/
├── DRF/                     # Project configuration and root URLs
│   ├── settings.py
│   └── urls.py
├── application/             # Main Django app
│   ├── models.py            # Student, Course, Enrollment
│   ├── serializer.py        # DRF serializers and validation
│   ├── tokens.py            # Custom JWT claims
│   ├── views.py             # Function-based and generic API views
│   └── urls.py              # API routes
└── manage.py
```

## Database Models

| Model | Fields / Relationships |
| --- | --- |
| `Student` | `name`, `age`, `place` |
| `Course` | `name`, `duration`, `fees`, `description` |
| `Enrollment` | `student` → Django `User`, `course` → `Course` |

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/SachinDevarajan/RestFramework.git
cd RestFramework
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install django djangorestframework djangorestframework-simplejwt "psycopg[binary]"
```

> The repository currently does not include a dependency lockfile. These are the main packages needed by the code shown in the project.

### 4. Configure PostgreSQL

Create a PostgreSQL database named `drf` and configure the `DATABASES` setting in `DRF/settings.py` with **your own** local database name, username, and password. Do not commit real credentials to Git.

For production or shared environments, load database credentials and `SECRET_KEY` from environment variables instead of storing them directly in `settings.py`.

### 5. Run migrations

```bash
python manage.py migrate
```

If you change models and need to generate new migrations, run `python manage.py makemigrations` before `migrate`.

### 6. Create a user (optional)

```bash
python manage.py createsuperuser
```

### 7. Start the development server

```bash
python manage.py runserver
```

Base URL: `http://127.0.0.1:8000/`

## API Endpoints

The following paths are taken from `application/urls.py`.

| Method | Endpoint | Purpose | Authentication |
| --- | --- | --- | --- |
| GET | `/` | API home message | Public |
| GET | `/students/` | Current student function-based example* | Public |
| GET | `/view_students/` | List students, five per page | DRF token |
| POST | `/auth/` | Obtain DRF auth token | Username/password |
| GET | `/courses/` | List courses | JWT access token |
| POST | `/add_course/` | Create course | JWT access token |
| POST | `/token/` | Obtain standard JWT access and refresh tokens | Username/password |
| POST | `/refresh/` | Sliding-token refresh view** | Sliding JWT |
| POST | `/login/` | Custom login returning JWT access and refresh tokens | Username/password |
| GET, POST | `/student_generic/` | List / create students | Default DRF permissions |
| PUT, PATCH, DELETE | `/student_generic_ud/<id>/` | Update / delete student | Default DRF permissions |
| GET | `/student_retrieve/<id>/` | Retrieve one student | Default DRF permissions |

\* **Important:** In the current code, `/students/` is declared as a `GET` view but attempts to validate and save `request.data`. Use `/student_generic/` for creating students until that function is corrected.

\*\* **Important:** `/refresh/` currently uses `TokenRefreshSlidingView`, while `/token/` issues an ordinary access/refresh pair. These are different JWT flows. For refreshing the ordinary refresh token, replace the view with `TokenRefreshView`.

### Example: Create a student

**POST** `http://127.0.0.1:8000/student_generic/`

```json
{
  "name": "Arun",
  "age": 22,
  "place": "Bengaluru"
}
```

### Example: List students with pagination

**GET** `http://127.0.0.1:8000/view_students/?page=1`

Set this header using a token returned by `/auth/`:

```http
Authorization: Token YOUR_DRF_TOKEN
```

The paginated response includes `count`, `next`, `previous`, and `results`.

### Example: Obtain JWT tokens

**POST** `http://127.0.0.1:8000/login/`

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

On successful login, the endpoint returns `access` and `refresh` tokens. The custom refresh token adds these claims: `username`, `email`, `first_name`, and `last_name`.

For protected JWT routes, send:

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Example: Create a course

**POST** `http://127.0.0.1:8000/add_course/`

```json
{
  "name": "Python Full Stack",
  "duration": "3 months",
  "fees": 15000,
  "description": "Python, Django, REST APIs and PostgreSQL"
}
```

The `CourseSerializer` validates that fees are greater than zero. Its derived `CourseDetailSerializer` additionally includes `description` and `duration`.

## Concepts Practiced

- REST endpoints and HTTP methods (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`)
- Serialization and deserialization
- Serializer field validation and serializer inheritance
- Function-based API views with `@api_view`
- Generic API views: `CreateAPIView`, `ListAPIView`, `RetrieveAPIView`, `UpdateAPIView`, `DestroyAPIView`
- Authentication vs. permissions
- DRF built-in token authentication vs. JWT authentication
- JWT claims and `RefreshToken.for_user()`
- Page-number pagination
- Django ORM and PostgreSQL models

## Current Limitations / Improvements

This repository is a learning project. Before using it in production:

1. Move the Django secret key and PostgreSQL credentials out of version-controlled settings and rotate any exposed secrets.
2. Fix the `/students/` HTTP method / create logic.
3. Rename `valid_age` to `validate_age` so DRF recognizes it as field-level validation.
4. Replace `TokenRefreshSlidingView` with `TokenRefreshView` if using standard JWT refresh tokens.
5. Consolidate the two `REST_FRAMEWORK` assignments in `settings.py` so both authentication and pagination settings are retained.
6. Add explicit permissions to the generic views as required by your application.
7. Add tests, a `requirements.txt` file, environment configuration, and enrollment endpoints.

## Author

**Sachin Devarajan**

- [GitHub](https://github.com/SachinDevarajan)
- [Portfolio](https://sachindevarajan.netlify.app/)
- [LinkedIn](https://www.linkedin.com/in/sachindevarajan/)

---

*Built to practice Django REST Framework concepts through hands-on API development.*
