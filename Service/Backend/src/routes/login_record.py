# =====================================================================================================================
#                   Import
# =====================================================================================================================
from typing import List, Optional, Self
from datetime import datetime
from dateutil.relativedelta import relativedelta

from fastapi import Request
from pydantic import BaseModel, Field

from router import BaseRouter
from database import BaseCollection, BasePipeline, BaseCondition


# =====================================================================================================================
#                   Class
# =====================================================================================================================
class LoginRecordResponse:
    class List(BaseModel):
        list_data: List[dict] = Field(...)
        page_count: int = Field(...)


# =====================================================================================================================
#                   Variable
# =====================================================================================================================
router = BaseRouter()
collection = BaseCollection(name="login_record")


# =====================================================================================================================
#                   Member Router
# =====================================================================================================================
@router.set_route(method="get", url="/login_records")
async def get_login_record_list(
    request: Request
) -> LoginRecordResponse.List:
    search_time = datetime.strptime(request.query_params.get('search_time'), '%Y-%m-%d')
    current_date_start = search_time.replace(hour=0, minute=0, second=0, microsecond=0)
    current_date_end = current_date_start + relativedelta(days=1)

    print(current_date_start)
    print(current_date_end)

    result_data = await collection.get_list_data(
        pipelines=[
             BasePipeline.match(
                BaseCondition.and_expression(
                    BaseCondition.greater_than("$login_time", current_date_start, equl=True),
                    BaseCondition.less_than("$login_time", current_date_end),
                )
            ),
            BasePipeline.lookup(
                name="user",
                key="user_id",
                pipelines=[
                    BasePipeline.project(
                        show=['nickname', 'login_time']
                    )
                ]
            ),
            BasePipeline.project(
                show=['login_time'],
                custom={
                    'nickname': {
                        '$first': '$user.nickname'
                    },
                }
            )
        ]
    )

    print(result_data)

    return result_data
