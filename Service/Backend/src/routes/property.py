# =====================================================================================================================
#                   Import
# =====================================================================================================================
import re
from fastapi import APIRouter, HTTPException, status, Request
from fastapi.encoders import jsonable_encoder
from database import properties_collection
from schema import PropertyCreateSchema
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# =====================================================================================================================
#                   Property Router
# =====================================================================================================================
router = APIRouter()


@router.post("/properties", status_code = status.HTTP_201_CREATED)
async def create_property(request: PropertyCreateSchema):
    try:
        property_data = jsonable_encoder(request)
        await properties_collection.insert_one(property_data)

        return {
            "data": {
                "name": property_data["name"]
            },
            "message": "Property create success."
        }
    except Exception as error:
        print(error)
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            message = "Property create failure."
        )

@router.get("/properties", status_code = status.HTTP_200_OK)
async def get_property_list(count: int, page: int, request: Request):
    try:
        current_time = datetime.now()
        day_start = datetime(current_time.year, current_time.month, current_time.day)
        day_end = day_start + timedelta(hours = 23, minutes = 59, seconds = 59)

        month_start = datetime(current_time.year, current_time.month, 1)
        month_end = month_start + relativedelta(months = 1) - relativedelta(seconds = 1)

        query_info = {}

        if request.query_params.get("kind"):
            query_info["kind"] = { "$regex": re.compile(request.query_params.get("kind")) }

        properties_data = await properties_collection.aggregate([
            {
                "$match": query_info
            },
            {
                "$lookup": {
                    "from": "trades",
                    "foreignField": "property_id",
                    "localField": "_id",
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$eq": ["$is_cancel", False],
                                }
                            }
                        },
                        {
                            "$project": {
                                "money": {
                                    "$cond": {
                                        "if": {
                                            "$eq": [ "$base_type", "money_in"]
                                        },
                                        "then": "$money",
                                        "else": {
                                            "$multiply": ["$money", -1]
                                        }
                                    }
                                },
                                "fee": {
                                    "$multiply": ["$charge_fee", -1]
                                },
                                "money_correction": {
                                    "$multiply": ["$money_correction", -1]
                                },
                                "stage_fee": True,
                                "in_day": {
                                    "$and": [
                                        { "$gte": ["$time_at", day_start], },
                                        { "$lte": ["$time_at", day_end], },
                                    ]
                                },
                                "in_month": {
                                    "$and": [
                                        { "$gte": ["$time_at", month_start], },
                                        { "$lte": ["$time_at", month_end], },
                                    ]
                                }
                            }
                        }
                    ],
                    "as": "trade_docs",
                }
            },
            {
                "$project": {
                    "_id": {
                        "$toString": "$_id",
                    },
                    "name": True,
                    "kind": True,
                    "account": True,
                    "today_balance": {
                        "$sum": {
                            "$map": {
                                "input": "$trade_docs",
                                "as": "trade_doc",
                                "in": {
                                    "$cond": [
                                        { "$eq": ["$$trade_doc.in_day", True] },
                                        { "$sum": ["$$trade_doc.money", "$$trade_doc.fee", "$$trade_doc.stage_fee"] },
                                        0,
                                    ]
                                }
                            }
                        }
                    },
                    "balance": {
                        "$sum": [
                            "$init_amount",
                            {
                                "$sum": ["$trade_docs.money"]
                            },
                            {
                                "$sum": ["$trade_docs.fee"]
                            },
                            {
                                "$sum": ["$trade_docs.stage_fee"]
                            },
                            {
                                "$sum": ["$trade_docs.money_correction"]
                            }
                        ]
                    },
                    "day_trade_count": {
                        "$size": {
                            "$filter": {
                                "input": "$trade_docs.in_day",
                                "as": "in_day",
                                "cond": {
                                    "$eq": ["$$in_day", True]
                                }
                            }
                        }
                    },
                    "month_trade_count": {
                        "$size": {
                            "$filter": {
                                "input": "$trade_docs.in_month",
                                "as": "in_month",
                                "cond": {
                                    "$eq": ["$$in_month", True]
                                }
                            }
                        }
                    },
                    "trade_count": {
                        "$size": "$trade_docs",
                    }
                }
            }
        ]).to_list(length = None)

        return {
            "data": properties_data,
            "info": {
                "pageCount": 1
            },
            "message": "Property list get success."
        }
    except Exception as error:
        print(error)
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Asset list get failure.")
