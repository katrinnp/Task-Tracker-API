# Task Tracker API

Task Tracker API is a REST API for managing tasks and users, built with **FastAPI**, **SQLAlchemy**, and **SQLite**. It supports full CRUD operations on tasks, filtering by completion status, basic pagination, and user-task relationships.

## Technologies

- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Uvicorn

## Project structure (backend `app` folder)

- `app/main.py` – Initializes the FastAPI application, creates database tables, and includes the routers.
- `app/models/` – SQLAlchemy models (`task.py`, `user.py`).
- `app/schemas/` – Pydantic schemas for request/response validation.
- `app/api/v1/` – HTTP endpoints (CRUD operations for tasks and users).
- `app/services/` – Business logic layer (e.g. `task_service.py`).
- `app/core/database.py` – Database configuration and the `get_db` dependency used by FastAPI.

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

| Method | Path        | Description           |
|--------|------------|----------------------|
| GET    | `/users/`  | List all users.      |
| POST   | `/users/`  | Create a new user.   |


## Tasks Endpoints

The following endpoints are available under the `/tasks` prefix:


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

1. Create and activate a virtual environment (optional but recommended).

2. Install dependencies:

pip install -r requirements.txt


3. Run the development server:

uvicorn app.main:app --reload


4. Open:

- Swagger UI: http://localhost:8000/docs  
- Root health check: http://localhost:8000/

## Future work

Planned improvements for this project:

- Add user authentication (JWT-based login/register).
- Restrict tasks so that each user can only access their own tasks.
- Implement login and password management.
- Improve pagination with total count and page metadata in the response.
- Add a simple frontend (React or plain HTML/JS) for managing tasks in the browser.
- Write more automated tests (unit and integration) for the API.
