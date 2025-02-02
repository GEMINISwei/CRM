# =====================================================================================================================
#                   Import
# =====================================================================================================================
from fastapi import APIRouter, HTTPException, status, Request
from database import CustomCollection, DBError, QueryPipeline, games_collection
from schema import GameSchema
from pydantic import BaseModel, Field
from bson.objectid import ObjectId
from typing import Optional
from log import CustomLog


# =====================================================================================================================
#                   Class
# =====================================================================================================================
class GameCreateRequest(BaseModel):
    name: str = Field(...)
    money_in_exchange: float = Field(...)
    money_out_exchange: float = Field(...)
    charge_fee: Optional[int] = Field(default=0)
    game_coin_fee: Optional[float] = Field(default=0.0)


class GameUpdateRequest(BaseModel):
    money_in_exchange: float = Field(...)
    money_out_exchange: float = Field(...)
    charge_fee: Optional[int] = Field(default=0)
    game_coin_fee: Optional[float] = Field(default=0.0)


# =====================================================================================================================
#                   Declare Variable
# =====================================================================================================================
router = APIRouter()
log = CustomLog("game")
collection = CustomCollection(name="games")


# =====================================================================================================================
#                   Game Router
# =====================================================================================================================
@router.post("/games")
async def create_game(request_data: GameCreateRequest):
    try:
        new_data = GameSchema(**request_data.model_dump())
        new_game, db_error = await collection.create(data=new_data)
        if db_error != DBError.NONE:
            raise Exception(db_error)

        return {
            "data": {
                "name": new_game["name"]
            },
            "message": "Game create success."
        }

    except Exception as error:
        match error.args[0]:
            case DBError.CREATE_DUPLICATE:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT)
            case _:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.patch("/games/{id}")
async def update_game(id: str, request_data: GameUpdateRequest):
    try:
        updated_data, db_error = await collection.update(id=id, methd="set", data=request_data.model_dump())
        if db_error != DBError.NONE:
            raise Exception(db_error)

        return {
            "data": {
                "name": updated_data['name']
            },
            "message": "Game update success."
        }

    except Exception as error:
        match error.args[0]:
            case DBError.UPDATE_NOT_FOUND:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
            case DBError.UPDATE_NOTHING:
                raise HTTPException(status_code = status.HTTP_405_METHOD_NOT_ALLOWED)
            case _:
                raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/games")
async def get_game_list(request_data: Request):
    try:
        result_json = await collection.get_list_data(
            page=request_data.query_params.get("page"),
            count=request_data.query_params.get("count")
        )

        return {
            "data": result_json["data"],
            "info": result_json["info"],
            "message": "Game list get success."
        }

    except Exception as error:
        print(error)
        if hasattr(error, 'status_code'):
            raise HTTPException(status_code=error.status_code, detail=error.detail)
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Game list get error.")


@router.get("/games/{id}")
async def get_game(id: str):
    try:
        query = QueryPipeline(
            data={
                "id": id
            },
            equl=["id"]
        )

        result_json = await collection.get_list_data(
            pipelines=[
                query.pipeline
            ]
        )

        return {
            "data": result_json["data"],
            "info": result_json["info"],
            "message": "Game get success."
        }

    except Exception as error:
        print(error)
        if hasattr(error, 'status_code'):
            raise HTTPException(status_code=error.status_code, detail=error.detail)
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Game list get error.")
