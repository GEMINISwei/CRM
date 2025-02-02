# =====================================================================================================================
#                   Import
# =====================================================================================================================
import math
from fastapi import APIRouter, HTTPException, status, Request
from fastapi.encoders import jsonable_encoder
from database import trades_collection
from utils.match import find_match, create_match
from schema import TradeCreateSchema, TradeUpdateSchema, TradeCheckSchema, CustomQueryRequest
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from typing import List

# =====================================================================================================================
#                   Declare Variable
# =====================================================================================================================
router = APIRouter()


# =====================================================================================================================
#                   Trade Router
# =====================================================================================================================
@router.post("/trades")
async def create_trade(request_data: TradeCreateSchema):
    try:
        new_data = request_data.to_json()
        now_time = datetime.now()
        current_date_start = now_time.replace(hour=0, minute=0, second=0, microsecond=0)
        current_date_end = current_date_start + timedelta(days=1)
        today_exist_count = await trades_collection.find({
            "time_at": {
                "$gte": current_date_start,
                "$lt": current_date_end
            }
        }).to_list(length=None)

        order_type = "B" if new_data["base_type"] == "money_out" else "S"
        order_date = now_time.strftime("%Y%m%d")
        order_index = len(today_exist_count) + 1

        new_data["member_id"] = ObjectId(new_data["member_id"])
        new_data["property_id"] = ObjectId(new_data["property_id"])
        new_data["stock_id"] = ObjectId(new_data["stock_id"])
        new_data["order_number"] = f"{order_type}{order_date}{order_index:0>3d}"
        new_data["is_matched"] = True if new_data["base_type"] == "money_out" else False
        new_data["time_at"] = now_time

        result_trade = await trades_collection.insert_one(new_data)

        trade_id = str(result_trade.inserted_id)
        money = new_data["money"]

        # 出金 (買入) 時, 建立媒合單
        if new_data["base_type"] == "money_out":
            await create_match(trade_id, money)

            # 建立新的媒合單, 順便媒合尚未媒合的交易單
            no_matched_trades = await trades_collection.aggregate([
                {
                    "$match": {
                        "is_cancel": {
                            "$eq": False
                        },
                        "is_matched": {
                            "$eq": False
                        }
                    }
                }
            ]).to_list(length=None)

            for trade in no_matched_trades:
                find_result = await find_match(str(trade["_id"]), trade["money"])
                await trades_collection.update_one({ "_id": trade["_id"] }, {
                    "$set": { "is_matched": find_result }
                })

        # 入金 (賣出) 時, 開始媒合
        elif new_data["base_type"] == "money_in":
            find_result = await find_match(trade_id, money)
            await trades_collection.update_one({ "_id": ObjectId(trade_id) }, {
                "$set": { "is_matched": find_result }
            })

        return {
            "data": {
                "order_number": new_data["order_number"]
            },
            "message": "Trade create success."
        }

    except Exception as error:
        print(error)
        if hasattr(error, 'status_code'):
            raise HTTPException(status_code = error.status_code, detail = error.detail)
        else:
            raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Trade create failure.")


@router.get("/trades/{id}")
async def get_trade(id: str):
    try:
        trade_data = await trades_collection.find_one({"_id": ObjectId(id)})
        if not trade_data:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Trade not found.")

        trade_data["_id"] = str(trade_data["_id"])
        trade_data["member_id"] = str(trade_data["member_id"])
        trade_data["property_id"] = str(trade_data["property_id"])
        trade_data["stock_id"] = str(trade_data["stock_id"])

        return {
            "data": trade_data,
            "message": "Trade get success."
        }

    except Exception as error:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Trade Get failure.")


