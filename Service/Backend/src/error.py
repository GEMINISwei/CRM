from fastapi import HTTPException, status


# =====================================================================================================================
#                   Class
# =====================================================================================================================
class HttpError:
    class Error_400_BadRequest(HTTPException):
        def __init__(self, err_msg = None):
            super().__init__(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=err_msg,
            )


    class Error_401_Unauthorized(HTTPException):
        def __init__(self, err_msg = "Could not validate credentials"):
            super().__init__(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=err_msg,
                headers={ "WWW-Authenticate": "Bearer" },
            )


    class Error_404_NOT_FOUND(HTTPException):
        def __init__(self, err_msg = None):
            super().__init__(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=err_msg,
            )


    class Error_405_METHOD_NOT_ALLOWED(HTTPException):
        def __init__(self, err_msg = None):
            super().__init__(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail=err_msg,
            )


    class Error_409_CONFLICT(HTTPException):
        def __init__(self, err_msg = None):
            super().__init__(
                status_code=status.HTTP_409_CONFLICT,
                detail=err_msg,
            )


    class Error_500_Internal_Server_Error(HTTPException):
        def __init__(self, err_msg = None):
            super().__init__(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=err_msg,
            )


class DBException(Exception):
    def __init__(self, response, *args):
        super().__init__(*args)
        self.response = response
