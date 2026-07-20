from pathlib import Path
import openpyxl
from playwright.sync_api import sync_playwright
import time


# =========================
# 设置
# =========================

ExcelFile = r"C:\c_wk\10_会社\PDF-相关\Test\code.xlsx"

SaveFolder = Path(
    r"C:\c_wk\10_会社\PDF-相关\Test\codePDF"
)

SaveFolder.mkdir(exist_ok=True)


URL = (
    "https://k2k.sagawa-exp.co.jp/"
    "p/sagawa/web/okurijoinput.jsp"
)


# =========================
# 读取Excel号码
# =========================

wb = openpyxl.load_workbook(ExcelFile)

ws = wb.active

numbers = []

for row in ws.iter_rows(min_col=1, values_only=True):

    if row[0]:

        no = str(row[0]).replace("-", "").strip()

        numbers.append(no)


print("查询数量:", len(numbers))


# =========================
# Edge浏览器
# =========================

with sync_playwright() as p:

    browser = p.chromium.launch(
        channel="msedge",
        headless=False
    )


    page = browser.new_page()


    for no in numbers:

        print("----------------")
        print("查询:", no)


        # 打开佐川输入页面

        page.goto(URL)

        page.wait_for_timeout(3000)


        # =========================
        # 输入号码
        # =========================

        page.wait_for_selector(
            "input[type='text']",
            timeout=10000
        )


        page.locator(
            "input[type='text']"
        ).first.fill(no)



        # =========================
        # 点击查询
        # =========================

        page.locator(
            "input[type='submit']"
        ).last.click()



        # 等待查询结果

        page.wait_for_timeout(5000)



        # =========================
        # 保存PDF
        # =========================

        pdf_path = SaveFolder / f"{no}.pdf"


        page.pdf(
            path=str(pdf_path),
            format="A4",
            print_background=True
        )


        print(
            "保存完成:",
            pdf_path
        )


    browser.close()


print("================")
print("全部完成")
print("================")