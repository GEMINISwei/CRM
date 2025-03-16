# =====================================================================================================================
#                   Import
# =====================================================================================================================
from fastapi import Request

from router import BaseRouter
from database import BaseCollection, BasePipeline, BaseCondition


# =====================================================================================================================
#                   Variable
# =====================================================================================================================
router = BaseRouter()
collection = BaseCollection(name="match")


# =====================================================================================================================
#                   Function
# =====================================================================================================================
# async def find_match(trade_id, money):
#     try:
#         find_result = False
#         need_update = False
#         update_data = []

#         no_complete_match = await collection.get_list_data(
#             pipelines=[
#                 BasePipeline.match(
#                     equl={
#                         "is_cancel": False
#                     },
#                     not_equl={
#                         "current_money": 0
#                     }
#                 )
#             ]
#         )

#         for match_order in no_complete_match:
#             if match_order["no_match_money"] >= money:
#                 match_order["no_match_money"] = match_order["no_match_money"] - money
#                 money = 0
#             else:
#                 money = money - match_order["no_match_money"]
#                 match_order["no_match_money"] = 0

#             match_order["sell_trade_ids"].append(trade_id)
#             update_data.append(match_order)

#             if money == 0:
#                 need_update = True
#                 break

#         if need_update:
#             for data in update_data:
#                 await matches_collection.update_one({ "_id": data["_id"] }, { "$set": data })
#                 find_result = True

#         return find_result

#     except Exception as error:
#         print(2, error)


# async def create_match(trade_id, money):
#     try:
#         new_data = {}

#         exist_count = await matches_collection.find().to_list(length=None)
#         order_index = len(exist_count) + 1

#         new_data["order_number"] = f"M{order_index:0>9d}"
#         new_data["buy_trade_id"] = trade_id
#         new_data["sell_trade_ids"] = []
#         new_data["total_money"] = money
#         new_data["no_match_money"] = money
#         new_data["is_cancel"] = False

#         new_match = MatchSchema(**new_data).to_json()
#         await matches_collection.insert_one(new_match)

#     except Exception as error:
#         print(error)


# =====================================================================================================================
#                   Trade Router
# =====================================================================================================================@
@router.set_route(method="get", url="matches")
async def get_match_list(
    request: Request
):
    result_data = await collection.get_list_data(
        pipelines=[
            BasePipeline.match(
                BaseCondition.equl("$is_cancel", False)
            ),
            BasePipeline.project(
                custom={
                    "money": BasePipeline.subtract(
                        items=[
                            "$total_money", "$no_match_money"
                        ]
                    )
                }
            )
        ]
    )

    return result_data