@router.get("/trades")
async def get_trade_list(request_data: Request):
    query_condition = {}
    query_data = CustomQueryRequest.to_json(request_data.query_params)
    page = int(query_data["page"])
    count = int(query_data["count"])

    if query_data["property_id"]:
        query_condition['property_id'] = { '$eq': query_data["property_id"] }

    # if query_data["member_game_name"]:
    #     query_condition['member_game_name'] = { '$regex': re.compile((query_data["member_game_name"])) }

    # if request.query_params.get('status'):
    #     query_condition['status'] = { '$regex': re.compile((request.query_params.get('status'))) }

    show_trades_data, total_data_count = await get_trades_data(query_condition, count, page)

    return {
        "data": show_trades_data,
        "info": {
            'pageCount': math.ceil(total_data_count / count)
        },
        "message": "Trade list get success."
    }


@router.patch("/trades/{id}")
async def update_trade(id: str, updateData: TradeUpdateSchema):
    try:
        new_data = jsonable_encoder(updateData)
        trade_data = await trades_collection.find_one({"_id": ObjectId(id)})
        if not trade_data:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Trade not found.")

        await trades_collection.update_one({ "_id": ObjectId(id) }, { "$set": new_data })

        return {
            "data": {},
            "message": "Trade update success."
        }

    except Exception as error:
        if hasattr(error, 'status_code'):
            raise HTTPException(status_code = error.status_code, detail = error.detail)
        else:
            raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Trade create failure.")


@router.patch("/trades/{id}/check")
async def update_trade_check(id: str, updateData: TradeCheckSchema):
    try:
        new_data = jsonable_encoder(updateData)
        trade_data = await trades_collection.find_one({"_id": ObjectId(id)})
        if not trade_data:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Trade not found.")

        await trades_collection.update_one({ "_id": ObjectId(id) }, { "$set": new_data })

        return {
            "data": {},
            "message": "Trade update success."
        }

    except Exception as error:
        if hasattr(error, 'status_code'):
            raise HTTPException(status_code = error.status_code, detail = error.detail)
        else:
            raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Trade create failure.")


@router.delete("/trades/{id}")
async def delete_trade(id: str):
    try:
        trade_data = await trades_collection.find_one({"_id": ObjectId(id)})

        if not trade_data:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Trade not found.")

        result = await trades_collection.update_one({ "_id": ObjectId(id) }, { "$set": { "is_cancel": True } })

        return {
            "data": {},
            "message": "Trade update success."
        }

    except Exception as error:
        if hasattr(error, 'status_code'):
            raise HTTPException(status_code = error.status_code, detail = error.detail)
        else:
            raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Trade create failure.")


