# Task Tracker API

Task Tracker API is a REST API for managing tasks and users, built with **FastAPI**, **SQLAlchemy**, and **SQLite**. It supports full CRUD operations on tasks, filtering by completion status, basic pagination, user-task relationships, and JWT-based authentication.

## Technologies

- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Uvicorn
- JWT
- Passlib (bcrypt password hashing)
- Docker

## Project structure (backend `app` folder)

- `app/main.py` – Initializes the FastAPI application, creates database tables, and includes the routers.
- `app/models/` – SQLAlchemy models (`task.py`, `user.py`).
- `app/schemas/` – Pydantic schemas for request/response validation.
- `app/api/v1/` – HTTP endpoints (CRUD operations for tasks, users and authentication).
- `app/services/` – Business logic layer (e.g. `task_service.py`).
- `app/core/database.py` – Database configuration and the `get_db` dependency used by FastAPI.
- `app/core/dependencies.py` – Authentication dependencies (e.g. `get_current_user`).

---

## Database Models

### User

- `id` – Integer, primary key
- `username` – String, unique
- `hashed_password` – String

### Task

- `id` – Integer, primary key
- `title` – String
- `description` – String
- `completed` – Boolean
- `user_id` – Foreign key → `users.id`

Each task belongs to a specific user.

---

# Authentication

The API uses **JWT (JSON Web Token)** authentication.

Passwords are securely hashed using **Passlib (bcrypt)**.

---

## Authentication Endpoints

The following endpoints are available under `/api/v1/auth`:

| Method | Path | Description |
|--------|------|------------|
| POST | `/api/v1/auth/register` | Register a new user |
| POST | `/api/v1/auth/login` | Login and receive access token |

---

## Register

Creates a new user.

Example request body:

json
{
  "username": "testuser",
  "password": "password123"
}

## Login

Returns a JWT access token.

Example response:

json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer"
}

## Using the Access Token

1. Login to receive an access token.
2. Open Swagger UI at: http://localhost:8000/docs
3. Click the **Authorize** button.
4. Enter: Bearer <access_token>
5. Access protected endpoints.

---

## Database Models

### User

- `id` – Integer, primary key
- `username` – String, unique

### Task

- `id` – Integer, primary key
- `title` – String
- `description` – String
- `completed` – Boolean
- `user_id` – Foreign key → `users.id`

Each task belongs to a specific user.

---

## HTTP API

### Health Check

| Method | Path | Description |
|--------|------|------------|
| GET    | `/`  | Returns a simple status message. |

---

## Users Endpoints

| Method | Path                  | Description                          |
|--------|-----------------------|--------------------------------------|
| GET    | `/users/`             | List all users.                     |
| GET    | `/users/{user_id}`    | Get a single user by ID.            |
| POST   | `/users/`             | Create a new user.                  |
| PATCH  | `/users/{user_id}`    | Partially update an existing user.  |
| DELETE | `/users/{user_id}`    | Delete a user (returns HTTP 204).   |

## Tasks Endpoints

| Method | Path              | Description                                  |
|--------|------------------|----------------------------------------------|
| GET    | `/tasks/`        | List tasks with optional filters and paging. |
| POST   | `/tasks/`        | Create a new task.                           |
| GET    | `/tasks/{id}`    | Get a task by its ID.                        |
| PUT    | `/tasks/{id}`    | Replace an existing task.                    |
| PATCH  | `/tasks/{id}`    | Partially update an existing task.           |
| DELETE | `/tasks/{id}`    | Delete a task (returns HTTP 204 No Content). |


### Query parameters for `GET /tasks/`

- `completed` – `true` or `false` to filter tasks by completion status.
- `limit` – Maximum number of tasks returned (default: 10).
- `skip` – Number of tasks to skip (used for pagination).

## Running locally

1. Create and activate a virtual environment.

2. Install dependencies:

pip install -r requirements.txt

3. Run the development server:

uvicorn app.main:app --reload

4. Open:

- Swagger UI: http://localhost:8000/docs  
- Root health check: http://localhost:8000/

## Running with Docker

This project includes a Dockerfile that allows the API to run inside a container without installing Python or dependencies locally.

### Requirements

- Docker installed and running  

### Build the Docker image

From the project root directory:

docker build -t task-tracker-api .

### Run the container

docker run -p 8000:8000 task-tracker-api

After the container starts, open:

- Swagger UI: http://localhost:8000/docs  
- Root health check: http://localhost:8000/  

---

## Future work

Planned improvements for this project:

- Add a simple frontend (React or plain HTML/JS) for managing tasks in the browser.  
- Write more automated tests (unit and integration) for the API.  

