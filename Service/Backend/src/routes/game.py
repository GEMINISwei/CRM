# =====================================================================================================================
#                   Import
# =====================================================================================================================
from typing import List, Optional

from fastapi import Request
from pydantic import BaseModel, Field

from router import BaseRouter
from database import BaseCollection, BasePipeline, BaseCondition


# =====================================================================================================================
#                   Class
# =====================================================================================================================
class GameRequest:
    class Create(BaseModel):
        name: str = Field(...)
        money_in_exchange: float = Field(...)
        money_out_exchange: float = Field(...)
        # filter_setting: str = Field(...)
        charge_fee: Optional[int] = Field(default=0)
        game_coin_fee: Optional[float] = Field(default=0.0)
        market_free_fee: Optional[int] = Field(default=0)

    class Update(BaseModel):
        money_in_exchange: float = Field(...)
        money_out_exchange: float = Field(...)
        # filter_setting: str = Field(...)
        charge_fee: Optional[int] = Field(default=0)
        game_coin_fee: Optional[float] = Field(default=0.0)
        market_free_fee: Optional[int] = Field(default=0)


class GameResponse:
    class Operate(BaseModel):
        name: str = Field(...)

    class Edit(BaseModel):
        name: str = Field(...)
        money_in_exchange: float = Field(...)
        money_out_exchange: float = Field(...)
        charge_fee: int = Field(...)
        game_coin_fee: float = Field(...)
        market_free_fee: int = Field(...)


    class List(BaseModel):
        list_data: List[dict] = Field(...)
        page_count: int = Field(...)


# =====================================================================================================================
#                   Variable
# =====================================================================================================================
router = BaseRouter()
collection = BaseCollection(name="game")


# =====================================================================================================================
#                   Game Router
# =====================================================================================================================
@router.set_route(method="post", url="/games")
async def create_game(
    request: Request, form_data: GameRequest.Create
) -> GameResponse.Operate:
    new_game = await collection.create_data(
        data=form_data.model_dump()
    )

    return new_game


@router.set_route(method="get", url="/games/{id}")
async def get_game(
    request: Request
) -> GameResponse.Edit:
    show_data = await collection.get_data(
        pipelines=[
            BasePipeline.match(
                BaseCondition.equl("$id", request.path_params.get("id"))
            )
        ]
    )

    return show_data


@router.set_route(method="get", url="/games")
async def get_game_list(
    request: Request
) -> GameResponse.List:
    result_data = await collection.get_list_data(
        page=request.query_params.get("page"),
        count=request.query_params.get("count")
    )

    return result_data


@router.set_route(method="patch", url="/games/{id}")
async def update_game(
    request: Request, form_data: GameRequest.Update
) -> GameResponse.Operate:
    update_data = await collection.update_data(
        find={
            "id": request.path_params.get("id")
        },
        data=form_data.model_dump()
    )

    return update_data
