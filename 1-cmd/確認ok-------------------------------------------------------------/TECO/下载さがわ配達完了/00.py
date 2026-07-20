from pypdf import PdfReader, PdfWriter
from pathlib import Path
import openpyxl
from playwright.sync_api import sync_playwright
import re
import datetime
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

wb = openpyxl.load_workbook(
    ExcelFile
)

ws = wb.active


numbers = []


for row in ws.iter_rows(
    min_col=1,
    values_only=True
):

    if row[0]:

        # 原号码（保存文件名用）
        original_no = str(row[0]).strip()


        # 输入网页用
        input_no = (
            original_no
            .replace("-", "")
            .strip()
        )


        numbers.append(
            (
                original_no,
                input_no
            )
        )


print(
    "查询数量:",
    len(numbers)
)



# =========================
# 浏览器
# =========================

with sync_playwright() as p:


    browser = p.chromium.launch(
        headless=False
    )


    page = browser.new_page()



    for original_no, input_no in numbers:


        print("================")
        print("查询:", original_no)
        print("================")



        # 打开佐川页面

        page.goto(URL)

        page.wait_for_timeout(3000)



        # =====================
        # 输入号码
        # =====================

        page.wait_for_selector(
            "input[type='text']",
            timeout=10000
        )


        page.locator(
            "input[type='text']"
        ).first.fill(input_no)



        # =====================
        # 查询
        # =====================

        page.locator(
            "input[type='submit']"
        ).last.click()



        # 等待结果

        page.wait_for_timeout(5000)



        # =====================
        # 获取网页文字
        # =====================

        text = page.locator(
            "body"
        ).inner_text()



        # =====================
        # 抓取配達完了日
        # =====================

        match = re.search(
            r"配達完了日\s*[：:]\s*(\d+)月(\d+)日",
            text
        )


        if match:


            month = match.group(1).zfill(2)

            day = match.group(2).zfill(2)


            year = str(
                datetime.datetime.now().year
            )


            finish_date = (
                year +
                month +
                day
            )


        else:

            finish_date = "日付なし"



        print(
            "配達完了日:",
            finish_date
        )



        # =====================
        # 保存PDF
        # =====================

        pdf_name = (
            f"{original_no}"
            f"({finish_date})"
            f".pdf"
        )


        pdf_path = (
            SaveFolder /
            pdf_name
        )



        page.pdf(
            path=str(pdf_path),
            format="A4",
            print_background=True
        )


        # =====================
        # 只保留PDF第一页
        # =====================

        reader = PdfReader(str(pdf_path))

        if len(reader.pages) > 1:

            writer = PdfWriter()

            writer.add_page(
                reader.pages[0]
            )


            temp_pdf = pdf_path.with_name(
                pdf_path.stem + "_temp.pdf"
            )


            with open(
                temp_pdf,
                "wb"
            ) as f:
                writer.write(f)


            # 删除原2页PDF
            pdf_path.unlink()


            # 改回原文件名
            temp_pdf.rename(pdf_path)


            print("第一页保留完成")


        print(
            "保存:",
            pdf_path
        )


        time.sleep(2)



    browser.close()



print("================")
print("全部完成")
print("================")