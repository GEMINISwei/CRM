# =====================================================================================================================
#                   Import
# =====================================================================================================================
from typing import List, Self
from datetime import datetime
from dateutil.relativedelta import relativedelta

from fastapi import Request
from pydantic import BaseModel, Field

from router import BaseRouter
from database import BaseCollection, BasePipeline


# =====================================================================================================================
#                   Class
# =====================================================================================================================
class CouponRequest:
    class Create(BaseModel):
        name: str = Field(...)
        start_time: datetime = Field(...)
        end_time: datetime = Field(...)
        money_floor: int = Field(...)
        coin_free: int = Field(...)

        def model_post_init(self: Self, _):
            self.end_time = self.end_time + relativedelta(days=1) - relativedelta(seconds=1)


class CouponResponse:
    class Operate(BaseModel):
        name: str = Field(...)

    class List(BaseModel):
        list_data: List[dict] = Field(...)
        page_count: int = Field(...)


# =====================================================================================================================
#                   Variable
# =====================================================================================================================
router = BaseRouter()
collection = BaseCollection(name="coupon")


# =====================================================================================================================
#                   Trade Router
# =====================================================================================================================
@router.set_route(method="post", url="/coupons")
async def create_coupon(
    request: Request, form_data: CouponRequest.Create
) -> CouponResponse.Operate:
    new_data = await collection.create_data(
        data=form_data.model_dump()
    )

    return new_data


@router.set_route(method="get", url="/coupons")
async def get_coupon_list(
    request: Request
) -> CouponResponse.List:
    result_data = await collection.get_list_data(
        pipelines=[
            BasePipeline.create_match(
                lte={
                    "start_time": datetime.now()
                },
                gte={
                    "end_time": datetime.now()
                }
            )
        ]
    )

    return result_data
