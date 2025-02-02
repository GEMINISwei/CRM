# =====================================================================================================================
#                   Import
# =====================================================================================================================
from fastapi import APIRouter, HTTPException, status, Request
from database import settings_collection
from schema import SettingUpdateRequest


# =====================================================================================================================
#                   Declare Variable
# =====================================================================================================================
router = APIRouter()


# =====================================================================================================================
#                   Setting Router
# =====================================================================================================================
@router.get("/settings", status_code = status.HTTP_200_OK)
async def get_settings(request_data: Request):
    try:
        collection_name = request_data.query_params.get('collection_name')
        setting = await settings_collection.find_one({ "collection_name": collection_name })
        if not setting:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Setting not found.")

        return {
            "data": setting['fields'],
            "message": "Setting get success."
        }
    except Exception as error:
        if hasattr(error, 'status_code'):
            raise HTTPException(status_code = error.status_code, detail = error.detail)
        else:
            raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Setting get error.")


@router.patch("/settings")
async def update_settings(request_data: SettingUpdateRequest):
    try:
        update_data = request_data.to_json()
        setting = await settings_collection.find_one({ "collection_name": update_data['collection_name'] })

        update_setting = {}
        update_setting["$" + update_data["update_type"]] = {}
        update_setting["$" + update_data["update_type"]]["fields." + update_data["field_name"]] = update_data["field_value"]
        await settings_collection.update_one({ "_id": setting['_id'] }, update_setting)

        return {
            "data": {},
            "message": "Setting update success."
        }
    except Exception as error:
        if hasattr(error, 'status_code'):
            raise HTTPException(status_code = error.status_code, detail = error.detail)
        else:
            raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Setting update error.")
