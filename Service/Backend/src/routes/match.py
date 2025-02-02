# =====================================================================================================================
#                   Import
# =====================================================================================================================
from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from database import matches_collection


# =====================================================================================================================
#                   Declare Variable
# =====================================================================================================================
router = APIRouter()


# =====================================================================================================================
#                   Trade Router
# =====================================================================================================================@router.get("/members")
@router.get("/matches")
async def get_match_list():
    try:
        aggregation_result = await matches_collection.aggregate([
            {
                "$match": {
                    "is_cancel": {
                        "$eq": False
                    }
                }
            },
            {
                "$addFields": {
                    "money": {
                        "$subtract": ["$total_money", "$no_match_money"]
                    }
                }
            },
            {
                "$project": {
                    "_id": False,
                    "no_match_money": False,
                }
            }
        ]).to_list(length=None)
        # result_json = DatabaseAggregation.format_data(aggregation_result)
        print(aggregation_result)

        return {
            "data": aggregation_result,
            "info": {
                "page_count": 1
            },
            "message": "Member list get success."
        }

    except Exception as error:
        print(error)
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Member list Get failure.")
