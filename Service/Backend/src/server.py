# =====================================================================================================================
#                   Import
# =====================================================================================================================
from os import environ
from typing import Dict

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from router import BaseRouter
from routes.user import router as UserRouter
from routes.login_record import router as LoginRecordRouter
from routes.game import router as GameRouter
from routes.member import router as MemberRouter
from routes.player import router as PlayerRouter
from routes.property import router as PropertyRouter
from routes.stock import router as StockRouter
from routes.trade import router as TradeRouter
from routes.match import router as MatchRouter
from routes.activity import router as ActivityRouter
from routes.lottery import router as LotteryRouter
from routes.setting import router as SettingRouter
from routes.report import router as ReportRouter
from websocket import WebsocketConnection


# =====================================================================================================================
#                   Variable
# =====================================================================================================================
ENV_API_URL = environ["API_URL"]
ENV_MODE = environ["MODE"]

apis_routers: Dict[str, BaseRouter] = {
    "User": UserRouter,
    "LoginRecord": LoginRecordRouter,
    "Game": GameRouter,
    "Member": MemberRouter,
    "Player": PlayerRouter,
    "Property": PropertyRouter,
    "Stock": StockRouter,
    "Trade": TradeRouter,
    "Match": MatchRouter,
    "Activity": ActivityRouter,
    "Lottery": LotteryRouter,
    "Setting": SettingRouter,
    "Report": ReportRouter,
}


# =====================================================================================================================
#                   Program
# =====================================================================================================================
# Production 環境
if ENV_MODE == "Production":
    app = FastAPI(docs_url=None, redoc_url=None)
# Development 環境
elif ENV_MODE == "Development":
    app = FastAPI()

# 設置主要的 API & 允許串接 IP, 等等前端才能連進來
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ENV_API_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 設置 API 之 Router
for tag, router in apis_routers.items():
    app.include_router(router, tags=[tag], prefix="/apis")

# Websocket 設置
websocket_connection = WebsocketConnection()
@app.websocket("/ws/{user}")
async def websocket_endpoint(websocket: WebSocket, user: str):
    await websocket_connection.connect(user=user, handle=websocket)

    try:
        while True:
            data = await websocket.receive_text()
            # 可根據需求處理接收到的訊息
            print(data)

    except WebSocketDisconnect:
        websocket_connection.disconnect(websocket)
        await websocket_connection.broadcast(f"\"{user}\" 已下線")
