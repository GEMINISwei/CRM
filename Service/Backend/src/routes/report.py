# =====================================================================================================================
#                   Import
# =====================================================================================================================
from fastapi import Request
from fastapi.responses import StreamingResponse

from router import BaseRouter
from excel import BaseExcel


# =====================================================================================================================
#                   Variable
# =====================================================================================================================
router = BaseRouter()


# =====================================================================================================================
#                   Report Router
# =====================================================================================================================
@router.set_route(method="get", url="/reports/download-excel")
async def download_excel(
    request: Request
):
    excel = BaseExcel()

    # Create Sheet #1
    excel.add_worksheet("金吉利銀行")
    sheet1_fields = [
        "日期", "人員", "轉入幣", "轉出老幣", "轉出包幣",
        "玩家暱稱", "轉出現金", "轉入現金", "遊戲名", "交流方式",
        "使用帳號", "手續"
    ]
    for field in sheet1_fields:
        excel.add_style_field(field)

    for _ in range(5):
        excel.add_row_data(
            info=[
                "1月1日", "文", 0, 130000, 0, "小明", 0, 1000, "老子", "玉山", "(老)金仔", 1950
            ],
            style={
                "bg_color": "FFBB77"
            }
        )

    for _ in range(5):
        excel.add_row_data(
            info=[
                "1月1日", "文", 140000, 0, 0, "小明", 1000, 0, "老子", "玉山", "(老)金仔", 0
            ],
            style={
                "bg_color": "84C1FF"
            }
        )

    excel.add_spare_row()

    excel.add_row_data(
        info=[
            "1月2日", "文", 0, 130000, 0, "小明", 0, 1000, "老子", "玉山", "(老)金仔", 1950
        ],
        style={
            "bg_color": "FFBB77"
        }
    )

    for _ in range(3):
        excel.add_row_data(
            info=[
                "1月2日", "文", 140000, 0, 0, "小明", 1000, 0, "老子", "玉山", "(老)金仔", 0
            ],
            style={
                "bg_color": "84C1FF"
            }
        )

    excel.add_worksheet("郵局")
    excel.add_worksheet("9188 超商")
    excel.add_worksheet("虛擬帳號")

    return StreamingResponse(
        excel.steam,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename="download.xlsx"'}
    )
