# Student Attendance Tracker

A full-stack attendance application built with React and FastAPI. It supports account registration, login, token refresh, and viewing or adding attendance records.

## 1. Project and Team

- **Project:** Student Attendance Tracker
- **Poojitha:** A1 - Registration, A2 - Login
- **Adib:** A3 - Refresh token
- **Thanmayee:** E1 - Get attendance, E2 - Add attendance

## 2. Live App

- **EC2 public link:** `----------------------------------`

## 3. How to Run It

Requirements: Git, Python 3.12+, Node.js 20+, npm, and Docker.

### Backend

From the repository root on a fresh laptop:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

API: `http://127.0.0.1:8001`  
Swagger docs: `http://127.0.0.1:8001/docs`

### Frontend

Open a second terminal at the repository root:

```bash
cd frontend
npm install
npm run dev
```

Open the URL printed by Vite, normally `http://localhost:5173`.

### Docker

The backend Docker image can be built and run from the `backend` directory:

```bash
cd backend
docker build -t student-attendance-backend .
docker run --name student-attendance-backend --rm -p 8001:8001 student-attendance-backend
```

Stop the container with `Ctrl+C`, or stop a container running in the background with:

```bash
docker rm -f student-attendance-backend
```

## 4. API Contract

All request and response bodies use JSON unless stated otherwise.

| ID | Method | Path | Request body | Success code |
| --- | --- | --- | --- | --- |
| A1 | `POST` | `/register` | `{"username":"student","email":"student@example.com","password":"password"}` | `200` |
| A2 | `POST` | `/login` | `{"email":"student@example.com","password":"password"}` | `200` |
| A3 | `POST` | `/refresh` | No JSON body; send the refresh token in the `refresh_token` header | `200` |
| E1 | `GET` | `/attendance` | No body; send the access token in the `token` header | `200` |
| E2 | `POST` | `/attendance` | `{"student_name":"Student Name","roll_no":"101","attendance_date":"2026-11-23","status":"present"}`; send the access token in the `token` header | `200` |

### Error Rules

| Condition | Status code | Response detail |
| --- | --- | --- |
| Email has no valid `@`/domain format | `422` | `Invalid email format` |
| Email is already registered | `409` | `Email already registered` |
| Login email or password is invalid | `401` | `Invalid email or password` |
| Access token header is missing | `401` | `Access token is missing` |
| Access token is invalid or expired | `401` | `Invalid or expired access token` |
| Refresh token is invalid or expired | `401` | `Invalid or expired refresh token` |
| Attendance status is not `present` or `absent` | `422` | `Status must be either present or absent` |
| Required username, email, password, student name, roll number, or other required value is empty | `422` | FastAPI validation detail |

## 5. Database

SQLite database file: `backend/attendance.db`

### `users`

| Column | Type |
| --- | --- |
| `id` | Integer, primary key |
| `username` | String |
| `email` | String |
| `hashed_password` | String |
| `created_at` | DateTime |

### `attendance`

| Column | Type |
| --- | --- |
| `id` | Integer, primary key |
| `user_id` | Integer, foreign key to `users.id` |
| `student_name` | String |
| `roll_no` | String |
| `attendance_date` | Date |
| `status` | String |
| `created_at` | DateTime |

## 6. Screenshots

Replace each placeholder below with the final screenshot.

![Registration screen](screenshots/registration.png)

Registration screen

![Login screen](screenshots/login.png)

Login screen

![Dashboard](screenshots/dashboard.png)

Dashboard

![Error message](screenshots/error-message.png)

Error message shown on screen

![Swagger docs endpoint](screenshots/docs-endpoint.png)

Endpoint working in `/docs`

![Green GitHub Actions run](screenshots/github-actions.png)

Green GitHub Actions run

## 7. Known Issues

- The deployed EC2 public link is not yet documented as a working link.
- The frontend API URL is hard-coded to `http://127.0.0.1:8001`, so it needs configuration to call the deployed backend.
- CORS is configured only for local Vite origins (`localhost:5173` and `127.0.0.1:5173`), not the EC2 frontend origin.
- Automatic refresh-token handling is not implemented in the frontend.
- The dashboard does not provide a frontend form for creating attendance records; E2 is currently available through the API/Swagger docs.
- The Docker workflow deployment image name and project container name are based on the workflow template and may need project-specific secrets and naming.
- SQLite is file-based and is not suitable for concurrent production workloads or horizontal scaling.

With more time, we would add automated frontend and backend tests, environment-based API configuration, automatic access-token refresh, a complete attendance-entry form, role-based access, pagination and filtering, PostgreSQL instead of SQLite, and HTTPS plus stronger secret and CORS configuration.
