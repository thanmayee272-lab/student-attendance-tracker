from sqlalchemy import Integer, String, Column, create_engine, Date, DateTime, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime, timedelta, timezone
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


ph = PasswordHasher()
DB_PATH = "attendance.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()


ACCESS_TOKEN_EXPIRY = 30 #mins
REFRESH_TOKEN_EXPIRY = 7*24*60 #mins (7 days)
SECRET_KEY = "SECRET123"
ALGORITHM = "HS256"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    hashed_password = Column(String)
    created_at = Column(DateTime)


class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    student_name = Column(String)
    roll_no = Column(String)
    attendance_date = Column(Date)
    status = Column(String)
    created_at = Column(DateTime)


Base.metadata.create_all(engine)


def attendance_details(record):
    return {
        "id": record.id,
        "student_name": record.student_name,
        "roll_no": record.roll_no,
        "attendance_date": str(record.attendance_date),
        "status": record.status,
        "created_at": str(record.created_at)
    }


# A1
def register_user(username, email, password):
    session = Session(engine)
    user_exists = session.query(User).filter_by(email=email).first()
    if user_exists:
        session.close()
        return False
    user = User(
        username=username,
        email=email,
        hashed_password=ph.hash(password),
        created_at=datetime.now()
    )
    session.add(new_user)
    session.commit()
    session.close()
    return True


# A2
def verify_login(email, password):
    session = Session(engine)
    user = session.query(User).filter_by(email=email).first()
    if user is None:
        session.close()
        return False
    try:
        ph.verify(user.hashed_password, password)
    except VerifyMismatchError:
        session.close()
        return False
    user_id = user.id
    session.close()
    access_token = create_token(user_id=user_id, token_type="access")
    refresh_token = create_token(user_id, token_type="refresh")
    return {"access_token": access_token, "refresh_token": refresh_token}


# A3
def create_token(user_id, token_type):
    time = ACCESS_TOKEN_EXPIRY
    if token_type == "refresh":
        time = REFRESH_TOKEN_EXPIRY
    payload = {
        "user_id": user_id,
        "token_type": token_type,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=time)
    }
    token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token, token_type):
    try:
        payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except:
        return False
    if payload["token_type"] == token_type:
        return payload["user_id"]
    return False


# E1
def get_attendance(user_id):
    session = Session(engine)
    records = session.query(Attendance).filter_by(user_id=user_id).all()
    response = [attendance_details(record) for record in records]
    session.close()
    return response


# E2
def add_attendance(user_id, student_name, roll_no, attendance_date, status):
    session = Session(engine)
    record = Attendance(
        user_id=user_id,
        student_name=student_name,
        roll_no=roll_no,
        attendance_date=attendance_date,
        status=status,
        created_at=datetime.now()
    )
    session.add(record)
    session.commit()
    session.refresh(record)
    response = attendance_details(record)
    session.close()
    return response
