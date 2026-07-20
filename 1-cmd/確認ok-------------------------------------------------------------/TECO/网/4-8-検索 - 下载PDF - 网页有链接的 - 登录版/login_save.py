import os
from playwright.sync_api import sync_playwright

# ================= 設定エリア =================
# ログインが必要な対象ページのURL
TARGET_URL = "https://mail.google.com/mail/u/2/#inbox"
# ログイン状態を保存するファイル名
AUTH_FILE = "auth_state.json"
# ============================================

def run():
    print("=" * 60)
    print("  🔐 ログイン状態保存ツール")
    print("=" * 60)
    print("1. ブラウザが起動します。")
    print("2. 表示されたページで、手動でアカウントとパスワードを入力してログインしてください。")
    print("3. ログインが完了し、目的のページが表示されたら、")
    print("   このコンソール画面に戻ってEnterキーを押してください。")
    print("=" * 60)

    with sync_playwright() as p:
        # ブラウザを起動（画面を表示する）
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # 対象ページへアクセス
        print(f"\n 対象ページを開いています: {TARGET_URL}")
        page.goto(TARGET_URL)
        page.wait_for_load_state("networkidle")

        # ーザーの操作を待つ
        input("\n👉 ログイン操作が完了したら、Enterキーを押してください...")

        # ログイン状態（CookieやLocalStorage）をJSONファイルに保存
        context.storage_state(path=AUTH_FILE)
        print(f"\n✅ 成功！ログイン状態が '{AUTH_FILE}' に保存されました。")
        print("   これ以降、ダウンロードスクリプトはこのファイルを読み込んで自動ログインします。")

        browser.close()
        print("\nブラウザを閉じました。")

if __name__ == "__main__":
    run()
    input("\n処理が完了しました。Enterキーを押して終了します...")