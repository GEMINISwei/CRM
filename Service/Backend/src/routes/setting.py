# =================================================================================================
#                   Import
# =================================================================================================
from fastapi import Request
from pydantic import BaseModel, Field
from typing import List

from router import BaseRouter
from database import BaseCollection, BasePipeline
from error import HttpError


# =================================================================================================
#                   Class
# =================================================================================================
class SettingRequest:
    class AddMemberCommunicationWay(BaseModel):
        communication_way: str


class SettingResponse:
    class MemberCommunicationWays(BaseModel):
        communication_ways: List[str] = Field(default_factory=list)

    class Operate(BaseModel):
        collection_name: str = Field(...)


# =================================================================================================
#                   Variable
# =================================================================================================
router = BaseRouter()
collection = BaseCollection(name="setting")


# =================================================================================================
#                   Setting Router
# =================================================================================================
@router.set_route(method="get", url="/settings/{collection_name}/{field}")
async def get_settings_info(
    request: Request
) -> SettingResponse.MemberCommunicationWays:
    show_data = await collection.get_data(
        pipelines=[
            BasePipeline.create_match(
                equl={
                    "collection_name": request.path_params.get("collection_name")
                }
            )
        ]
    )
    if show_data is None:
        raise HttpError.Error_404_NOT_FOUND()

    fields_info: dict = show_data["fields"]
    result_data = {
        key: value for key, value in fields_info.items() if key == request.path_params.get("field")
    }

    return result_data


@router.set_route(method="patch", url="/settings/member/communication_ways")
async def add_member_communication_ways(
    request: Request, form_data: SettingRequest.AddMemberCommunicationWay
) -> SettingResponse.Operate:
    edit_data = form_data.model_dump()
    update_data = await collection.update_data(
        find={
            "collection_name": "member"
        },
        method="push",
        data={
            "fields.communication_ways": edit_data["communication_way"]
        }
    )

    return update_data
