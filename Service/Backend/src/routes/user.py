# =====================================================================================================================
#                   Import
# =====================================================================================================================
from os import environ
from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
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

    class Checkout(BaseModel):
        property: dict = Field(...)
        game_stock_all: dict = Field(...)
        game_stock: dict = Field(...)


# =====================================================================================================================
#                   Variable
# =====================================================================================================================
router = BaseRouter()
collection = BaseCollection(name="user")
login_record_collection = BaseCollection(name="login_record")
property_collection = BaseCollection(name="property")
game_collection = BaseCollection(name="game")
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

    await login_record_collection.create_data(
        data={
            "user_id": user_data["id"],
            "login_time": datetime.now()
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
    show_mode = 'date' if request.query_params.get('search_time').__len__() == 10 else 'month'

    if show_mode == 'date':
        search_time = datetime.strptime(request.query_params.get('search_time'), '%Y-%m-%d')
        current_date_start = search_time.replace(hour=0, minute=0, second=0, microsecond=0)
        current_date_end = current_date_start + relativedelta(days=1)

        output_group = {
            "user_with_search_time": {
                "$concat": [
                    "$completed_by",
                    "_x_",
                    { "$dateToString": { "format": "%Y-%m-%d", "date": "$time_at" } }
                ]
            }
        }
    elif show_mode == 'month':
        search_time = datetime.strptime(request.query_params.get('search_time'), '%Y-%m')
        current_date_start = search_time.replace(hour=0, minute=0, second=0, microsecond=0)
        current_date_end = current_date_start + relativedelta(months=1)

        output_group = {
            "user_with_search_time": {
                "$concat": [
                    "$completed_by",
                    "_x_",
                    { "$dateToString": { "format": "%Y-%m", "date": "$time_at" } }
                ]
            }
        }


    result_data = await trade_collection.get_list_data(
        pipelines=[
            BasePipeline.match(
                BaseCondition.and_expression(
                    BaseCondition.equl("$game_id", request.query_params.get("game_id")),
                    BaseCondition.greater_than("$time_at", current_date_start, equl=True),
                    BaseCondition.less_than("$time_at", current_date_end),
                    BaseCondition.equl("$is_cancel", False),
                    BaseCondition.not_equl("$completed_by", None),
                )
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
                        "$game_coin",
                        0
                    ),
                    "real_out_coin": BaseCondition.if_then_else(
                        BaseCondition.equl("$base_type", "money_in"),
                        "$game_coin",
                        0
                    ),
                    "money_fee": BaseCalculate.subtract(
                        "$stage_fee",
                        "$charge_fee",
                    ),
                    **output_group
                }
            ),
            {
                "$group": {
                    "_id": "$user_with_search_time",
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

    # 在最後面需要補上篩選出來的總和
    result_data['list_data'].append({
        "_id": "Total_x_-",
        "daily_in_money": sum(single_data["daily_in_money"] for single_data in result_data['list_data']),
        "daily_out_money": sum(single_data["daily_out_money"] for single_data in result_data['list_data']),
        "daily_in_coin": sum(single_data["daily_in_coin"] for single_data in result_data['list_data']),
        "daily_out_coin": sum(single_data["daily_out_coin"] for single_data in result_data['list_data']),
        "money_fee": sum(single_data["money_fee"] for single_data in result_data['list_data']),
        "no_charge_coin": sum(single_data["no_charge_coin"] for single_data in result_data['list_data']),
        "activity_coin": sum(single_data["activity_coin"] for single_data in result_data['list_data']),
    })

    return result_data


@router.set_route(method="get", url="/users/trade_checkout")
async def get_user_trade_checkout(
    request: Request
) -> UserResponse.Checkout:
    now_time = datetime.now()
    mode = request.query_params.get('mode')
    username = request.query_params.get('username')

    # 利用 Mode 判斷要抓取的時間區間
    if mode == 'day':
        time_start = now_time.replace(hour=7, minute=0, second=0, microsecond=0)
        time_end = time_start + relativedelta(hours=12)
    elif mode == 'night-1':
        time_start = now_time.replace(hour=19, minute=0, second=0, microsecond=0)
        time_end = time_start + relativedelta(hours=5)
    elif mode == 'night-2':
        time_start = now_time.replace(hour=0, minute=0, second=0, microsecond=0)
        time_end = time_start + relativedelta(hours=7)

    # 所有資產餘額
    property_data = await property_collection.get_list_data(
        pipelines=[
            BasePipeline.match(
                BaseCondition.equl("$kind", "bank"),
            ),
            BasePipeline.lookup(
                name="trade",
                key="id",
                conditions=[
                    BaseCondition.equl("$is_cancel", False),
                    BaseCondition.equl("$property_id", "$$id"),
                ],
                pipelines=[
                    BasePipeline.project(
                        custom={
                            "final_money": BaseCalculate.sum(
                                BaseCondition.if_then_else(
                                    BaseCondition.equl("$base_type", "money_in"),
                                    "$money",
                                    BaseCalculate.multiply("$money", -1)
                                ),
                                "$charge_fee",
                                BaseCalculate.multiply("$stage_fee", -1),
                                BaseCalculate.multiply("$details.money_correction", -1),
                                BaseCalculate.multiply("$details.diff_bank_fee", -1),
                            )
                        }
                    )
                ]
            ),
            BasePipeline.project(
                name="property",
                custom={
                    "balance": BaseCalculate.sum(
                        "$init_amount",
                        BaseCalculate.sum("$trade.final_money")
                    )
                }
            )
        ]
    )

    # 依遊戲顯示, 庫存、轉入轉出幣、活動幣、官方手續費、營業額
    game_stock_all_data = await game_collection.get_list_data(
        pipelines=[
            BasePipeline.lookup(
                name="stock",
                key="id",
                conditions=[
                    BaseCondition.equl("$game_id", "$$id")
                ],
                pipelines=[
                    BasePipeline.lookup(
                        name="trade",
                        key="id",
                        conditions=[
                            BaseCondition.equl("$is_cancel", False),
                            BaseCondition.equl("$stock_id", "$$id"),
                        ],
                        pipelines=[
                            BasePipeline.project(
                                show=['activity_coin'],
                                custom={
                                    "final_coin": BaseCalculate.sum(
                                        BaseCondition.if_then_else(
                                            BaseCondition.equl("$base_type", "money_in"),
                                            BaseCalculate.multiply("$game_coin", -1),
                                            "$game_coin"
                                        ),
                                        BaseCalculate.multiply("$game_coin_fee", -1),
                                        BaseCalculate.multiply("$details.game_coin_correction", -1),
                                        BaseCalculate.multiply("$details.game_coin_fee_correction", -1)
                                    )
                                }
                            ),
                        ],
                    ),
                    BasePipeline.project(
                        name="stock",
                        custom={
                            "balance": BaseCalculate.sum(
                                "$init_amount",
                                BaseCalculate.sum("$trade.final_coin")
                            )
                        }
                    ),
                ],
            ),
        ],
    )

    game_stock_data = await game_collection.get_list_data(
        pipelines=[
            BasePipeline.lookup(
                name="stock",
                key="id",
                conditions=[
                    BaseCondition.equl("$game_id", "$$id")
                ],
                pipelines=[
                    BasePipeline.lookup(
                        name="trade",
                        key="id",
                        conditions=[
                            BaseCondition.equl("$is_cancel", False),
                            BaseCondition.equl("$stock_id", "$$id"),
                            BaseCondition.equl("$completed_by", username),
                            BaseCondition.greater_than("$time_at", time_start, equl=True),
                            BaseCondition.less_than("$time_at", time_end)
                        ],
                        pipelines=[
                            BasePipeline.project(
                                show=['activity_coin'],
                                custom={
                                    "money_in": BaseCalculate.sum(
                                        BaseCondition.if_then_else(
                                            BaseCondition.equl("$base_type", "money_in"),
                                            "$money",
                                            0
                                        ),
                                    ),
                                    "money_out": BaseCalculate.sum(
                                        BaseCondition.if_then_else(
                                            BaseCondition.equl("$base_type", "money_out"),
                                            "$money",
                                            0
                                        ),
                                        "$details.money_correction",
                                    ),
                                    "game_coin_in": BaseCalculate.sum(
                                        BaseCondition.if_then_else(
                                            BaseCondition.equl("$base_type", "money_out"),
                                            "$game_coin",
                                            0
                                        ),
                                    ),
                                    "game_coin_out": BaseCalculate.subtract(
                                        BaseCalculate.sum(
                                            BaseCondition.if_then_else(
                                                BaseCondition.equl("$base_type", "money_in"),
                                                "$game_coin",
                                                0
                                            ),
                                            "$details.game_coin_correction",
                                        ),
                                        "$activity_coin",
                                    ),
                                    "game_coin_fee_out": BaseCalculate.sum(
                                        "$game_coin_fee",
                                        "$details.game_coin_fee_correction",
                                    ),
                                }
                            ),
                        ],
                    ),
                    BasePipeline.project(
                        name="stock",
                        custom={
                            "money_out": BaseCalculate.sum("$trade.money_out"),
                            "money_in": BaseCalculate.sum("$trade.money_in"),
                            "game_coin_in": BaseCalculate.sum("$trade.game_coin_in"),
                            "game_coin_out": BaseCalculate.sum("$trade.game_coin_out"),
                            "activity_coin": BaseCalculate.sum("$trade.activity_coin"),
                            "game_coin_fee_out": BaseCalculate.sum("$trade.game_coin_fee_out"),
                            "game_coin_out_total": BaseCalculate.sum(
                                BaseCalculate.sum("$trade.game_coin_out"),
                                BaseCalculate.sum("$trade.activity_coin"),
                                BaseCalculate.sum("$trade.game_coin_fee_out"),
                            ),
                        }
                    ),
                ],
            ),
        ],
    )

    return {
        "property": property_data,
        "game_stock_all": game_stock_all_data,
        "game_stock": game_stock_data,
    }
