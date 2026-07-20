import os
import re
import time
import requests
from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright

# ================= 設定エリア =================
# 検索結果ページのURL
TARGET_URL = "https://mail.google.com/mail/u/2/#inbox"
# ファイルの保存先フォルダ
SAVE_DIR = r"C:\Work\下载文件"
# 保存したログイン状態ファイル
AUTH_FILE = "auth_state.json"
# 最大ダウンロード数（テスト用）
MAX_DOWNLOADS = 20
# ============================================

# 保存フォルダが存在しない場合は作成
os.makedirs(SAVE_DIR, exist_ok=True)

def sanitize_filename(name):
    """Windowsのファイル名として不正な文字を削除・置換する"""
    # 不正な文字を削除
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', name)
    # 先頭と末尾のスペースを削除し、内部のスペースをアンダースコアに置換
    name = name.strip().replace(' ', '_').replace('\u3000', '_')
    if not name:
        return "unnamed"
    # ファイル名の長さを制限（最大60文字）
    return name[:60]

def get_safe_filename(base_name, used_names):
    """重複を防ぐための最終ファイル名を生成する"""
    safe = sanitize_filename(base_name)
    if safe not in used_names:
        used_names.add(safe)
        return safe
    
    # 同名ファイルがある場合は末尾に連番を付与
    counter = 1
    while f"{safe}_{counter}" in used_names:
        counter += 1
    final = f"{safe}_{counter}"
    used_names.add(final)
    return final

def extract_title_from_page(page):
    """ページの見出し（タイトル）を抽出する"""
    # 優先順位の高いセレクターから順に検索
    for selector in ["h1", "title", ".page-title", ".article-title", "meta[property='og:title']"]:
        el = page.query_selector(selector)
        if el:
            # metaタグの場合はcontent属性、それ以外はテキストを取得
            text = el.get_attribute("content") if el.tag_name() == "meta" else el.inner_text()
            if text and len(text.strip()) > 2:
                return text.strip()
    return None

def find_pdf_url(page, base_url):
    """ページ内に埋め込まれたPDFのURLを検索する"""
    # aタグのhrefに.pdfが含まれるものを探す
    links = page.query_selector_all("a[href*='.pdf']")
    for link in links:
        href = link.get_attribute("href")
        if href:
            return urljoin(base_url, href)
    
    # iframeやembedタグの場合
    embed = page.query_selector("embed[type='application/pdf'], iframe[src*='.pdf']")
    if embed:
        src = embed.get_attribute("src")
        if src:
            return urljoin(base_url, src)
    return None

def download_file(url, save_path):
    """requestsライブラリを使用してファイルを直接ダウンロードする"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        with open(save_path, "wb") as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"    ❌ ダウンロードエラー: {e}")
        return False

def run():
    # ログイン状態ファイルの存在チェック
    if not os.path.exists(AUTH_FILE):
        print(f"❌ エラー: ログイン状態ファイル '{AUTH_FILE}' が見つかりません。")
        print("   先に 'login_save.py' を実行してログイン状態を保存してください。")
        return

    downloaded_count = 0
    skipped_count = 0
    used_names = set()

    print("=" * 60)
    print("   PDF自動ダウンロードツール（ログイン対応版）")
    print("=" * 60)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        
        # 🔥 核心：保存したログイン状態（Cookie）を読み込んでブラウザを起動
        context = browser.new_context(storage_state=AUTH_FILE)
        page = context.new_page()

        print(f"\n🔐 ログイン状態を読み込みました。ページへアクセス中...")
        page.goto(SEARCH_URL)
        page.wait_for_load_state("networkidle")
        time.sleep(2)

        print("\n 検索結果の項目をスキャン中...")
        
        # ページ内のリンクを取得
        links = page.query_selector_all("a[href]")
        items = []
        for link in links:
            href = link.get_attribute("href")
            if href and href.startswith("http"):
                items.append({"element": link, "href": href})
        
        print(f"✅ {len(items)} 個のリンクを発見しました。\n")

        # 各リンクを処理
        for i, item in enumerate(list(items)[:MAX_DOWNLOADS], 1):
            href = item["href"]
            print(f"\n[{i}/{min(MAX_DOWNLOADS, len(items))}] 処理中: {href[:60]}...")

            try:
                # 詳細ページへ移動
                page.goto(href)
                page.wait_for_load_state("networkidle")
                time.sleep(1)

                # 1. ページのタイトル（ファイル名）を抽出
                original_name = extract_title_from_page(page)
                if original_name:
                    print(f"   名称抽出: {original_name}")
                else:
                    # タイトルが取れない場合はURLから生成
                    original_name = os.path.splitext(os.path.basename(urlparse(href).path))[0]
                    print(f"  📝 名称未取得 → URLベース: {original_name}")

                # 2. PDFの実体URLを検索
                pdf_url = find_pdf_url(page, href)
                if pdf_url:
                    print(f"  🔗 PDF発見: {pdf_url}")
                else:
                    print(f"  ❌ PDFリンクが見つかりませんでした")
                    continue

                # 3. 安全なファイル名を確定
                final_name = get_safe_filename(original_name, used_names)
                save_path = os.path.join(SAVE_DIR, f"{final_name}.pdf")

                # 4. ファイルをダウンロード
                print(f"  ⬇️ ダウンロード中: {final_name}.pdf")
                if download_file(pdf_url, save_path):
                    print(f"  ✅ 保存完了: {final_name}.pdf")
                    downloaded_count += 1
                else:
                    print(f"  ❌ 保存に失敗しました")

            except Exception as e:
                print(f"  ❌ 予期せぬエラー: {e}")

            time.sleep(0.5) # サーバーへの負荷を避けるため待機

        browser.close()

        print("\n" + "=" * 60)
        print("🎉 全ての処理が完了しました！")
        print("=" * 60)
        print(f"   ✅ 新規ダウンロード: {downloaded_count} 個")
        print(f"   ⏭️ スキップ（重複等）: {skipped_count} 個")
        print(f"   📁 保存先: {SAVE_DIR}")
        print("=" * 60)

if __name__ == "__main__":
    run()
    input("\n処理が完了しました。Enterキーを押して終了します...")