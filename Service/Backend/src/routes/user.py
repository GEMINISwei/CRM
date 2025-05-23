# =====================================================================================================================
#                   Import
# =====================================================================================================================
from os import environ
from datetime import datetime, timedelta, timezone

from pydantic import BaseModel, Field
from passlib.context import CryptContext
from jose import jwt

from database import BaseCollection, BasePipeline, BaseCondition
from error import HttpError
from router import BaseRouter


# =====================================================================================================================
#                   Class
# =====================================================================================================================
class UserRequest:
    class Create(BaseModel):
        username: str = Field(...)
        password: str = Field(...)

    class Login(BaseModel):
        username: str = Field(...)
        password: str = Field(...)

    class Logout(BaseModel):
        username: str = Field(...)


class UserResponse:
    class Operate(BaseModel):
        username: str = Field(...)

    class Login(BaseModel):
        username: str = Field(...)
        token_type: str = Field(default="bearer")
        access_token: str = Field(...)
        shift: str = Field(...)


# =====================================================================================================================
#                   Variable
# =====================================================================================================================
router = BaseRouter()
collection = BaseCollection(name="user")
pwd_context = CryptContext(schemes=["bcrypt"])
SECRET_KEY = environ["JWT_SECRET_KEY"]
ALGORITHM = environ["JWT_ALGORITHM"]
ACCESS_TOKEN_EXPIRE_HOURS = int(environ["JWT_ACCESS_TOKEN_EXPIRE_HOURS"])
ACCESS_TOKEN_EXPIRE_MINUTES = int(environ["JWT_ACCESS_TOKEN_EXPIRE_MINUTES"])


# =====================================================================================================================
#                   User Router
# =====================================================================================================================
@router.set_route(method="post", url="/users", auth=False)
async def create_user(
    form_data: UserRequest.Create
) -> UserResponse.Operate:
    new_data = form_data.model_dump()
    new_data["password"] = pwd_context.hash(new_data["password"])

    new_user = await collection.create_data(
        data=new_data
    )

    return new_user


@router.set_route(method="post", url="/users/login", auth=False)
async def user_login(
    form_data: UserRequest.Login
) -> UserResponse.Login:
    login_data = form_data.model_dump()


    user_data = await collection.get_data(
        pipelines=[
            BasePipeline.match(
                BaseCondition.equl("$username", login_data["username"])
            )
        ]
    )
    if user_data is None:
        raise HttpError.Error_401_Unauthorized("Username not found")

    is_verify = pwd_context.verify(form_data.password, user_data["password"])
    if not is_verify:
        raise HttpError.Error_401_Unauthorized("Incorrect password")

    # 驗證成功後, 產生 JWT
    token = jwt.encode({
        "username": user_data["username"],
        "exp": datetime.now(timezone.utc) + timedelta(
            hours=ACCESS_TOKEN_EXPIRE_HOURS,
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    }, SECRET_KEY, algorithm=ALGORITHM)

    update_user = await collection.update_data(
        find={
            "id": user_data["id"]
        },
        data={
            "access_token": token
        }
    )

    return update_user


@router.set_route(method="post", url="/users/logout", auth=False)
async def user_logout(
    form_data: UserRequest.Logout
) -> UserResponse.Operate:
    logout_data = form_data.model_dump()

    user_data = await collection.get_data(
        pipelines=[
            BasePipeline.match(
                BaseCondition.equl("$username", logout_data["username"])
            )
        ]
    )

    update_user = await collection.update_data(
        find={
            "id": user_data["id"]
        },
        data={
            "access_token": ""
        }
    )

    return update_user
