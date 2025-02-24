# =================================================================================================
#                   Import
# =================================================================================================
from typing import List, Optional, Self
from bson.objectid import ObjectId
from datetime import datetime

from fastapi import Request
from pydantic import BaseModel, Field

from router import BaseRouter
from database import BaseCollection, BasePipeline


# =================================================================================================
#                   Class
# =================================================================================================
class MemberRequest:
    class Create(BaseModel):
        game_id: str = Field(...)
        nickname: str = Field(...)
        sex: Optional[str] = Field(default=None)
        first_communication_time: Optional[datetime] = Field(default=None)
        first_communication_way: Optional[str] = Field(default=None)
        first_communication_amount: Optional[int] = Field(default=None)
        description: Optional[str] = Field(default=None)
        accounts: Optional[List[str]] = Field(default=[])
        sock_puppets: Optional[List[str]] = Field(default=[])
        phones: Optional[List[str]] = Field(default=[])

    class UpdateInfo(BaseModel):
        sex: Optional[str] = Field(default = None)
        first_communication_time: Optional[datetime] = Field(default=None)
        first_communication_way: Optional[str] = Field(default=None)
        first_communication_amount: Optional[int] = Field(default=None)
        description: Optional[str] = Field(default = None)

    class UpdateAccounts(BaseModel):
        accounts: Optional[List[str]] = Field(default = [])

    class UpdateSockPuppets(BaseModel):
        sock_puppets: Optional[List[str]] = Field(default = [])

    class UpdatePhones(BaseModel):
        phones: Optional[List[str]] = Field(default = [])


class MemberResponse:
    class Operate(BaseModel):
        nickname: str = Field(...)

    class Edit(BaseModel):
        nickname: str = Field(...)
        sex: Optional[str] = Field(default=None)
        first_communication_time: Optional[datetime] = Field(default=None)
        first_communication_way: Optional[str] = Field(default=None)
        first_communication_amount: Optional[int] = Field(default=None)
        description: Optional[str] = Field(default=None)
        accounts: Optional[List[str]] = Field(default=[])
        sock_puppets: Optional[List[str]] = Field(default=[])
        phones: Optional[List[str]] = Field(default=[])

    class List(BaseModel):
        list_data: List[dict] = Field(...)
        page_count: int = Field(...)


# =================================================================================================
#                   Variable
# =================================================================================================
router = BaseRouter()
collection = BaseCollection(name="member")


# =================================================================================================
#                   Member Router
# =================================================================================================
@router.set_route(method="post", url="/members")
async def create_member(
    request: Request, form_data: MemberRequest.Create
) -> MemberResponse.Operate:
    new_member = await collection.create_data(
        data=form_data.model_dump()
    )

    return new_member


@router.set_route(method="get", url="/members/{id}")
async def get_member(
    request: Request
) -> MemberResponse.Edit:
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


@router.set_route(method="get", url="/members")
async def get_member_list(
    request: Request
) -> MemberResponse.List:
    result_data = await collection.get_list_data(
        pipelines=[
            # BasePipeline.create_lookup(name="games", key="game_id"),
            BasePipeline.create_match(
                equl={
                    "game_id": request.query_params.get("game_id"),
                },
                fuzzy={
                    "nickname": request.query_params.get("nickname"),
                    "accounts": request.query_params.get("accounts"),
                    "sock_puppets": request.query_params.get("sock_puppets"),
                    "phones": request.query_params.get("phones"),
                }
            ),
        ],
        page=request.query_params.get("page"),
        count=request.query_params.get("count")
    )

    return result_data


@router.set_route(method="patch", url="/members/{id}")
async def update_member(
    request: Request, form_data: MemberRequest.UpdateInfo
) -> MemberResponse.Operate:
    update_data = await collection.update_data(
        find={
            "id": request.path_params.get("id")
        },
        data=form_data.model_dump()
    )

    return update_data


@router.set_route(method="patch", url="/members/{id}/accounts")
async def update_member_accounts(
    request: Request, form_data: MemberRequest.UpdateAccounts
) -> MemberResponse.Operate:
    update_data = await collection.update_data(
        find={
            "id": request.path_params.get("id")
        },
        data=form_data.model_dump()
    )

    return update_data


@router.set_route(method="patch", url="/members/{id}/sock_puppets")
async def update_member_sock_puppets(
    request: Request, form_data: MemberRequest.UpdateSockPuppets
) -> MemberResponse.Operate:
    update_data = await collection.update_data(
        find={
            "id": request.path_params.get("id")
        },
        data=form_data.model_dump()
    )

    return update_data


@router.set_route(method="patch", url="/members/{id}/phones")
async def update_member_phones(
    request: Request, form_data: MemberRequest.UpdatePhones
) -> MemberResponse.Operate:
    update_data = await collection.update_data(
        find={
            "id": request.path_params.get("id")
        },
        data=form_data.model_dump()
    )

    return update_data


@router.set_route(method="delete", url="/members/{id}")
async def delete_member(
    request: Request
) -> MemberResponse.Operate:
    delete_data = await collection.delete_data(
        find={
            "id": request.path_params.get("id")
        }
    )

    return delete_data