async def get_trades_data(conditions: dict, count: int = 0, page: int = 1):
    show_trades_data = []
    query_pipeline = []
    show_pipeline = []
    count_pipeline = []
    total_data_count = 0

    # 關聯 Members Collection
    query_pipeline.append({
        "$lookup": {
            "from": "members",
            "foreignField": "_id",
            "localField": "member_id",
            "pipeline": [
                {
                    "$lookup": {
                        "from": "games",
                        "foreignField": "_id",
                        "localField": "game_id",
                        "as": "game_docs",
                    }
                },
                {
                    "$project": {
                        "_id": False,
                        "game_kind": {
                            "$getField": {
                                "field": "name",
                                "input": {
                                    "$first": "$game_docs"
                                }
                            }
                        },
                        "game_name": True,
                    }
                }
            ],
            "as": "member_docs",
        }
    })
    query_pipeline.append({
        "$lookup": {
            "from": "properties",
            "foreignField": "_id",
            "localField": "property_id",
            "as": "property_docs",
        }
    })
    query_pipeline.append({
        "$lookup": {
            "from": "stocks",
            "foreignField": "_id",
            "localField": "stock_id",
            "as": "stock_docs",
        }
    })
    query_pipeline.append({
        "$lookup": {
            "from": "trades",
            "let": {
                "id": "$_id",
                "property_id": "$property_id",
                "status": "$status",
            },
            "pipeline": [
                {
                    "$match": {
                        "$expr": {
                            "$and": [
                                {
                                    "$eq": ["$is_cancel", False],
                                },
                                {
                                    "$eq": ["$property_id", "$$property_id"]
                                },
                                {
                                    "$lte": ["$_id", "$$id"]
                                }
                            ]
                        }
                    },
                },
                {
                    "$project": {
                        "_id": False,
                        "total_money": {
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
                        "total_fee": {
                            "$multiply": ["$charge_fee", -1]
                        },
                        "money_correction": {
                            "$multiply": ["$money_correction", -1]
                        }
                    }
                }
            ],
            "as": "trade_docs",
        }
    })

    query_pipeline.append({
        "$match": {
            "is_cancel": False
        }
    })

    # 產出資料格式
    query_pipeline.append({
        "$project": {
            "_id": {
                "$toString": "$_id"
            },
            "property_id": {
                "$toString": "$property_id"
            },
            "member_game_kind": {
                "$getField": {
                    "field": "game_kind",
                    "input": {
                        "$first": "$member_docs"
                    }
                }
            },
            "member_game_name": {
                "$getField": {
                    "field": "game_name",
                    "input": {
                        "$first": "$member_docs"
                    }
                }
            },
            "stock_role_name": {
                "$getField": {
                    "field": "role_name",
                    "input": {
                        "$first": "$stock_docs"
                    }
                }
            },
            "base_type": True,
            "charge_method": {
                "$getField": {
                    "field": "kind",
                    "input": {
                        "$first": "$property_docs"
                    }
                }
            },
            # "details": True,
            "custom_no": {
                "$getField": {
                    "field": "custom_no",
                    "input": "$details"
                }
            },
            "pay_code": {
                "$getField": {
                    "field": "pay_code",
                    "input": "$details"
                }
            },
            "store": {
                "$getField": {
                    "field": "store",
                    "input": "$details"
                }
            },
            "last_five_code": {
                "$getField": {
                    "field": "last_five_code",
                    "input": "$details"
                }
            },
            "record_time": {
                "$getField": {
                    "field": "record_time",
                    "input": "$details"
                }
            },
            "v_account": {
                "$getField": {
                    "field": "v_account",
                    "input": "$details"
                }
            },
            "money": True,
            "charge_fee": True,
            "game_coin": {
                "$sum": [
                    "$game_coin",
                    "$game_coin_correction"
                ]
            },
            "balance": {
                "$sum": [
                    {
                        "$sum": [
                            "$property_docs.init_amount",
                        ]
                    },
                    {
                        "$sum": [
                            "$trade_docs.total_money",
                        ]
                    },
                    {
                        "$sum": [
                            "$trade_docs.total_fee",
                        ]
                    },
                    {
                        "$sum": [
                            "$trade_docs.money_correction",
                        ]
                    }
                ]
            },
            "real_in": {
                "$sum": [
                    "$money",
                    {
                        "$multiply": ["$charge_fee", -1]
                    },
                    "$stage_fee",
                ]
            },
            "time_at": {
                "$dateToString": {
                    "format": "%Y-%m-%d %H:%M:%S",
                    "date": "$time_at"
                }
            },
            "first_check": True,
            "second_check": True,
        },
    })

    # 新增搜尋條件
    if len(conditions) != 0:
        query_pipeline.append({
            "$match": conditions
        })

    # 顯示數量及分頁顯示
    show_pipeline.append({
        "$skip": (page - 1) * count
    })
    show_pipeline.append({
        "$limit": count
    })

    show_pipeline.append({
        "$sort": {
            "_id": -1
        }
    })

    # 符合資料的總筆數
    count_pipeline.append({
        "$count": "data_count"
    })

    show_trades_data = await trades_collection.aggregate(query_pipeline + show_pipeline).to_list(length = None)

    if len(show_trades_data) != 0:
        total_data_obj = await trades_collection.aggregate(query_pipeline + count_pipeline).to_list(length = None)
        total_data_count = total_data_obj[0]["data_count"]

    return show_trades_data, total_data_count
