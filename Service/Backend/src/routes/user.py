# =====================================================================================================================
#                   Import
# =====================================================================================================================
from os import environ
from datetime import datetime, timedelta, timezone
from typing import List

from pydantic import BaseModel, Field
from passlib.context import CryptContext
from jose import jwt
from fastapi import Request

from database import BaseCollection, BasePipeline, BaseCondition, BaseCalculate
from error import HttpError
from router import BaseRouter


# =====================================================================================================================
#                   Class
# =====================================================================================================================
class UserRequest:
    class Create(BaseModel):
        nickname: str = Field(...)
        username: str = Field(...)
        password: str = Field(...)
        shift: str = Field(...)
        level_group: str = Field(default="Initialize")


    class Login(BaseModel):
        username: str = Field(...)
        password: str = Field(...)

    class Logout(BaseModel):
        username: str = Field(...)


class UserResponse:
    class Operate(BaseModel):
        nickname: str = Field(...)

    class Login(BaseModel):
        nickname: str = Field(...)
        username: str = Field(...)
        token_type: str = Field(default="bearer")
        access_token: str = Field(...)
        shift: str = Field(...)
        level_group: str = Field(...)
        permissions: object = Field(...)

    class List(BaseModel):
        list_data: List[dict] = Field(...)
        page_count: int = Field(...)


# =====================================================================================================================
#                   Variable
# =====================================================================================================================
router = BaseRouter()
collection = BaseCollection(name="user")
trade_collection = BaseCollection(name="trade")
setting_collection = BaseCollection(name="setting")
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
            ),
        ]
    )
    if user_data is None:
        raise HttpError.Error_401_Unauthorized("Username not found")

    is_verify = pwd_context.verify(form_data.password, user_data["password"])
    if not is_verify:
        raise HttpError.Error_401_Unauthorized("Incorrect password")

    permission_data = await setting_collection.get_data(
        pipelines=[
            BasePipeline.match(
                BaseCondition.equl("$collection_name", "permission")
            )
        ]
    )

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

    # Admin 預設權限全開, 不需要給個別畫面的權限
    if user_data['level_group'] == 'Admin':
        update_user['level_group'] = 'Admin'
        update_user['permissions'] = {}
    # 找出對應權限的頁面權限資訊
    elif permission_data['fields'].get(user_data['level_group']):
        update_user['level_group'] = user_data['level_group']
        update_user['permissions'] = permission_data['fields'][user_data['level_group']]
    # 沒有找到對應的, 則直接給予初始權限 (當作沒權限)
    else:
        update_user['level_group'] = "Initialize"
        update_user['permissions'] = {}

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


@router.set_route(method="get", url="/users/trade_performance")
async def get_user_trade_performance(
    request: Request
) -> UserResponse.List:
    result_data = await trade_collection.get_list_data(
        pipelines=[
            BasePipeline.match(
                BaseCondition.equl("$game_id", request.query_params.get("game_id")),
            ),
            BasePipeline.match(
                BaseCondition.equl("$is_cancel", False),
                BaseCondition.not_equl("$completed_by", None),
            ),
            BasePipeline.project(
                show=[
                    "time_at",
                    "completed_by",
                    "no_charge",
                    "no_charge_coin",
                    "activity_coin"
                ],
                custom={
                    "real_in_money": BaseCondition.if_then_else(
                        BaseCondition.equl("$base_type", "money_in"),
                        BaseCalculate.sum(
                            "$money",
                            "$charge_fee",
                            BaseCalculate.multiply("$stage_fee", -1),
                        ),
                        0
                    ),
                    "real_out_money": BaseCondition.if_then_else(
                        BaseCondition.equl("$base_type", "money_out"),
                        BaseCalculate.sum(
                            "$money",
                            "$charge_fee",
                            BaseCalculate.multiply("$stage_fee", -1),
                            BaseCalculate.multiply("$details.money_correction", 1),
                            BaseCalculate.multiply("$details.diff_bank_fee", 1),
                        ),
                        0
                    ),
                    "real_in_coin": BaseCondition.if_then_else(
                        BaseCondition.equl("$base_type", "money_out"),
                        BaseCalculate.sum(
                            "$game_coin",
                        ),
                        0
                    ),
                    "real_out_coin": BaseCondition.if_then_else(
                        BaseCondition.equl("$base_type", "money_in"),
                        BaseCalculate.sum(
                            "$game_coin",
                            "$game_coin_fee",
                        ),
                        0
                    ),
                    "money_fee": BaseCalculate.subtract(
                        "$stage_fee",
                        "$no_charge",
                    ),
                    "user_with_date": {
                        "$concat": [
                            "$completed_by",
                            "_x_",
                            { "$dateToString": { "format": "%Y-%m-%d", "date": "$time_at" } }
                        ]
                    }
                }
            ),
            {
                "$group": {
                    "_id": "$user_with_date",
                    "daily_in_money": { "$sum": "$real_in_money" },
                    "daily_out_money": { "$sum": "$real_out_money" },
                    "daily_in_coin": { "$sum": "$real_in_coin" },
                    "daily_out_coin": { "$sum": "$real_out_coin" },
                    "money_fee": { "$sum": "$money_fee" },
                    "no_charge_coin": { "$sum": "$no_charge_coin" },
                    "activity_coin": { "$sum": "$activity_coin" },
                }
            },
            {
                "$sort": { "_id": 1 }
            }
        ]
    )

    return result_data
