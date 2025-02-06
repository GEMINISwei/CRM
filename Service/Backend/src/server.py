# =====================================================================================================================
#                   Import
# =====================================================================================================================
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
    origins = [ENV_API_URL]
# Development 環境
elif ENV_MODE == "Development":
    app = FastAPI()
    origins = [f"{ENV_API_URL}:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
