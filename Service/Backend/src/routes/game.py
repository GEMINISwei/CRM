# =====================================================================================================================
#                   Import
# =====================================================================================================================
from fastapi import APIRouter, HTTPException, status, Request
from database import CustomCollection, DBError, QueryPipeline
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from log import CustomLog
from routes.user import token_required
import http_error

# =====================================================================================================================
#                   Game Schema
# =====================================================================================================================
class GameSchema:
    name: str
    money_in_exchange: float
    money_out_exchange: float
    charge_fee: int
    game_coin_fee: float
    created_time: datetime = Field(default_factory=lambda: datetime.now())


# =====================================================================================================================
#                   API Request
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
#                   API Response
# =====================================================================================================================
class GameCreateResponse(BaseModel):
    name: str = Field(...)


class GameEditResponse(BaseModel):
    name: str = Field(...)
    money_in_exchange: float = Field(...)
    money_out_exchange: float = Field(...)
    charge_fee: int = Field(...)
    game_coin_fee: float = Field(...)


class GameUpdateResponse(BaseModel):
    name: str = Field(...)


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
@token_required
async def create_game(
    request: Request,
    form_data: GameCreateRequest
) -> GameCreateResponse:
    try:
        new_data = form_data.model_dump()
        new_game, db_error = await collection.create(data=new_data)
        if db_error != DBError.NONE:
            raise Exception(db_error)

        return new_game

    except Exception as error:
        print(error)

        match error.args[0]:
            case DBError.CREATE_DUPLICATE:
                raise http_error.Error_409_CONFLICT()

        raise http_error.Error_500_Internal_Server_Error()


@router.get("/games/{id}")
@token_required
async def get_game(
    request: Request,
    id: str
) -> GameEditResponse:
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

        edit_data = result_json["data"][0]

        return edit_data

    except Exception as error:
        print(error)
        raise http_error.Error_500_Internal_Server_Error()


@router.patch("/games/{id}")
@token_required
async def update_game(
    request: Request,
    id: str,
    form_data: GameUpdateRequest
) -> GameUpdateResponse:
    try:
        updated_data, db_error = await collection.update(id=id, methd="set", data=form_data.model_dump())
        if db_error != DBError.NONE:
            raise Exception(db_error)

        return updated_data

    except Exception as error:
        print(error)

        match error.args[0]:
            case DBError.UPDATE_NOT_FOUND:
                raise http_error.Error_404_NOT_FOUND()
            case DBError.UPDATE_NOTHING:
                raise http_error.Error_405_METHOD_NOT_ALLOWED()

        raise http_error.Error_500_Internal_Server_Error()


@router.get("/games")
@token_required
async def get_game_list(request: Request):
    try:
        result_json = await collection.get_list_data(
            page=request.query_params.get("page"),
            count=request.query_params.get("count")
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
