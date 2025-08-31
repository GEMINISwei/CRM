# =====================================================================================================================
#                   Import
# =====================================================================================================================
from typing import List, Optional
from datetime import datetime
from dateutil.relativedelta import relativedelta

from fastapi import Request
from pydantic import BaseModel, Field

from router import BaseRouter
from database import BaseCollection, BasePipeline, BaseCondition, BaseCalculate


# =====================================================================================================================
#                   Class
# =====================================================================================================================
class PropertyRequest:
    class Create(BaseModel):
        name: str = Field(...)
        kind: str = Field(...)
        account: Optional[str] = Field(default=None)
        init_amount: Optional[int] = Field(default=0)

    class Update(BaseModel):
        name: str = Field(...)
        init_amount: int = Field(...)


class PropertyResponse:
    class Operate(BaseModel):
        name: str = Field(...)

    class Edit(BaseModel):
        name: str = Field(...)
        init_amount: int = Field(...)

    class List(BaseModel):
        list_data: List[dict] = Field(...)
        page_count: int = Field(...)


# =====================================================================================================================
#                   Variable
# =====================================================================================================================
router = BaseRouter()
collection = BaseCollection(name="property")
trade_collection = BaseCollection(name="trade")


# =====================================================================================================================
#                   Property Router
# =====================================================================================================================
@router.set_route(method="post", url="/properties")
async def create_property(
    request: Request, form_data: PropertyRequest.Create
) -> PropertyResponse.Operate:
    new_property = await collection.create_data(
        data=form_data.model_dump()
    )

    return new_property


@router.set_route(method="get", url="/properties/{id}")
async def get_property(
    request: Request
) -> PropertyResponse.Edit:
    show_data = await collection.get_data(
        pipelines=[
            BasePipeline.match(
                BaseCondition.equl("$id", request.path_params.get("id"))
            )
        ]
    )

    return show_data


@router.set_route(method="get", url="/properties")
async def get_property_list(
    request: Request
) -> PropertyResponse.List:
    current_time = datetime.now()
    day_start = datetime(current_time.year, current_time.month, current_time.day)
    day_end = day_start + relativedelta(days=1) - relativedelta(seconds=1)

    month_start = datetime(current_time.year, current_time.month, 1)
    month_end = month_start + relativedelta(months=1) - relativedelta(seconds=1)

    result_data = await collection.get_list_data(
        pipelines=[
            BasePipeline.lookup(
                name="trade",
                key="id",
                conditions=[
                    BaseCondition.equl("$is_cancel", False),
                    BaseCondition.equl("$property_id", "$$id"),
                    BaseCondition.not_equl("$completed_by", None),
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
                            ),
                            "in_day": BaseCondition.and_expression(
                                BaseCondition.greater_than("$time_at", day_start, equl=True),
                                BaseCondition.less_than("$time_at", day_end, equl=True)
                            ),
                            "in_month": BaseCondition.and_expression(
                                BaseCondition.greater_than("$time_at", month_start, equl=True),
                                BaseCondition.less_than("$time_at", month_end, equl=True)
                            )
                        }
                    )
                ]
            ),
            BasePipeline.project(
                name="property",
                custom={
                    "today_balance": BaseCalculate.sum(
                        BasePipeline.map(
                            input="$trade",
                            output=BaseCondition.if_then_else(
                                BaseCondition.equl("$$this.in_day", True),
                                "$$this.final_money",
                                0
                            )
                        )
                    ),
                    "balance": BaseCalculate.sum(
                        "$init_amount",
                        BaseCalculate.sum("$trade.final_money")
                    ),
                    "day_count": BaseCalculate.size(
                        BasePipeline.filter("$trade.in_day", True)
                    ),
                    "month_count": BaseCalculate.size(
                        BasePipeline.filter("$trade.in_month", True)
                    ),
                    "total_count": BaseCalculate.size("$trade")
                }
            )
        ],
        page=request.query_params.get("page"),
        count=request.query_params.get("count")
    )

    return result_data


@router.set_route(method="get", url="/properties/supermarket_daily")
async def get_supermarket_daily(
    request: Request
) -> PropertyResponse.List:
    result_data = await trade_collection.get_list_data(
        pipelines=[
            BasePipeline.match(
                BaseCondition.equl("$is_cancel", False),
            ),
            BasePipeline.match(
                BaseCondition.equl("$property_id", request.query_params.get("property_id"))
            ),
            BasePipeline.project(
                show=["time_at"],
                custom={
                    "real_in": BaseCalculate.sum(
                        "$money",
                        "$charge_fee",
                        BaseCalculate.multiply("$stage_fee", -1),
                    ),
                }
            ),
            {
                "$group": {
                    "_id": {
                        "$dateToString": { "format": "%Y-%m-%d", "date": "$time_at" }
                    },
                    "daily_amount": { "$sum": "$real_in" },
                    "count": { "$sum": 1 }
                }
            },
            {
                "$sort": { "_id": 1 }
            }
        ]
    )

    return result_data


@router.set_route(method="get", url="/properties/v_account_daily")
async def get_v_account_daily(
    request: Request
) -> PropertyResponse.List:
    result_data = await trade_collection.get_list_data(
        pipelines=[
            BasePipeline.match(
                BaseCondition.equl("$is_cancel", False),
            ),
            BasePipeline.match(
                BaseCondition.equl("$property_id", request.query_params.get("property_id"))
            ),
            BasePipeline.project(
                show=["time_at"],
                custom={
                    "real_in": BaseCalculate.sum(
                        "$money",
                        "$charge_fee",
                        BaseCalculate.multiply("$stage_fee", -1),
                    ),
                }
            ),
            {
                "$group": {
                    "_id": {
                        "$dateToString": { "format": "%Y-%m-%d", "date": "$time_at" }
                    },
                    "daily_amount": { "$sum": "$real_in" },
                    "count": { "$sum": 1 }
                }
            },
            {
                "$sort": { "_id": 1 }
            }
        ]
    )

    return result_data


@router.set_route(method="patch", url="/properties/{id}")
async def update_property(
    request: Request, form_data: PropertyRequest.Update
) -> PropertyResponse.Operate:
    update_data = await collection.update_data(
        find={
            "id": request.path_params.get("id")
        },
        data=form_data.model_dump()
    )

    return update_data
