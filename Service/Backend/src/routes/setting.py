# =====================================================================================================================
#                   Import
# =====================================================================================================================
from fastapi import Request
from pydantic import BaseModel, Field
from typing import List, Any

from router import BaseRouter
from database import BaseCollection, BasePipeline, BaseCondition
from error import HttpError


# =====================================================================================================================
#                   Class
# =====================================================================================================================
class SettingRequest:
    class updateSettingInfo(BaseModel):
        collection_name: str = Field(...)
        field: str = Field(...)
        value: Any = Field(...)


class SettingResponse:
    class InfoData(BaseModel):
        collection_name: str = Field(...)
        field: str = Field(...)
        value: Any = Field(...)

    class Operate(BaseModel):
        collection_name: str = Field(...)


# =====================================================================================================================
#                   Variable
# =====================================================================================================================
router = BaseRouter()
collection = BaseCollection(name="setting")


# =====================================================================================================================
#                   Setting Router
# =====================================================================================================================
@router.set_route(method="get", url="/settings/{collection_name}/{field}")
async def get_settings_info(
    request: Request
) -> SettingResponse.InfoData:
    show_data = await collection.get_data(
        pipelines=[
            BasePipeline.match(
                BaseCondition.equl("$collection_name", request.path_params.get("collection_name"))
            )
        ]
    )
    if show_data is None:
        raise HttpError.Error_404_NOT_FOUND()

    if request.path_params.get("field") == 'all':
        result_value = show_data["fields"]
    else:
        result_value = show_data["fields"][request.path_params.get("field")]

    return {
        "collection_name": request.path_params.get("collection_name"),
        "field": request.path_params.get("field"),
        "value": result_value
    }


@router.set_route(method="patch", url="/set_settings")
async def set_setting_info(
    request: Request, form_data: SettingRequest.updateSettingInfo
) -> SettingResponse.Operate:
    edit_data = form_data.model_dump()
    update_data = await collection.update_data(
        find={
            "collection_name": edit_data["collection_name"]
        },
        method="set",
        data={
            f"fields.{edit_data["field"]}": edit_data["value"]
        }
    )

    return update_data


@router.set_route(method="patch", url="/add_settings")
async def add_setting_info(
    request: Request, form_data: SettingRequest.updateSettingInfo
) -> SettingResponse.Operate:
    edit_data = form_data.model_dump()
    update_data = await collection.update_data(
        find={
            "collection_name": edit_data["collection_name"]
        },
        method="push",
        data={
            f"fields.{edit_data["field"]}": edit_data["value"]
        }
    )

    return update_data

@router.set_route(method="delete", url="/delete_settings")
async def delete_setting_info(
    request: Request, form_data: SettingRequest.updateSettingInfo
) -> SettingResponse.Operate:
    delete_data = form_data.model_dump()
    update_data = await collection.update_data(
        find={
            "collection_name": delete_data["collection_name"]
        },
        method="pull",
        data={
            f"fields.{delete_data["field"]}": delete_data["value"]
        }
    )

    return update_data
