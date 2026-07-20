from playwright.sync_api import sync_playwright
from pathlib import Path


# =========================
# 设置
# =========================

URL = "https://www.xxxx"

USERNAME = "你的用户名"
PASSWORD = "你的密码"


# CSV保存位置
SAVE_FOLDER = Path(
    r"C:\c_wk\10_会社\PDF-相关\Test"
)


# =========================
# 自动登录 + 下载CSV
# =========================

with sync_playwright() as p:

    # 打开浏览器
    browser = p.chromium.launch(
        headless=False
    )


    context = browser.new_context(
        accept_downloads=True
    )


    page = context.new_page()


    # =========================
    # 打开登录页面
    # =========================

    page.goto(URL)

    print("打开登录页面")


    # =========================
    # 输入用户名
    # =========================

    page.fill(
        "#TextUserId",
        USERNAME
    )


    # =========================
    # 输入密码
    # =========================

    page.fill(
        "#TextPassword",
        PASSWORD
    )


    print("账号密码输入完成")


    # =========================
    # 点击登录
    # =========================

    page.click(
        "#BtnOk"
    )


    print("已经点击登录")


    # =========================
    # 等待登录完成
    # 等CSV按钮出现
    # =========================

    page.wait_for_selector(
        "#ImgBtnCsv",
        timeout=30000
    )


    print("登录成功，进入下载页面")


    print("当前URL:")
    print(page.url)



    # =========================
    # 下载CSV
    # =========================

    with page.expect_download() as download_info:

        page.click(
            "#ImgBtnCsv"
        )


    download = download_info.value


    # =========================
    # 保存文件
    # =========================

    SAVE_FOLDER.mkdir(
        exist_ok=True
    )


    save_file = SAVE_FOLDER / download.suggested_filename


    download.save_as(
        str(save_file)
    )


    print("======================")
    print("CSV下载完成")
    print(save_file)
    print("======================")


    # =========================
    # 保持浏览器
    # =========================

    input(
        "完成，按 Enter 关闭浏览器..."
    )


    browser.close()