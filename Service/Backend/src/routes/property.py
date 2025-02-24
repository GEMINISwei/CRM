# =================================================================================================
#                   Import
# =================================================================================================
from typing import List, Optional
from datetime import datetime
from dateutil.relativedelta import relativedelta

from fastapi import Request
from pydantic import BaseModel, Field

from router import BaseRouter
from database import BaseCollection, BasePipeline



# =================================================================================================
#                   Class
# =================================================================================================
class PropertyRequest:
    class Create(BaseModel):
        name: str = Field(...)
        kind: str = Field(...)
        account: Optional[str] = Field(default=None)
        init_amount: Optional[int] = Field(default=0)


class PropertyResponse:
    class Operate(BaseModel):
        name: str = Field(...)

    class List(BaseModel):
        list_data: List[dict] = Field(...)
        page_count: int = Field(...)


# =================================================================================================
#                   Variable
# =================================================================================================
router = BaseRouter()
collection = BaseCollection(name="property")


# =================================================================================================
#                   Property Router
# =================================================================================================
@router.set_route(method="post", url="/properties")
async def create_property(
    request: Request, form_data: PropertyRequest.Create
) -> PropertyResponse.Operate:
    new_property = await collection.create_data(
        data=form_data.model_dump()
    )

    return new_property


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
            BasePipeline.create_lookup(
                name="trade",
                key="id",
                match_conditions=[
                    BasePipeline.create_eq_condition("$is_cancel", False),
                    BasePipeline.create_eq_condition("$property_id", "$$id")
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
                                        items=["$money_correction", -1]
                                    )
                                ]
                            ),
                            "in_day": BasePipeline.create_and_condition(
                                items=[
                                    BasePipeline.create_gte_condition("$time_at", day_start),
                                    BasePipeline.create_lte_condition("$time_at", day_end)
                                ]
                            ),
                            "in_month": BasePipeline.create_and_condition(
                                items=[
                                    BasePipeline.create_gte_condition("$time_at", month_start),
                                    BasePipeline.create_lte_condition("$time_at", month_end)
                                ]
                            )
                        }
                    )
                ]
            ),
            BasePipeline.create_project(
                name="property",
                custom={
                    "today_balance": BasePipeline.create_sum(
                        items=[
                            BasePipeline.create_map(
                                input="$trade",
                                docs="trade",
                                expn=BasePipeline.create_if_condition(
                                    if_expn=BasePipeline.create_eq_condition("$$trade.in_day", True),
                                    then_expn="$$trade.final_money",
                                    else_expn=0
                                )
                            )
                        ]
                    ),
                    "balance": BasePipeline.create_sum(
                        items=[
                            "$init_amount",
                            BasePipeline.create_sum(
                                items=[
                                    "$trade.final_money"
                                ]
                            )
                        ]
                    ),
                    "day_count": BasePipeline.create_size(
                        item=BasePipeline.create_filter(
                            input="$trade.in_day",
                            value=True
                        )
                    ),
                    "month_count": BasePipeline.create_size(
                        item=BasePipeline.create_filter(
                            input="$trade.in_month",
                            value=True
                        )
                    ),
                    "total_count": BasePipeline.create_size(
                        item="$trade"
                    )
                }
            )
        ],
        page=request.query_params.get("page"),
        count=request.query_params.get("count")
    )

    return result_data
