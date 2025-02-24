# =====================================================================================================================
#                   Import
# =====================================================================================================================
from typing import Callable
from functools import wraps

from fastapi import HTTPException

from error import HttpError, DBException


# =====================================================================================================================
#                   Function Prototype
# =====================================================================================================================
def except_process(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)

        except Exception as error:
            if isinstance(error, DBException):
                raise error.response
            elif isinstance(error, HTTPException):
                raise error
            else:
                print("BUG:     ", error)
                raise HttpError.Error_500_Internal_Server_Error()

    return wrapper
