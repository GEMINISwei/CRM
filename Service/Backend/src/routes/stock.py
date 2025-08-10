# =====================================================================================================================
#                   Import
# =====================================================================================================================
from typing import List, Optional

from fastapi import Request
from pydantic import BaseModel, Field

from router import BaseRouter
from database import BaseCollection, BasePipeline, BaseCondition, BaseCalculate


# =====================================================================================================================
#                   Class
# =====================================================================================================================
class StockRequest:
    class Create(BaseModel):
        game_id: str = Field(...)
        role_name: str = Field(...)
        init_amount: Optional[int] = Field(default=0)


class StockResponse:
    class Operate(BaseModel):
        role_name: str = Field(...)

    class List(BaseModel):
        list_data: List[dict] = Field(...)
        page_count: int = Field(...)


# =====================================================================================================================
#                   Variable
# =====================================================================================================================
router = BaseRouter()
collection = BaseCollection(name="stock")


# =====================================================================================================================
#                   Stock Router
# =====================================================================================================================
@router.set_route(method="post", url="/stocks")
async def create_stock(
    request: Request, form_data: StockRequest.Create
) -> StockResponse.Operate:
    new_stock = await collection.create_data(
        data=form_data.model_dump()
    )

    return new_stock


@router.set_route(method="get", url="/stocks")
async def get_stock_list(
    request: Request
) -> StockResponse.List:
    result_data = await collection.get_list_data(
        pipelines=[
            BasePipeline.match(
                BaseCondition.equl("$game_id", request.query_params.get("game_id"))
            ),
            BasePipeline.lookup(
                name="trade",
                key="id",
                conditions=[
                    BaseCondition.equl("$is_cancel", False),
                    BaseCondition.equl("$stock_id", "$$id")
                ],
                pipelines=[
                    BasePipeline.project(
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
                    )
                ]
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
        page=request.query_params.get("page"),
        count=request.query_params.get("count")
    )

    return result_data
