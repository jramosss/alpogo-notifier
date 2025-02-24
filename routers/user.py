from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr, BaseModel, Field

from models.User import User
from services.auth import create_access_token, get_current_user

router = APIRouter()


class UserModel(BaseModel):
    email: EmailStr = Field(default=None)
    # todo add validations for password like min length
    password: str


@router.post("/register/")
def register(user: UserModel):
    if User.get_or_none(User.email == user.email):
        raise HTTPException(status_code=400, detail="User already exists")

    User.create_user(user.email, user.password)
    return {"message": "User created"}


@router.post("/login/")
def login(email: str, password: str):
    user = User.get_or_none(User.email == email)
    if not user or not user.check_password(password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user)
    return {"access_token": token}
