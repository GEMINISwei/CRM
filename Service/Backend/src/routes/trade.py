# =====================================================================================================================
#                   Import
# =====================================================================================================================
from typing import Optional, Self
from datetime import datetime, timedelta

from fastapi import Request
from pydantic import BaseModel, Field

from router import BaseRouter
from database import BaseCollection, BasePipeline
# from utils.match import find_match, create_match


# =====================================================================================================================
#                   Class
# =====================================================================================================================
class TradeRequest:
    class Create(BaseModel):
        member_id: str = Field(...)
        property_id: str = Field(...)
        stock_id: str = Field(...)
        base_type: str = Field(...)
        money: int = Field(...)
        charge_fee: int = Field(...)
        game_coin: int = Field(...)
        game_coin_fee: int = Field(...)
        stage_fee: Optional[int] = Field(default=0)
        money_correction: Optional[int] = Field(default=0)
        game_coin_correction: Optional[int] = Field(default=0)
        details: Optional[dict] = Field(default={})
        is_matched: Optional[bool] = Field(default=False)

        def model_post_init(self: Self, _):
            self.is_matched = True if self.base_type == "money_out" else False

    class Update(BaseModel):
        details: Optional[dict] = Field(default = {})

    class Check(BaseModel):
        checked_user: str = Field(...)


class TradeResponse:
    class Operate(BaseModel):
        order_number: str = Field(...)

    class Edit(BaseModel):
        pass


# =====================================================================================================================
#                   Variable
# =====================================================================================================================
router = BaseRouter()
collection = BaseCollection(name="trade")


# =====================================================================================================================
#                   Function
# =====================================================================================================================
async def get_order_number(type: str):
    try:
        now_time = datetime.now()
        current_date_start = now_time.replace(hour=0, minute=0, second=0, microsecond=0)
        current_date_end = current_date_start + timedelta(days=1)
        today_exist_trades = await collection.get_list_data(
            pipelines=[
                BasePipeline.create_match(
                    range={
                        "time_at": [current_date_start, current_date_end]
                    }
                )
            ]
        )

        order_type = "B" if type == "money_out" else "S"
        order_date = now_time.strftime("%Y%m%d")
        order_index = len(today_exist_trades["list_data"]) + 1

        return f"{order_type}{order_date}{order_index:0>3d}"

    except Exception as error:
        print(error)


# =====================================================================================================================
#                   Trade Router
# =====================================================================================================================
@router.set_route(method="post", url="/trades")
async def create_trade(
    request: Request, form_data: TradeRequest.Create
) -> TradeResponse.Operate:
    new_data = form_data.model_dump()
    new_data["order_number"] = await get_order_number(type=new_data["base_type"])

    new_trade = await collection.create_data(
        data=new_data
    )

    # trade_id = str(result_trade.inserted_id)
    # money = new_data["money"]

    # 出金 (買入) 時, 建立媒合單
    # if new_data["base_type"] == "money_out":
    #     await create_match(trade_id, money)

    #     # 建立新的媒合單, 順便媒合尚未媒合的交易單
    #     no_matched_trades = await trades_collection.aggregate([
    #         {
    #             "$match": {
    #                 "is_cancel": {
    #                     "$eq": False
    #                 },
    #                 "is_matched": {
    #                     "$eq": False
    #                 }
    #             }
    #         }
    #     ]).to_list(length=None)

    #     for trade in no_matched_trades:
    #         find_result = await find_match(str(trade["_id"]), trade["money"])
    #         await trades_collection.update_one({ "_id": trade["_id"] }, {
    #             "$set": { "is_matched": find_result }
    #         })

    # # 入金 (賣出) 時, 開始媒合
    # elif new_data["base_type"] == "money_in":
    #     find_result = await find_match(trade_id, money)
    #     await trades_collection.update_one({ "_id": ObjectId(trade_id) }, {
    #         "$set": { "is_matched": find_result }
    #     })

    return new_trade



@router.set_route(method="get", url="/trades/{id}")
async def get_trade(
    request: Request
):
    show_data = await collection.get_data(
        pipelines=[
            BasePipeline.create_match(
                equl={
                    "id": request.path_params.get("id")
                }
            )
        ]
    )

    return show_data


@router.set_route(method="get", url="/trades")
async def get_trade_list(
    request: Request
):
    result_data = await collection.get_list_data(
        pipelines=[
            BasePipeline.create_match(
                equl={
                    "is_cancel": False,
                    "property_id": request.query_params.get("property_id")
                }
            ),
            # 計算以前到現在的所有交易
            BasePipeline.create_lookup(
                name="trade",
                key="id",
                lets={
                    "time_at": "$time_at",
                    "property_id": "$property_id"
                },
                match_conditions=[
                    BasePipeline.create_eq_condition("$is_cancel", False),
                    BasePipeline.create_eq_condition("$property_id", "$$property_id"),
                    BasePipeline.create_lte_condition("$time_at", "$$time_at")
                ],
                pipelines=[
                    BasePipeline.create_project(
                        custom={
                            "final_money": BasePipeline.create_sum(
                                items=[
                                    BasePipeline.create_if_condition(
                                        if_expn=BasePipeline.create_eq_condition("$base_type", "money_in"),
                                        then_expn="$money",
                                        else_expn=BasePipeline.create_multiply(
                                            items=["$money", -1]
                                        )
                                    ),
                                    BasePipeline.create_multiply(
                                        items=["$charge_fee", -1]
                                    ),
                                    BasePipeline.create_multiply(
                                        items=["$details.money_correction", -1]
                                    )
                                ]
                            )
                        }
                    )
                ]
            ),
            BasePipeline.create_lookup(
                name="member",
                key="member_id",
                pipelines=[
                    BasePipeline.create_lookup(
                        name="game",
                        key="game_id"
                    )
                ]
            ),
            BasePipeline.create_lookup(
                name="property",
                key="property_id"
            ),
            BasePipeline.create_lookup(
                name="stock",
                key="stock_id"
            ),
            BasePipeline.create_project(
                name="trade",
                show=["member", "stock"],
                custom={
                    "balance": BasePipeline.create_sum(
                        items=[
                            BasePipeline.create_sum(
                                items=[
                                    "$property.init_amount"
                                ]
                            ),
                            BasePipeline.create_sum(
                                items=[
                                    "$trade.final_money"
                                ]
                            ),
                        ]
                    )
                }
            )
        ],
        page=request.query_params.get("page"),
        count=request.query_params.get("count"),
        reverse=True
    )

    return result_data


@router.set_route(method="patch", url="/trades/{id}")
async def update_trade(
    request: Request, form_data: TradeRequest.Update
) -> TradeResponse.Operate:
    print(form_data.model_dump())
    update_data = await collection.update_data(
        find={
            "id": request.path_params.get("id")
        },
        data=form_data.model_dump()
    )

    return update_data


@router.set_route(method="patch", url="/trades/{id}/check")
async def update_trade_check(
    request: Request, form_data: TradeRequest.Check
) -> TradeResponse.Operate:
    update_data = await collection.update_data(
        find={
            "id": request.path_params.get("id")
        },
        data=form_data.model_dump()
    )

    return update_data


@router.set_route(method="delete", url="/trades/{id}")
async def cancel_trade(
    request: Request
) -> TradeResponse.Operate:
    cancel_data = await collection.update_data(
        find={
            "id": request.path_params.get("id")
        },
        data={
            "is_cancel": True
        }
    )

    return cancel_data
