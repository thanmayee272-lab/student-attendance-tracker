from fastapi import FastAPI, HTTPException, Header, Body
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
from pydantic import BaseModel, Field
import function

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


STATUS = ["present", "absent"]

def check_token(token):
    if token is None:
        raise HTTPException(status_code=401, detail="Access token is missing")
    user_id = function.verify_token(token=token, token_type="access")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired access token")
    return user_id


class UserIn(BaseModel):
    username: str = Field(min_length=1)
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)


class AttendanceCreate(BaseModel):
    student_name: str = Field(min_length=1)
    roll_no: str = Field(min_length=1)
    attendance_date: date
    status: str


# A1
@app.post("/register")
def register_user(user: UserIn):
    if "@" not in user.email or "." not in user.email.split("@")[-1]:
        raise HTTPException(status_code=422, detail="Invalid email format")
    if function.register_user(user.username, user.email, user.password):
        return {"message": "Registration successfully"}
    raise HTTPException(status_code=409, detail="Email already registered")


# A2
@app.post("/login")
def login(email=Body(), password=Body()):
    token = function.verify_login(email=email, password=password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return token


# A3
@app.post("/refresh")
def refresh_token(refresh_token = Header(None)):
    user_id = function.verify_token(token=refresh_token, token_type="refresh")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    access_token = function.create_token(user_id=user_id, token_type="access")
    return {"access_token": access_token}


# E1
@app.get("/attendance")
def get_attendance(token = Header(None)):
    user_id = check_token(token)
    return function.get_attendance(user_id)


# E2
@app.post("/attendance")
def add_attendance(attendance: AttendanceCreate, token=Header(None)):
    user_id = check_token(token)
    if attendance.status not in STATUS:
        raise HTTPException(status_code=422, detail="Status must be either present or absent")
    return function.add_attendance(user_id, attendance.student_name, attendance.roll_no, attendance.attendance_date, attendance.status)