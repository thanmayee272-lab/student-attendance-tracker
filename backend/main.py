from fastapi import FastAPI, HTTPException, Header, Body
from fastapi.middleware.cors import CORSMiddleware
import functions
from pydantic import BaseModel
from datetime import date

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"])


@app.get("/")
def hello():
    return {"message": "Welcome to Class_rep Movie"}

@app.post("/register")
def register(user: User):
    if functions.register_user(user_name=user.username, password=user.password, user_type=user.user_type):
        return {"message": "User registered successfully"}
    raise HTTPException(status_code=400, detail="User already exists")        


@app.post("/login")
def login(username: str = Body(), password: str = Body()):
    token = functions.verify_login(username=username, password=password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid")
    return token


@app.post("/refresh")
def refresh(refresh_token = Header(None)):
    payload = functions.verify_token(token=refresh_token, token_type = "refresh")
    if not payload:
        raise HTTPException(status_code = 401, detail = "Invalid or refresh token")
    access_token = functions.create_token(username=payload["username"], user_type=payload["user_type"], token_type = "access")
    return {"access_token": access_token}