# =====================================================================================================================
#                   Import
# =====================================================================================================================
from typing import List, Optional
from datetime import datetime
from dateutil.relativedelta import relativedelta
import math

from fastapi import Request
from pydantic import BaseModel, Field

from router import BaseRouter
from database import BaseCollection, BasePipeline, BaseCondition


# =====================================================================================================================
#                   Class
# =====================================================================================================================
class SplitTradeRequest:
    class Create(BaseModel):
        money: int = Field(...)
        created_by: str = Field(...)
        is_finish: bool = Field(default=False)

    class Refund(BaseModel):
        refund_money: int = Field(...)
        created_by: str = Field(...)



class SplitTradeResponse:
    class Operate(BaseModel):
        id: str = Field(...)

    class List(BaseModel):
        list_data: List[dict] = Field(...)
        page_count: int = Field(...)


# =====================================================================================================================
#                   Variable
# =====================================================================================================================
router = BaseRouter()
collection = BaseCollection(name="split_trade")
trade_collection = BaseCollection(name="trade")


# =====================================================================================================================
#                   Function
# =====================================================================================================================
async def create_split_trade(is_main: bool, split_data: dict):
    final_data: dict = {
        "main_trade_id": "",
        "sub_trade_ids": [],
        "temp_trade_id": "",
        "total_money": 0,
    }

    # 用資料來判斷是拆帳中的主帳還是分帳
    if is_main is True:
        final_data['main_trade_id'] = split_data['trade_id']
        final_data['sub_trade_ids'].append(split_data['trade_id'])
        final_data['temp_trade_id'] = split_data['temp_trade_id']
        final_data['total_money'] = split_data['total_money']
    else:
        final_data['sub_trade_ids'].append(split_data['trade_id'])

    await collection.create_data(
        data=final_data
    )


# =====================================================================================================================
#                   Game Router
# =====================================================================================================================
@router.set_route(method="get", url="/split_trades")
async def get_split_trade_list(
    request: Request
) -> SplitTradeResponse.List:
    result_data = await collection.get_list_data(
        pipelines=[
            BasePipeline.match(
                BaseCondition.not_equl("$temp_trade_id", "")
            ),
            BasePipeline.lookup(
                name="trade",
                key="main_trade_id",
                output="main_trade",
                pipelines=[
                    BasePipeline.lookup(
                        name="property",
                        key="property_id",
                    ),
                    BasePipeline.lookup(
                        name="member",
                        key="member_id",
                        pipelines=[
                            BasePipeline.lookup(
                                name="player",
                                key="id",
                                conditions=[
                                    BaseCondition.equl("$member_id", "$$id")
                                ]
                            ),
                            BasePipeline.project(
                                name="member",
                                show=["player"],
                                custom={
                                    'nickname': {
                                        '$first': '$player.name'
                                    },
                                }
                            ),
                        ]
                    ),
                    BasePipeline.project(
                        name="trade",
                        show=['time_at', 'property'],
                        custom={
                            'member_name': {
                                '$first': '$member.nickname'
                            },
                            'property_name': {
                                '$first': '$property.name'
                            },
                            'property_kind': {
                                '$first': '$property.kind'
                            },
                            'property_id': {
                                '$first': '$property.id'
                            }
                        }
                    )
                ]
            ),
            BasePipeline.lookup(
                name="trade",
                key="sub_trade_ids",
                output="sub_trades",
                conditions=[
                    BaseCondition.include("$id", "$$sub_trade_ids"),
                ],
            ),
            BasePipeline.project(
                show=['total_money'],
                custom={
                    'date': {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": {
                                '$first': '$main_trade.time_at'
                            }
                        }
                    },
                    'member_name': {
                        '$first': '$main_trade.member_name'
                    },
                    "already_money": {
                        '$sum': '$sub_trades.money'
                    },
                    'property_name': {
                        '$first': '$main_trade.property_name'
                    },
                    'property_kind': {
                        '$first': '$main_trade.property_kind'
                    },
                    'property_id': {
                        '$first': '$main_trade.property_id'
                    },
                }
            )
        ],
        page=request.query_params.get("page"),
        count=request.query_params.get("count")
    )

    return result_data


