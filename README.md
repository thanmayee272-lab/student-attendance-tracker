# Student Attendance Tracker

A simple attendance app with a React frontend and a FastAPI backend. Users can create an account, sign in, and view attendance records associated with their account.

## Features

- User registration and login
- Access and refresh token authentication
- View attendance records for the signed-in user
- Create attendance records through the backend API
- SQLite storage

## Technologies

| Part | Technologies |
| --- | --- |
| Frontend | React, Vite |
| Backend | Python, FastAPI, SQLAlchemy, SQLite |
| Authentication | JWT, Argon2 password hashing |

## Getting Started

You will need Python and Node.js installed.

### Start the backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

The API runs at `http://127.0.0.1:8001`. Interactive API documentation is available at `http://127.0.0.1:8001/docs`.

### Start the frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite (usually `http://localhost:5173`). The frontend currently sends API requests to `http://127.0.0.1:8001`.

## API Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `POST` | `/register` | Create an account |
| `POST` | `/login` | Sign in and receive tokens |
| `POST` | `/refresh` | Get a new access token |
| `GET` | `/attendance` | List the signed-in user's attendance records |
| `POST` | `/attendance` | Add an attendance record |

Attendance status must be `present` or `absent`. Attendance requests use the `token` header with the access token.

## Work Progress

| Area | Status | Notes |
| --- | --- | --- |
| Backend account registration and login | Complete | Includes password hashing and token creation |
| Backend attendance API | Complete | Supports listing and adding user-specific records |
| Frontend registration and login | Complete | Includes basic success and error messages |
| Frontend attendance dashboard | In progress | Displays records; an attendance-entry form is not yet available in the UI |
| Frontend token refresh | In progress | Backend endpoint exists; automatic refresh is not wired into the frontend |

## Contribution Areas

| Contributor area | Contributions |
| --- | --- |
| Frontend | React/Vite app, registration and login screens, API requests, attendance dashboard, and logout flow |
| Backend | FastAPI endpoints, input validation, authentication and password hashing, SQLAlchemy models, and SQLite persistence |

## Project Structure

```text
backend/
  function.py       # Database models and authentication/attendance logic
  main.py           # FastAPI app and API endpoints
  requirements.txt  # Python dependencies
frontend/
  src/
    components/     # Login, registration, and dashboard
    App.jsx         # App navigation and session state
```
