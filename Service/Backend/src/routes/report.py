import openpyxl

# 建立一個 Excel
workbook = openpyxl.Workbook()

# 建立一個頁籤
sheet_0 = workbook.worksheets[0]
sheet_0.title = "Test 1"

sheet_1 = workbook.create_sheet("Test 2")

workbook.save("TTT.xlsx")
