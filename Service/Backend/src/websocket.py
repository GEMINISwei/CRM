# =====================================================================================================================
#                   Import
# =====================================================================================================================
from json import dumps
from typing import Self, List

from fastapi import WebSocket


# =====================================================================================================================
#                   Class
# =====================================================================================================================
class WebsocketInfo:
    user: str
    handle: WebSocket

    def __init__(self: Self, user: str, handle: WebSocket):
        self.user = user
        self.handle = handle


class WebsocketConnection:
    active_info: List[WebsocketInfo]

    def __init__(self: Self):
        self.active_info = []

    async def connect(self: Self, user: str, handle: WebSocket):
        # 等待連接
        await handle.accept()
        # 儲存 Websocket 連接對象
        ws_info = WebsocketInfo(user=user, handle=handle)
        self.active_info.append(ws_info)

        # 通知使用者, 目前已上線的使用者
        online_users = [info.user for info in self.active_info]
        message = dumps(online_users)
        await self.send_message(user=user, message=message)

    def disconnect(self: Self, handle: WebSocket):
        matches = [idx for idx, info in enumerate(self.active_info) if info.handle == handle]
        if matches:
            match_index = matches[0]
            del self.active_info[match_index]

    # 發送個人訊息
    async def send_message(self: Self, user: str, message: str):
        match_index = [info.user for info in self.active_info].index(user)
        await self.active_info[match_index].handle.send_text(message)

    # 發送廣播
    async def broadcast(self: Self, message: str):
        for info in self.active_info:
            await info.handle.send_text(message)