@router.set_route(method="patch", url="/split_trades/{id}")
async def create_sub_split_trade(
    request: Request, form_data: SplitTradeRequest.Create
) -> SplitTradeResponse.Operate:
    form_data = form_data.model_dump()
    current_split_trade_id = request.path_params.get("id")

    split_trade = await collection.get_data(
        pipelines=[
            BasePipeline.match(
                BaseCondition.equl("$id", current_split_trade_id)
            )
        ]
    )

    main_trade = await trade_collection.get_data(
        pipelines=[
            BasePipeline.match(
                BaseCondition.equl("$id", split_trade.get('main_trade_id'))
            ),
            BasePipeline.lookup(
                name="game",
                key="game_id",
            )
        ]
    )

    # 以此次拆帳金額計算遊戲幣
    split_game_coin = form_data['money'] * main_trade['game'][0]['money_in_exchange']
    split_game_coin = math.ceil(split_game_coin)
    split_game_coin_fee = math.ceil(split_game_coin * main_trade['game'][0]['game_coin_fee'])

    new_trade = await trade_collection.create_data(
        data={
            'game_id': main_trade['game_id'],
            'member_id': main_trade['member_id'],
            'player_id': main_trade['player_id'],
            'property_id': main_trade['property_id'],
            'stock_id': main_trade['stock_id'],
            'base_type': main_trade['base_type'],
            'money': form_data['money'],
            'charge_fee': 0,
            'game_coin': split_game_coin,
            'game_coin_fee': split_game_coin_fee,
            'created_by': form_data['created_by'],
            'time_at': datetime.now(),
            'order_number': main_trade['order_number'],
            'details': main_trade['details'],
            "completed_by": form_data['created_by'],
        }
    )

    cancel_data = await trade_collection.update_data(
        find={
            "id": split_trade['temp_trade_id']
        },
        data={
            "is_cancel": True
        }
    )

    if form_data['is_finish'] is True:
        new_temp_trade_id = ""
    else:
        temp_trade = await trade_collection.create_data(
            data={
                'game_id': main_trade['game_id'],
                'member_id': main_trade['member_id'],
                'player_id': main_trade['player_id'],
                'property_id': main_trade['property_id'],
                'stock_id': main_trade['stock_id'],
                'base_type': main_trade['base_type'],
                'money': cancel_data['money'] - form_data['money'],
                'charge_fee': 0,
                'game_coin': 0,
                'game_coin_fee': 0,
                'created_by': '',
                'time_at': datetime.now() - relativedelta(seconds=1),
                'order_number': main_trade['order_number'],
                'details': main_trade['details'],
            }
        )

        new_temp_trade_id = temp_trade['id']

    update_data = await collection.update_data(
        find={
            "id": current_split_trade_id,
        },
        data={
            "temp_trade_id": new_temp_trade_id,
        }
    )

    update_data = await collection.update_data(
        find={
            "id": current_split_trade_id
        },
        method="push",
        data={
            "sub_trade_ids": new_trade['id']
        }
    )

    return update_data


@router.set_route(method="patch", url="/refund_split_trades/{id}")
async def create_refund_split_trade(
    request: Request, form_data: SplitTradeRequest.Refund
) -> SplitTradeResponse.Operate:
    form_data = form_data.model_dump()
    current_split_trade_id = request.path_params.get("id")

    split_trade = await collection.get_data(
        pipelines=[
            BasePipeline.match(
                BaseCondition.equl("$id", current_split_trade_id)
            )
        ]
    )

    main_trade = await trade_collection.get_data(
        pipelines=[
            BasePipeline.match(
                BaseCondition.equl("$id", split_trade.get('main_trade_id'))
            ),
            BasePipeline.lookup(
                name="game",
                key="game_id",
            )
        ]
    )

    # 之前尚未處理之金額紀錄
    _ = await trade_collection.create_data(
        data={
            'game_id': main_trade['game_id'],
            'member_id': main_trade['member_id'],
            'player_id': main_trade['player_id'],
            'property_id': main_trade['property_id'],
            'stock_id': main_trade['stock_id'],
            'base_type': main_trade['base_type'],
            'money': form_data['refund_money'],
            'charge_fee': 0,
            'game_coin': 0,
            'game_coin_fee': 0,
            'created_by': main_trade['created_by'],
            'time_at': datetime.now(),
            'order_number': main_trade['order_number'],
            'details': main_trade['details'],
            'completed_by': main_trade['created_by'],
            'no_calculate': True,
        }
    )

    # 退款紀錄
    _ = await trade_collection.create_data(
        data={
            'game_id': main_trade['game_id'],
            'member_id': main_trade['member_id'],
            'player_id': main_trade['player_id'],
            'property_id': main_trade['property_id'],
            'stock_id': main_trade['stock_id'],
            'base_type': 'money_out',
            'money': form_data['refund_money'],
            'charge_fee': 0,
            'game_coin': 0,
            'game_coin_fee': 0,
            'created_by': form_data['created_by'],
            'time_at': datetime.now() + relativedelta(seconds=1),
            'order_number': main_trade['order_number'],
            'details': main_trade['details'],
            'completed_by': main_trade['created_by'],
            'is_refund': True,
            'no_calculate': True,
        }
    )

    _ = await trade_collection.update_data(
        find={
            "id": split_trade['temp_trade_id']
        },
        data={
            "is_cancel": True
        }
    )

    # Refund 直接結束拆帳, temp_trade_id 直接給空
    update_data = await collection.update_data(
        find={
            "id": current_split_trade_id,
        },
        data={
            "temp_trade_id": "",
        }
    )

    return update_data
