# =====================================================================================================================
#                   Import
# =====================================================================================================================
from typing import List, Optional

from fastapi import Request
from pydantic import BaseModel, Field

from router import BaseRouter
from database import BaseCollection, BasePipeline


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
            BasePipeline.create_match(
                equl={
                    "game_id": request.query_params.get("game_id")
                }
            ),
            BasePipeline.create_lookup(
                name="trade",
                key="id",
                match_conditions=[
                    BasePipeline.create_eq_condition("$is_cancel", False),
                    BasePipeline.create_eq_condition("$stock_id", "$$id")
                ],
                pipelines=[
                    BasePipeline.create_project(
                        custom={
                            "final_coin": BasePipeline.create_sum(
                                items=[
                                    BasePipeline.create_if_condition(
                                        if_expn=BasePipeline.create_eq_condition("$base_type", "money_in"),
                                        then_expn=BasePipeline.create_multiply(
                                            items=["$game_coin", -1]
                                        ),
                                        else_expn="$game_coin"
                                    ),
                                    BasePipeline.create_multiply(
                                        items=["$game_coin_fee", -1]
                                    ),
                                    BasePipeline.create_multiply(
                                        items=["$details.game_coin_correction", -1]
                                    )
                                ]
                            )
                        }
                    )
                ]
            ),
            BasePipeline.create_project(
                name="stock",
                custom={
                    "balance": BasePipeline.create_sum(
                        items=[
                            "$init_amount",
                            BasePipeline.create_sum(
                                items="$trade.final_coin"
                            )
                        ]
                    )
                }
            ),

        ],
        page=request.query_params.get("page"),
        count=request.query_params.get("count")
    )

    return result_data
