# =====================================================================================================================
#                   Import
# =====================================================================================================================
from pydantic import BaseModel, Field
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Request
from passlib.context import CryptContext
from jose import jwt, JWTError
from database import users_collection
from functools import wraps
from typing import List
import os
import http_error


# =====================================================================================================================
#                   Schema
# =====================================================================================================================
class UserSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
    disabled: bool = Field(default=False)
    token: str = Field(default="")
    level_group: str = Field(default="Initialize")


# =====================================================================================================================
#                   API Request
# =====================================================================================================================
class UserCreateRequest(BaseModel):
    username: str = Field(...)
    password: str = Field(...)


class UserLoginRequest(BaseModel):
    username: str = Field(...)
    password: str = Field(...)


class UserLogoutRequest(BaseModel):
    username: str = Field(...)


# =====================================================================================================================
#                   API Response
# =====================================================================================================================
class UserCreateResponse(BaseModel):
    username: str = Field(...)


class UserLoginResponse(BaseModel):
    username: str = Field(...)
    token_type: str = Field(default="bearer")
    access_token: str = Field(...)


class UserLogoutResponse(BaseModel):
    pass


class UserOnlineResponse(BaseModel):
    users: List[str] = Field(default_factory=lambda: [])

# =====================================================================================================================
#                   Declare Variable
# =====================================================================================================================
router = APIRouter()
SECRET_KEY = os.environ["JWT_SECRET_KEY"]
ALGORITHM = os.environ["JWT_ALGORITHM"]
ACCESS_TOKEN_EXPIRE_HOURS = int(os.environ["JWT_ACCESS_TOKEN_EXPIRE_HOURS"])
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["JWT_ACCESS_TOKEN_EXPIRE_MINUTES"])


# =====================================================================================================================
#                   Function Prototype
# =====================================================================================================================
def token_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            headers = kwargs["request"].headers
            token = headers.get('Authorization').replace("Bearer ", "")
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("username")
            if username is None:
                raise http_error.Error_401_Unauthorized()

            user_data = await users_collection.find_one({ "username": username })
            if user_data is None:
                raise http_error.Error_401_Unauthorized()
            elif user_data["disabled"]:
                raise http_error.Error_400_BadRequest("Disabled User")

            return await func(*args, **kwargs)

        except JWTError as error:
            if str(error) == "Signature has expired.":
                print(1)
                raise http_error.Error_401_Unauthorized("Signature has expired")

            raise http_error.Error_401_Unauthorized()

    return wrapper


# =====================================================================================================================
#                   User Router
# =====================================================================================================================
@router.post("/users")
async def create_user(
    form_data: UserCreateRequest
) -> UserCreateResponse:
    try:
        pwd_context = CryptContext(schemes=["bcrypt"])

        new_data = form_data.model_dump()
        new_data["password"] = pwd_context.hash(new_data["password"])
        new_user = UserSchema(**new_data).model_dump()

        await users_collection.insert_one(new_user)

        return new_user

    except:
        raise http_error.Error_500_Internal_Server_Error("User create failure")


@router.post("/users/login")
async def user_login(
    form_data: UserLoginRequest
) -> UserLoginResponse:
    try:
        # 確認資料庫中是否有此 User, 並進行驗證
        pwd_context = CryptContext(schemes=["bcrypt"])
        login_data = form_data.model_dump()
        user_data = await users_collection.find_one({ "username": login_data["username"] })
        if user_data is None:
            raise http_error.Error_401_Unauthorized("Username not found")

        is_verify = pwd_context.verify(form_data.password, user_data["password"])
        if is_verify == False:
            raise http_error.Error_401_Unauthorized("Incorrect password")

        # 驗證成功後, 產生 JWT
        token = jwt.encode({
            "username": user_data["username"],
            "exp": datetime.now(timezone.utc) + timedelta(
                hours=ACCESS_TOKEN_EXPIRE_HOURS,
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )
        }, SECRET_KEY, algorithm=ALGORITHM)

        await users_collection.update_one({ "username": login_data["username"] }, {
            "$set": {
                "token": token
            }
        })

        return {
            "username": user_data["username"],
            "access_token": token,
        }

    except:
        raise http_error.Error_500_Internal_Server_Error("User login failure")


@router.post("/users/logout")
async def user_logout(
    form_data: UserLogoutRequest
) -> UserLogoutResponse:
    try:
        logout_data = form_data.model_dump()
        await users_collection.update_one({ "username": logout_data["username"] }, {
            "$set": {
                "token": ""
            }
        })

        return {}
    except Exception as error:
        print(error)
        raise http_error.Error_500_Internal_Server_Error()


@router.get("/users/online")
@token_required
async def get_online_users(
    request: Request
) -> UserOnlineResponse:
    try:
        users_data = await users_collection.aggregate([
            {
                "$match": {
                    "token": {
                        "$ne": ""
                    }
                }
            }
        ]).to_list(length = None)

        return {
            "users": list(map(lambda x: x['username'], users_data))
        }

    except Exception as error:
        print(error)
        raise http_error.Error_500_Internal_Server_Error()
