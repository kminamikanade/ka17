from pathlib import Path
import time
import openpyxl

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


# =========================
# Excel
# =========================

excel_file = Path(
    r"C:\c_wk\10_会社\佐川番号.xlsx"
)


# =========================
# PDF保存位置
# =========================

save_folder = Path(
    r"C:\c_wk\10_会社\佐川PDF"
)

save_folder.mkdir(
    exist_ok=True
)


# =========================
# 读取Excel
# =========================

wb = openpyxl.load_workbook(
    excel_file
)

ws = wb.active


numbers = []

for row in ws.iter_rows(
    min_col=1,
    values_only=True
):

    if row[0]:

        numbers.append(
            str(row[0])
        )


print(
    "号码数量:",
    len(numbers)
)


# =========================
# Chrome设置
# =========================

options = Options()

options.add_argument(
    "--start-maximized"
)


driver = webdriver.Chrome(
    options=options
)


# =========================
# 查询
# =========================

for number in numbers:


    try:

        print(
            "查询:",
            number
        )


        driver.get(
            "https://k2k.sagawa-exp.co.jp/p/sagawa/web/okurijosearcheng.jsp"
        )


        time.sleep(3)


        # 这里填写输入框
        # （佐川网页如果改版，需要调整ID）

        textbox = driver.find_element(
            By.NAME,
            "okurijoNo"
        )


        textbox.send_keys(
            number
        )


        button = driver.find_element(
            By.NAME,
            "search"
        )


        button.click()


        time.sleep(5)



        # 后续这里调用浏览器打印PDF


        print(
            "完成:",
            number
        )



    except Exception as e:

        print(
            "错误:",
            number,
            e
        )



driver.quit()


print("全部完成")

input("按 Enter结束...")