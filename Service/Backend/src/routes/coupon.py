# =====================================================================================================================
#                   Import
# =====================================================================================================================
from fastapi import APIRouter, HTTPException, status, Request
from fastapi.encoders import jsonable_encoder
from database import DatabaseAggregation, coupons_collection
from schema import CouponSchema, CouponCreateRequest
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from typing import List

# =====================================================================================================================
#                   Declare Variable
# =====================================================================================================================
router = APIRouter()


# =====================================================================================================================
#                   Trade Router
# =====================================================================================================================@router.get("/members")
@router.post("/coupons")
async def create_coupon(request_data: CouponCreateRequest):
    try:
        new_data = request_data.to_json()
        # now_time = datetime.now()
        new_coupon = CouponSchema(**new_data).to_json()
        new_coupon["start_time"] = datetime.strptime(new_coupon["start_time"], "%Y-%m-%dT%H:%M:%S")
        new_coupon["end_time"] = datetime.strptime(new_coupon["end_time"], "%Y-%m-%dT%H:%M:%S")

        await coupons_collection.insert_one(new_coupon)

        return {
            "data": {
                "name": new_coupon["name"]
            },
            "message": "Coupon create success."
        }
    except Exception as error:
        print(error)
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Coupon create failure.")


@router.get("/coupons")
async def get_coupon_list():
    try:
        aggregation = DatabaseAggregation()
        aggregation.add_time_range_pipline("start_time", "end_time")
        aggregation.add_output_pipeline(fields=[
            "name", "start_time", "end_time", "money_floor", "money_free"
        ])
        print(aggregation.pagination_pipelines)
        aggregation_result = await coupons_collection.aggregate(aggregation.pagination_pipelines).to_list(length=None)
        result_json = DatabaseAggregation.format_data(aggregation_result)
        print(result_json["data"])

        return {
            "data": result_json["data"],
            "info": result_json["info"],
            "message": "Coupon list get success."
        }
    except Exception as error:
        print(error)
        if hasattr(error, 'status_code'):
            raise HTTPException(status_code=error.status_code, detail=error.detail)
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Coupon list get error.")
