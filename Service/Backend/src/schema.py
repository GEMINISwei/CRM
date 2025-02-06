# =====================================================================================================================
#                   Import
# =====================================================================================================================
from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from fastapi import Request
from dataclasses import dataclass, field


# =====================================================================================================================
#                   Custom Modeal
# =====================================================================================================================
class CustomBaseModel(BaseModel):
    def to_json(self):
        return jsonable_encoder(self)


class CustomQueryRequest(Request):
    @staticmethod
    def to_json(query_data):
        result_json = {}

        if query_data:
            for key_and_value in str(query_data).split("&"):
                [key, value] = key_and_value.split("=")
                result_json[key] = str(value)

        return result_json


# =====================================================================================================================
#                   User Schema
# =====================================================================================================================
class UserSchema(CustomBaseModel):
    # 使用者名稱
    name: str
    email: str
    password: str


class UserCreateRequest(CustomBaseModel):
    name: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)


class UserLoginRequest(CustomBaseModel):
    name: str = Field(...)
    password: str = Field(...)


# =====================================================================================================================
#                   Game Schema
# =====================================================================================================================
@dataclass
class GameSchema:
    # 遊戲名稱
    name: str
    # 入金 - 賣出遊戲幣之匯率
    money_in_exchange: float
    # 出金 - 買入遊戲幣之匯率
    money_out_exchange: float
    # 交易手續費
    charge_fee: int
    # 遊戲幣手續費率
    game_coin_fee: float
    # 建立時間
    created_time: datetime = field(default_factory=lambda: datetime.now())


# =====================================================================================================================
#                   Member Schema
# =====================================================================================================================
class MemberSchema(CustomBaseModel):
    game_id: str                                # 關聯之 Game Id
    nickname: str                               # 遊戲暱稱
    accounts: List[str]                         # 會員個人帳戶
    sock_puppets: List[str]                     # 分身帳號
    phones: List[str]                           # 電話 / 手機號碼
    sex: Optional[str]                          # 性別
    f_communication_time: Optional[datetime]    # 第一次交流時間
    f_communication_way: Optional[str]          # 第一次交流方式
    f_communication_amount: Optional[int]       # 第一次交流金額
    description: Optional[str]                  # 註解


class MemberCreateRequest(CustomBaseModel):
    game_id: str = Field(...)
    nickname: str = Field(...)
    accounts: Optional[List[str]] = Field(default=[])
    sock_puppets: Optional[List[str]] = Field(default=[])
    phones: Optional[List[str]] = Field(default=[])
    sex: Optional[str] = Field(default=None)
    f_communication_time: Optional[datetime] = Field(default=None)
    f_communication_way: Optional[str] = Field(default=None)
    f_communication_amount: Optional[int] = Field(default=None)
    description: Optional[str] = Field(default=None)


class MemberUpdateRequest(CustomBaseModel):
    accounts: Optional[List[str]] = Field(default = [])
    sock_puppets: Optional[List[str]] = Field(default = [])
    phones: Optional[List[str]] = Field(default = [])
    sex: Optional[str] = Field(default = None)
    f_communication_time: Optional[datetime] = Field(default=None)
    f_communication_way: Optional[str] = Field(default=None)
    f_communication_amount: Optional[int] = Field(default=None)
    description: Optional[str] = Field(default = None)


class MemberListRequest(CustomBaseModel):
    page: str = Field(...)
    count: str = Field(...)
    game_id: str = Field(...)
    nickname: Optional[str] = Field(...)
    accounts: Optional[str] = Field(default="")
    sock_puppets: Optional[str] = Field(default="")
    phones: Optional[str] = Field(default="")


# =====================================================================================================================
#                   Stock Schema
# =====================================================================================================================
class StockSchema(CustomBaseModel):
    game_id: str        # 關聯之 Game Id
    role_name: str      # 角色名稱
    init_amount: int    # 初始金額

class StockCreateSchema(CustomBaseModel):
    game_id: str = Field(...)
    role_name: str = Field(...)
    init_amount: Optional[int] = Field(default = 0)


class StockUpdateSchema(CustomBaseModel):
    init_amount: Optional[int] = Field(default = 0)


# =====================================================================================================================
#                   Property Schema
# =====================================================================================================================
class PropertyCreateSchema(CustomBaseModel):
    name: str = Field(...)
    kind: str = Field(...)
    account: Optional[str] = Field(default = None)
    init_amount: Optional[int] = Field(default = 0)


# =====================================================================================================================
#                   Trade Schema
# =====================================================================================================================
# member_id             關聯 Member Collection
# property_id           關聯 Property Collection
# stock_id              關聯 Stock Collection
# base_type             出入金類型
# money                 金額
# charge_fee            交易手續費
# game_coin             遊戲幣
# game_coin_fee         遊戲幣手續費
# stage_fee             平台費用
# money_correction      金額修正
# game_coin_correction  遊戲幣修正
# details               詳細內容
# is_matched            是否媒合完成
# is_cancel             是否取消此單
# first_check           第一次檢查
# second_check          第二次檢查
class TradeCreateSchema(CustomBaseModel):
    member_id: str = Field(...)
    property_id: str = Field(...)
    stock_id: str = Field(...)
    base_type: str = Field(...)
    money: int = Field(...)
    charge_fee: int = Field(...)
    game_coin: int = Field(...)
    game_coin_fee: int = Field(...)
    stage_fee: Optional[int] = Field(default = 0)
    money_correction: Optional[int] = Field(default = 0)
    game_coin_correction: Optional[int] = Field(default = 0)
    details: Optional[dict] = Field(default = {})
    is_matched: Optional[bool] = Field(default = False)
    is_cancel: Optional[bool] = Field(default = False)
    first_check: str = Field(...)
    second_check: Optional[str] = Field(default = None)


class TradeUpdateSchema(CustomBaseModel):
    details: Optional[dict] = Field(default = {})
    money_correction: Optional[int] = Field(default = 0)
    game_coin_correction: Optional[int] = Field(default = 0)


class TradeCheckSchema(CustomBaseModel):
    second_check: Optional[str] = Field(default = None)


# =====================================================================================================================
#                   Match Schema
# =====================================================================================================================
class MatchSchema(CustomBaseModel):
    order_number: str           # 單據號碼
    buy_trade_id: str           # 出金 - 買入交易紀錄
    sell_trade_ids: List[str]   # 入金 - 賣出交易紀錄 (多組)
    total_money: int            # 買入金額
    no_match_money: int         # 尚未媒合金額
    is_cancel: bool             # 是否取消此紀錄


# =====================================================================================================================
#                   Match Schema
# =====================================================================================================================
class CouponSchema(CustomBaseModel):
    name: str               # 活動名稱
    start_time: datetime    # 開始時間
    end_time: datetime      # 結束時間
    money_floor: int        # 滿額條件
    money_free: int         # 優惠金額


class CouponCreateRequest(CustomBaseModel):
    name: str = Field(...)
    start_time: datetime = Field(...)
    end_time: datetime = Field(...)
    money_floor: int = Field(...)
    money_free: int = Field(...)


# =====================================================================================================================
#                   Setting Schema
# =====================================================================================================================
class SettingUpdateRequest(CustomBaseModel):
    collection_name: str = Field(...)
    update_type: str = Field(...)
    field_name: str = Field(...)
    field_value: Any = Field(...)
