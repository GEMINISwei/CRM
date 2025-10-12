# =====================================================================================================================
#                   Import
# =====================================================================================================================
from typing import List, Optional, Self
from datetime import datetime

from fastapi import Request
from pydantic import BaseModel, Field

from router import BaseRouter
from database import BaseCollection, BasePipeline, BaseCondition


# =====================================================================================================================
#                   Class
# =====================================================================================================================
class PlayerRequest:
    class Create(BaseModel):
        member_id: str = Field(...)
        name: str = Field(...)
        is_main: Optional[bool] = Field(default=False)

    class UpdateInfo(BaseModel):
        name: str = Field(...)
        # is_main: bool = Field(...)


class PlayerResponse:
    class Operate(BaseModel):
        name: str = Field(...)

    class Edit(BaseModel):
        name: str = Field(...)
        is_main: bool = Field(...)


# =====================================================================================================================
#                   Variable
# =====================================================================================================================
router = BaseRouter()
collection = BaseCollection(name="player")


# =====================================================================================================================
#                   Member Router
# =====================================================================================================================
@router.set_route(method="post", url="/players")
async def create_player(
    request: Request, form_data: PlayerRequest.Create
) -> PlayerResponse.Operate:
    new_member = await collection.create_data(
        data=form_data.model_dump()
    )

    return new_member


@router.set_route(method="get", url="/players/{id}")
async def get_player(
    request: Request
) -> PlayerResponse.Edit:
    show_data = await collection.get_data(
        pipelines=[
            BasePipeline.match(
                BaseCondition.equl("$id", request.path_params.get("id"))
            )
        ]
    )

    return show_data


@router.set_route(method="patch", url="/players/{id}")
async def update_player(
    request: Request, form_data: PlayerRequest.UpdateInfo
) -> PlayerResponse.Operate:
    update_data = await collection.update_data(
        find={
            "id": request.path_params.get("id")
        },
        data=form_data.model_dump()
    )

    return update_data


@router.set_route(method="delete", url="/players/{id}")
async def delete_player(
    request: Request
) -> PlayerResponse.Operate:
    # 不是主遊戲帳號, 才可刪除
    delete_data = await collection.delete_data(
        find={
            "id": request.path_params.get("id"),
            'is_main': False,
        }
    )

    return delete_data
