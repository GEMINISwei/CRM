# =====================================================================================================================
#                   Import
# =====================================================================================================================
from fastapi import APIRouter, HTTPException, status, Request
from database import stocks_collection
from schema import StockSchema, StockCreateSchema


# =====================================================================================================================
#                   Stock Router
# =====================================================================================================================
router = APIRouter()


@router.post("/stocks")
async def create_stock(request_data: StockCreateSchema):
    try:
        new_data = request_data.to_json()

        new_stock = StockSchema(**new_data).to_json()
        await stocks_collection.insert_one(new_stock)

        return {
            "data": {
                "role_name": new_stock["role_name"]
            },
            "message": "Stock create success."
        }
    except Exception as error:
        print(error)
        if hasattr(error, 'status_code'):
            raise HTTPException(status_code = error.status_code, detail = error.detail)
        else:
            raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Stock create error.")


@router.get("/stocks")
async def get_stock_list(request_data: Request):
    try:
        stocks_data = await stocks_collection.aggregate([
            {
                "$match": {
                    "game_id": {
                        "$eq": request_data.query_params.get('game_id')
                    }
                }
            },
            {
                "$lookup": {
                    "from": "trades",
                    "foreignField": "stock_id",
                    "localField": "_id",
                    "pipeline": [
                        {
                            "$match": {
                                "is_cancel": {
                                    "$eq": False,
                                }
                            }
                        },
                        {
                            "$project": {
                                "game_coin": {
                                    "$cond": {
                                        "if": {
                                            "$eq": [ "$base_type", "money_in"]
                                        },
                                        "then": {
                                            "$multiply": ["$game_coin", -1]
                                        },
                                        "else": "$game_coin",
                                    }
                                },
                                "game_coin_fee": True,
                                "game_coin_correction": True,
                            }
                        }
                    ],
                    "as": "trade_docs"
                }
            },
            {
                "$project": {
                    "_id": {
                        "$toString": "$_id",
                    },
                    "role_name": True,
                    "balance": {
                        "$sum": [
                            "$init_amount",
                            {
                                "$sum": ["$trade_docs.game_coin"],
                            },
                            {
                                "$multiply": [
                                    {
                                        "$sum": ["$trade_docs.game_coin_fee"],
                                    },
                                    -1
                                ]
                            },
                            {
                                "$multiply": [
                                    {
                                        "$sum": ["$trade_docs.game_coin_correction"],
                                    },
                                    -1
                                ]
                            }
                        ],
                    }
                },
            },
        ]).to_list(length = None)

        return {
            "data": stocks_data,
            "info": {
                "pageCount": 1
            },
            "message": "Stock list get success."
        }
    except Exception as error:
        if hasattr(error, 'status_code'):
            raise HTTPException(status_code = error.status_code, detail = error.detail)
        else:
            raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Stock list get error.")
