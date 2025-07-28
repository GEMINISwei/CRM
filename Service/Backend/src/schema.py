# =====================================================================================================================
#                   Import
# =====================================================================================================================
from typing import List
from datetime import datetime
from dataclasses import dataclass, field


# =====================================================================================================================
#                   Class
# =====================================================================================================================
class DataSchema:
    @classmethod
    def set_schema_data(cls, name: str, data: dict):
        try:
            necessary_fields = eval(f"{name.capitalize()}.__annotations__")
            necessary_data = {
                key: value for key, value in data.items() if key in necessary_fields
            }

            return eval(f"{name.capitalize()}")(**necessary_data).__dict__

        except Exception as error:
            print(error)

    @classmethod
    def get_schema_fields(cls, name: str):
        try:
            necessary_fields = eval(f"{name.capitalize()}.__annotations__")
            necessary_data = [
                field for field in necessary_fields
            ]

            return necessary_data

        except Exception as error:
            print(error)


@dataclass
class User:
    username: str
    password: str
    disabled: bool = field(default=False)
    access_token: str = field(default="")
    shift: str = field(default="")
    level_group: str = field(default="Initialize")


@dataclass
class Game:
    name: str
    money_in_exchange: float
    money_out_exchange: float
    filter_setting: str
    charge_fee: int = field(default=0)
    game_coin_fee: float = field(default=0.0)
    market_free_fee: int = field(default=0)


@dataclass
class Member:
    game_id: str
    sex: str = field(default=None)
    accounts: List[str] = field(default_factory=list)
    phones: List[str] = field(default_factory=list)
    description: str = field(default=None)
    first_info: dict = field(default_factory=dict)


@dataclass
class Player:
    member_id: str
    name: str
    is_main: bool


@dataclass
class Property:
    name: str
    kind: str
    account: str = field(default=None)
    init_amount: int = field(default=0)


@dataclass
class Stock:
    game_id: str
    role_name: str
    init_amount: int = field(default=0)


@dataclass
class Trade:
    member_id: str
    player_id: str
    property_id: str
    stock_id: str
    base_type: str
    money: int
    charge_fee: int
    game_coin: int
    game_coin_fee: int
    created_by: str
    order_number: str = field(default=None)
    stage_fee: int = field(default=0)
    money_correction: int = field(default=0)
    game_coin_correction: int = field(default=0)
    details: dict = field(default_factory=dict)
    completed_by: bool = field(default=None)
    checked_by: bool = field(default=None)
    is_matched: bool = field(default=False)
    is_cancel: bool = field(default=False)
    time_at: datetime = field(default_factory=lambda: datetime.now())


@dataclass
class Activity:
    game_id: str
    name: str
    base_type: str
    start_time: datetime
    end_time: datetime
    money_floor: int
    coin_free: int


@dataclass
class MatchSchema:
    order_number: str
    buy_trade_id: str
    total_money: int
    no_match_money: int
    is_cancel: bool
    sell_trade_ids: List[str] = field(default_factory=lambda: list)
