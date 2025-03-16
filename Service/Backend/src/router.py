# =====================================================================================================================
#                   Import
# =====================================================================================================================
from os import environ
from typing import Self, Callable
from functools import wraps

from fastapi import APIRouter, HTTPException
from jose import jwt, JWTError

from database import BaseCollection, BasePipeline, BaseCondition
from error import HttpError, DBException


# =====================================================================================================================
#                   Class
# =====================================================================================================================
class BaseRouter(APIRouter):
    def set_route(self: Self, method: str, url: str, auth: bool=True):
        def decorator(func: Callable):
            @eval(f'self.{method}("{url}")', {"self": self})
            @wraps(func)
            async def wrapper(*args, **kwargs):
                try:
                    if auth:
                        headers = kwargs["request"].headers
                        token = headers.get('Authorization').replace("Bearer ", "")
                        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                        username = payload.get("username")
                        if username is None:
                            raise HttpError.Error_401_Unauthorized()

                        user_data = await auth_collection.get_data(
                            pipelines=[
                                BasePipeline.match(
                                    BaseCondition.equl("$username", username)
                                )
                            ]
                        )
                        if user_data is None:
                            raise HttpError.Error_401_Unauthorized()
                        elif user_data["disabled"]:
                            raise HttpError.Error_400_BadRequest("Disabled User")

                    return await func(*args, **kwargs)

                except JWTError as error:
                    if str(error) == "Signature has expired.":
                        raise HttpError.Error_401_Unauthorized("Signature has expired")

                    raise HttpError.Error_401_Unauthorized()

                except Exception as error:
                    if isinstance(error, DBException):
                        raise error.response
                    elif isinstance(error, HTTPException):
                        raise error
                    else:
                        print("BUG:     ", error)
                        raise HttpError.Error_500_Internal_Server_Error()

            return wrapper
        return decorator


# class BaseAPI:
#     def __init__(self: Self, name: str):
#         # # 檢查必須的 Class
#         # need_class = ["Request", "Response"]
#         # for class_name in need_class:
#         #     if class_name not in dir(self):
#         #         raise TypeError(f"class {class_name} not exist in {self.__class__.__name__}")

#         #     if eval(f"self.{class_name}").__class__.__name__ != "type":
#         #         raise TypeError(f"{class_name} not a class")

#         self.router = BaseRouter()
#         self.collection = BaseCollection(name=name)
#         self.log = LogFile(name=name)


# 有需要在新增抽象類別及方法 (ABC, abstractmethod)


# =====================================================================================================================
#                   Variable
# =====================================================================================================================
SECRET_KEY = environ["JWT_SECRET_KEY"]
ALGORITHM = environ["JWT_ALGORITHM"]
auth_collection = BaseCollection(name="user")
