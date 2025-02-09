# =====================================================================================================================
#                   Import
# =====================================================================================================================
import os
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from dataclasses import dataclass
from routes.game import router as GameRouter
from routes.member import router as MemberRouter
from routes.property import router as PropertyRouter
from routes.stock import router as StockRouter
from routes.trade import router as TradeRouter
from routes.match import router as MatchRouter
from routes.coupon import router as CouponRouter
from routes.setting import router as SettingRouter
from routes.user import router as UserRouter


# =====================================================================================================================
#                   Environment Variable
# =====================================================================================================================
ENV_API_URL = os.environ["API_URL"]
ENV_MODE = os.environ["MODE"]


# =====================================================================================================================
#                   Global Settings
# =====================================================================================================================
# 設置主要的 API & 允許串接 IP, 等等前端才能連進來
# Production 環境
if ENV_MODE == "Production":
    app = FastAPI(docs_url=None, redoc_url=None)
# Development 環境
elif ENV_MODE == "Development":
    app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ENV_API_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================================================================================
#                   Routes Setting
# =====================================================================================================================
api_routers = {
    "Game": GameRouter,
    "Member": MemberRouter,
    "Property": PropertyRouter,
    "Stock": StockRouter,
    "Trade": TradeRouter,
    "Match": MatchRouter,
    "Coupon": CouponRouter,
    "Setting": SettingRouter,
    "User": UserRouter,
}

for tag, router in api_routers.items():
    app.include_router(router, tags=[tag], prefix="/apis")



# =====================================================================================================================
#                   Websocker Setting
# =====================================================================================================================
@dataclass
class WebsocketInfo:
    # def __init__(self, handle: WebSocket, username: str):
    handle: WebSocket
    username: str

connected_info: List[WebsocketInfo] = []


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        # await broadcast_users()
        while True:
            data = await websocket.receive_text()
            # 可根據需求處理接收到的訊息
            json_data = json.loads(data)
            if json_data.get("login"):
                ws_info = WebsocketInfo(
                    handle=websocket,
                    username=json_data["login"]["username"]
                )
                connected_info.append(ws_info)
                await broadcast_users()

    except WebSocketDisconnect:
        disconnect_index = list(map(lambda x: x.__dict__["handle"], connected_info)).index(websocket)
        del connected_info[disconnect_index]
        await broadcast_users()


async def broadcast_users():
    online_users = list(map(lambda x: x.__dict__["username"], connected_info))

    sendInfo = {
        "online_users": online_users
    }

    # 向所有客戶端廣播當前在線使用者數量
    for info in connected_info:
        print(sendInfo)
        await info.handle.send_text(json.dumps(sendInfo))
