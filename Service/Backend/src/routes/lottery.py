# =====================================================================================================================
#                   Import
# =====================================================================================================================
from typing import List, Self
from datetime import datetime
from dateutil.relativedelta import relativedelta
from os import environ

from fastapi import Request
from pydantic import BaseModel, Field

from router import BaseRouter
from database import BaseCollection, BasePipeline, BaseCondition


# =====================================================================================================================
#                   Class
# =====================================================================================================================
class LotteryRequest:
    class Create(BaseModel):
        trade_id: str = Field(...)
        target_award: str = Field(...)
        result_award: str = Field(default="--")

    class Update(BaseModel):
        result_award: str = Field(...)


class LotteryResponse:
    class Operate(BaseModel):
        id: str = Field(...)

    class Edit(BaseModel):
        target_award: str = Field(...)
        result_award: str = Field(...)
        block: object = Field(...)

    class List(BaseModel):
        list_data: List[dict] = Field(...)
        page_count: int = Field(...)


# =====================================================================================================================
#                   Variable
# =====================================================================================================================
router = BaseRouter()
collection = BaseCollection(name="lottery")
setting_collection = BaseCollection(name="setting")
ENV_API_URL = environ["API_URL"]


# =====================================================================================================================
#                   Trade Router
# =====================================================================================================================
@router.set_route(method="post", url="/lotteries")
async def create_lottery(
    request: Request, form_data: LotteryRequest.Create
) -> LotteryResponse.Operate:
    setting_data = await setting_collection.get_data(
        pipelines=[
            BasePipeline.match(
                BaseCondition.equl("$collection_name", "award")
            )
        ]
    )

    form_data = form_data.model_dump()
    form_data['block'] = setting_data['fields']['block']

    new_data = await collection.create_data(
        data=form_data
    )

    return new_data


@router.set_route(method="get", url="/lotteries/{id}", auth=False)
async def get_lottery(
    request: Request
) -> LotteryResponse.Edit:
    show_data = await collection.get_data(
        pipelines=[
            BasePipeline.match(
                BaseCondition.equl("$id", request.path_params.get("id"))
            )
        ]
    )

    return show_data


@router.set_route(method="patch", url="/lotteries/{id}", auth=False)
async def update_lottery(
    request: Request, form_data: LotteryRequest.Update
) -> LotteryResponse.Operate:
    update_data = await collection.update_data(
        find={
            "id": request.path_params.get("id")
        },
        data=form_data.model_dump()
    )

    return update_data
