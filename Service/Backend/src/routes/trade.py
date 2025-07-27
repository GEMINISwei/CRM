# =====================================================================================================================
#                   Import
# =====================================================================================================================
from typing import Optional, Self
from datetime import datetime, timedelta

from fastapi import Request
from pydantic import BaseModel, Field

from router import BaseRouter
from database import BaseCollection, BasePipeline, BaseCondition, BaseCalculate
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
        created_by: str = Field(...)
        # stage_fee: Optional[int] = Field(default=0)
        money_correction: Optional[int] = Field(default=0)
        game_coin_correction: Optional[int] = Field(default=0)
        details: Optional[dict] = Field(default={})
        completed_by: Optional[str] = Field(default=None)
        checked_by: Optional[str] = Field(default=None)
        is_matched: Optional[bool] = Field(default=False)

        def model_post_init(self: Self, _):
            self.is_matched = True if self.base_type == "money_out" else False

    class Update(BaseModel):
        details: Optional[dict] = Field(default = {})

    class Complete(BaseModel):
        completed_by: str = Field(...)
        time_at: datetime = Field(default_factory=lambda: datetime.now())
        is_reset_time: Optional[bool] = Field(default=False)

        def model_post_init(self: Self, _):
            if not self.is_reset_time:
                delattr(self, "time_at")

    class Check(BaseModel):
        checked_by: str = Field(...)


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
property_collection = BaseCollection(name="property")
setting_collection = BaseCollection(name="setting")


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
                BasePipeline.match(
                    BaseCondition.and_expression(
                        BaseCondition.greater_than("$time_at", current_date_start, equl=True),
                        BaseCondition.less_than("$time_at", current_date_end)
                    )
                )
            ]
        )

        order_type = "B" if type == "money_out" else "S"
        order_date = now_time.strftime("%Y%m%d")
        order_index = len(today_exist_trades["list_data"]) + 1

        return f"{order_type}{order_date}{order_index:0>3d}"

    except Exception as error:
        print(error)


async def get_stage_fee(property_id: str):
    try:
        property_data = await property_collection.get_data(
            pipelines=[
                BasePipeline.match(
                    BaseCondition.equl("$id", property_id)
                )
            ]
        )

        trade_setting = await setting_collection.get_data(
            pipelines=[
                BasePipeline.match(
                    BaseCondition.equl("$collection_name", "trade")
                )
            ]
        )

        return trade_setting["fields"]["fee"][f"{property_data["kind"]}_stage"]

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
    new_data["stage_fee"] = await get_stage_fee(property_id=new_data["property_id"])

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
            BasePipeline.match(
                BaseCondition.equl("$id", request.path_params.get("id"))
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
            BasePipeline.match(
                BaseCondition.equl("$is_cancel", False),
            ),
            BasePipeline.match(
                BaseCondition.equl("$property_id", request.query_params.get("property_id"))
            ),
            # 計算以前到現在的所有交易
            BasePipeline.lookup(
                name="trade",
                key="id",
                lets={
                    "time_at": "$time_at",
                    "property_id": "$property_id"
                },
                conditions=[
                    BaseCondition.equl("$is_cancel", False),
                    BaseCondition.equl("$property_id", "$$property_id"),
                    BaseCondition.less_than("$time_at", "$$time_at", equl=True)
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
                                # BaseCalculate.multiply("$charge_fee", -1),
                                BaseCalculate.multiply("$details.money_correction", -1),
                                BaseCalculate.multiply("$details.diff_bank_fee", -1),
                            )
                        }
                    )
                ]
            ),
            BasePipeline.lookup(
                name="member",
                key="member_id",
                pipelines=[
                    BasePipeline.lookup(
                        name="game",
                        key="game_id"
                    )
                ]
            ),
            BasePipeline.lookup(
                name="property",
                key="property_id"
            ),
            BasePipeline.lookup(
                name="stock",
                key="stock_id"
            ),
            BasePipeline.project(
                name="trade",
                show=["member", "stock"],
                custom={
                    "balance": BaseCalculate.sum(
                        BaseCalculate.sum("$property.init_amount"),
                        BaseCalculate.sum("$trade.final_money"),
                    ),
                    # 修正金額需跟原始金額合併成最終金額
                    "money": BaseCalculate.sum(
                        "$money",
                        "$details.money_correction",
                    ),
                    # 修正遊戲幣需跟原始遊戲幣合併成最終遊戲幣
                    "game_coin": BaseCalculate.sum(
                        "$game_coin",
                        "$details.game_coin_correction",
                    ),
                    "real_in": BaseCalculate.sum(
                        "$money",
                        "$charge_fee",
                        BaseCalculate.multiply("$stage_fee", -1),
                    ),
                }
            )
        ],
        page=request.query_params.get("page"),
        count=request.query_params.get("count"),
        sort={ "time_at": -1 }
    )

    return result_data


@router.set_route(method="patch", url="/trades/{id}")
async def update_trade(
    request: Request, form_data: TradeRequest.Update
) -> TradeResponse.Operate:
    update_data = await collection.update_data(
        find={
            "id": request.path_params.get("id")
        },
        data=form_data.model_dump()
    )

    return update_data


@router.set_route(method="patch", url="/trades/{id}/complete")
async def update_trade_complete(
    request: Request, form_data: TradeRequest.Complete
) -> TradeResponse.Operate:
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
