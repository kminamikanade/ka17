from playwright.sync_api import sync_playwright

DOWNLOAD_PATH = r"C:\c_wk\10_会社\PDF-相关\Test\loginTest"

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    page = browser.new_page(
        accept_downloads=True
    )
URL = "https://www.enavi-ts.net/ts-staff/login.aspx?ID=wzhW9wHef&AspxAutoDetectCookieSupport=1&type=pc1973"
12001411
    # 打开登录页面
    page.goto("https://www.enavi-ts.net/ts-staff/login.aspx?ID=wzhW9wHef&AspxAutoDetectCookieSupport=1&type=pc1973")

    # 输入账号
    page.fill("用户名输入框", "你的用户名")

    # 输入密码
    page.fill("密码输入框", "你的密码")

    # 点击登录
    page.click("登录按钮")

    # 等待登录完成
    page.wait_for_timeout(5000)


    # 进入下载页面
    page.goto("下载页面地址")


    # 点击下载
    with page.expect_download() as download_info:
        page.click("PDF下载按钮")

    download = download_info.value

    # 保存
    download.save_as(
        DOWNLOAD_PATH + "\\" + download.suggested_filename
    )


    print("下载完成")

    browser.close()