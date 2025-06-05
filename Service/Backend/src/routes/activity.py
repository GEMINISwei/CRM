# =====================================================================================================================
#                   Import
# =====================================================================================================================
from typing import List, Self
from datetime import datetime
from dateutil.relativedelta import relativedelta

from fastapi import Request
from pydantic import BaseModel, Field

from router import BaseRouter
from database import BaseCollection, BasePipeline, BaseCondition


# =====================================================================================================================
#                   Class
# =====================================================================================================================
class ActivityRequest:
    class Create(BaseModel):
        game_id: str = Field(...)
        name: str = Field(...)
        base_type: str = Field(...)
        start_time: datetime = Field(...)
        end_time: datetime = Field(...)
        money_floor: int = Field(...)
        coin_free: int = Field(...)

        def model_post_init(self: Self, _):
            self.end_time = self.end_time + relativedelta(days=1) - relativedelta(seconds=1)

    class Update(BaseModel):
        name: str = Field(...)
        start_time: datetime = Field(...)
        end_time: datetime = Field(...)
        money_floor: int = Field(...)
        coin_free: int = Field(...)

        def model_post_init(self: Self, _):
            self.end_time = self.end_time + relativedelta(days=1) - relativedelta(seconds=1)


class ActivityResponse:
    class Operate(BaseModel):
        name: str = Field(...)

    class Edit(BaseModel):
        game_id: str = Field(...)
        name: str = Field(...)
        base_type: str = Field(...)
        start_time: datetime = Field(...)
        end_time: datetime = Field(...)
        money_floor: int = Field(...)
        coin_free: int = Field(...)

    class List(BaseModel):
        list_data: List[dict] = Field(...)
        page_count: int = Field(...)


# =====================================================================================================================
#                   Variable
# =====================================================================================================================
router = BaseRouter()
collection = BaseCollection(name="activity")


# =====================================================================================================================
#                   Trade Router
# =====================================================================================================================
@router.set_route(method="post", url="/activities")
async def create_activity(
    request: Request, form_data: ActivityRequest.Create
) -> ActivityResponse.Operate:
    new_data = await collection.create_data(
        data=form_data.model_dump()
    )

    return new_data


@router.set_route(method="get", url="/activities/{id}")
async def get_activity(
    request: Request
) -> ActivityResponse.Edit:
    show_data = await collection.get_data(
        pipelines=[
            BasePipeline.match(
                BaseCondition.equl("$id", request.path_params.get("id"))
            )
        ]
    )

    return show_data


@router.set_route(method="get", url="/activities")
async def get_activity_list(
    request: Request
) -> ActivityResponse.List:
    result_data = await collection.get_list_data(
        pipelines=[
            BasePipeline.match(
                BaseCondition.and_expression(
                    BaseCondition.less_than("$start_time", datetime.now(), equl=True),
                    BaseCondition.greater_than("$end_time", datetime.now(), equl=True),
                    BaseCondition.regex("$game_id", request.query_params.get("game_id"))
                )
            ),
            BasePipeline.lookup(
                name="game",
                key="game_id"
            )
        ]
    )

    return result_data


@router.set_route(method="patch", url="/activities/{id}")
async def update_trade_check(
    request: Request, form_data: ActivityRequest.Update
) -> ActivityResponse.Operate:
    update_data = await collection.update_data(
        find={
            "id": request.path_params.get("id")
        },
        data=form_data.model_dump()
    )

    return update_data


@router.set_route(method="delete", url="/activities/{id}")
async def cancel_trade(
    request: Request
) -> ActivityResponse.Operate:
    delete_data = await collection.delete_data(
        find={
            "id": request.path_params.get("id")
        }
    )

    return delete_data
