import jwt
import datetime
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer
from models.User import User
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
ALGORITHM = "HS256"
TOKEN_EXPIRATION_MINUTES = 300

security = HTTPBearer()

def create_access_token(user: User) -> str:
    payload = {
        "sub": user.email,
        "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=TOKEN_EXPIRATION_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(token: str = Security(security)) -> User:
    email = decode_access_token(token.credentials)
    user = User.get_or_none(User.email == email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user")
    return user