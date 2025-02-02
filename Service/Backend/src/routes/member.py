# =====================================================================================================================
#                   Import
# =====================================================================================================================
import re
from fastapi import APIRouter, HTTPException, status, Request
from database import CustomCollection, QueryPipeline, LookupPipeline, members_collection
from schema import MemberSchema, MemberCreateRequest, MemberUpdateRequest
from bson.objectid import ObjectId
from datetime import datetime
from log import CustomLog


# =====================================================================================================================
#                   Declare Variable
# =====================================================================================================================
router = APIRouter()
log = CustomLog("member")


# =====================================================================================================================
#                   Member Router
# =====================================================================================================================
@router.post("/members")
async def create_member(request_data: MemberCreateRequest):
    try:
        new_data = request_data.to_json()

        f_communication_time = new_data["f_communication_time"]
        if f_communication_time != None:
            print(f_communication_time)
            f_communication_time = datetime.strptime(f_communication_time, "%Y-%m-%dT%H:%M:%S")

        new_data["f_communication_time"] = f_communication_time

        new_member = MemberSchema(**new_data).to_json()
        await members_collection.insert_one(new_member)

        return {
            "data": {
                "nickname": new_member["nickname"]
            },
            "message": "Member create success."
        }

    except Exception as error:
        print(error)
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Member create failure.")


@router.get("/members")
async def get_member_list(request_data: Request):
    try:
        collection = CustomCollection(name="members")

        query = QueryPipeline(
            data=request_data.query_params,
            equl=["game_id"],
            regex=["nickname", "accounts", "sock_puppets", "phones"]
        )

        lookup = LookupPipeline(
            name="games",
            key="game_id"
        )

        result_json = await collection.get_list_data(
            pipelines=[
                query.pipeline,
                lookup.pipeline
            ],
            page=request_data.query_params.get("page"),
            count=request_data.query_params.get("count")
        )

        return {
            "data": result_json["data"],
            "info": result_json["info"],
            "message": "Member list get success."
        }

    except Exception as error:
        print(error)
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Member list Get failure.")


@router.get("/members/{id}")
async def get_member(id: str):
    try:
        collection = CustomCollection(name="members")

        query = QueryPipeline(
            data={
                "id": id
            },
            equl=["id"],
        )

        result_json = await collection.get_list_data(
            pipelines=[
                query.pipeline
            ]
        )

        if len(result_json["data"]) == 0:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Member not found.")

        return {
            "data": result_json["data"][0],
            "message": "Member get success."
        }

    except Exception as error:
        print(error)
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Member Get failure.")


@router.patch("/members/{id}")
async def update_member(id: str, request_data: MemberUpdateRequest):
    try:
        update_data = request_data.to_json()
        f_communication_time = update_data["f_communication_time"]
        if f_communication_time != None:
            f_communication_time = datetime.strptime(f_communication_time, "%Y-%m-%dT%H:%M:%S")

        update_data["f_communication_time"] = f_communication_time

        update_result = await members_collection.update_one({ "_id": ObjectId(id)}, { "$set": update_data })
        if update_result.matched_count == 0:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Member not found.")
        elif update_result.modified_count <= 0:
            raise HTTPException(status_code = status.HTTP_405_METHOD_NOT_ALLOWED, detail = "內容無變更, 請確認更新資訊 !")

        matched_data = await members_collection.find_one({"_id": ObjectId(id)})

        return {
            "data": {
                "nickname": matched_data['nickname']
            },
            "message": f"會員 {matched_data['nickname']} 資料更新成功 !"
        }

    except Exception as error:
        print(error)
        if hasattr(error, 'status_code'):
            raise HTTPException(status_code = error.status_code, detail = error.detail)
        else:
            raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "伺服器發生錯誤 !")


@router.patch("/members/{id}/accounts")
async def update_member_accounts(id: str, request_data: MemberUpdateRequest):
    try:
        update_data = request_data.to_json()
        need_update_data = {
            "accounts": update_data["accounts"]
        }
        update_result = await members_collection.update_one({ "_id": ObjectId(id)}, { "$set": need_update_data })
        if update_result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found.")
        if update_result.modified_count <= 0:
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="內容無變更, 請確認更新資訊 !")

        matched_data = await members_collection.find_one({"_id": ObjectId(id)})

        return {
            "data": {
                "nickname": matched_data["nickname"]
            },
            "message": f"會員 {matched_data['nickname']} 資料更新成功 !"
        }

    except Exception as error:
        print(error)
        if hasattr(error, 'status_code'):
            raise HTTPException(status_code = error.status_code, detail = error.detail)
        else:
            raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "伺服器發生錯誤 !")


@router.patch("/members/{id}/sock_puppets")
async def update_member_sock_puppets(id: str, request_data: MemberUpdateRequest):
    try:
        update_data = request_data.to_json()
        need_update_data = {
            "sock_puppets": update_data["sock_puppets"]
        }
        update_result = await members_collection.update_one({ "_id": ObjectId(id)}, { "$set": need_update_data })
        if update_result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found.")
        if update_result.modified_count <= 0:
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="內容無變更, 請確認更新資訊 !")

        matched_data = await members_collection.find_one({"_id": ObjectId(id)})

        return {
            "data": {
                "nickname": matched_data['nickname']
            },
            "message": f"會員 {matched_data['nickname']} 資料更新成功 !"
        }

    except Exception as error:
        print(error)
        if hasattr(error, 'status_code'):
            raise HTTPException(status_code=error.status_code, detail=error.detail)
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="伺服器發生錯誤 !")


@router.patch("/members/{id}/phones")
async def update_member_phones(id: str, request_data: MemberUpdateRequest):
    try:
        update_data = request_data.to_json()
        need_update_data = {
            "phones": update_data["phones"]
        }
        update_result = await members_collection.update_one({ "_id": ObjectId(id)}, { "$set": need_update_data })
        if update_result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found.")
        if update_result.modified_count <= 0:
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="內容無變更, 請確認更新資訊 !")

        matched_data = await members_collection.find_one({"_id": ObjectId(id)})

        return {
            "data": {
                "nickname": matched_data['nickname']
            },
            "message": f"會員 {matched_data['nickname']} 資料更新成功 !"
        }

    except Exception as error:
        print(error)
        if hasattr(error, 'status_code'):
            raise HTTPException(status_code = error.status_code, detail = error.detail)
        else:
            raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "伺服器發生錯誤 !")


@router.delete("/members/{id}")
async def delete_member(id: str):
    member_data = await members_collection.find_one({"_id": ObjectId(id)})

    if not member_data:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User not found.")

    await members_collection.delete_one({"_id": ObjectId(id)})

    return {
        "data": {
            "nickname": member_data['nickname']
        },
        "message": "User delete success."
    }
