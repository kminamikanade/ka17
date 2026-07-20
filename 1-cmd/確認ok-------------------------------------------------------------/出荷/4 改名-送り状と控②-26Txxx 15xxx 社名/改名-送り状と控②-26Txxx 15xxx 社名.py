#根据 15AFGxxxxxx 文件的改成イントラ中の名前


from pathlib import Path
import re


# =========================
# 多个文件夹 + 对应的新文件名
# =========================
tasks = [
    {
        "folder": Path(r"C:\c_wk\10_会社\PDF-相关\Test\PDF"),
        "new_names_text": """
        16GG033246 14AWE1240144-125478 公司①
        26T12345 14AWE1240145-125478 東京株式会社①
        """
    },
    {
        "folder": Path(r"C:\c_wk\10_会社\PDF-相关\Test2\PDF"),
        "new_names_text": """
        16GG033246 14AWE1240144-125478 公司②
        26T12345 14AWE1240145-125478 東京株式会社③
        """
    }
]


# =========================
# 提取编号函数
# =========================
def get_codes(text):
    codes = re.findall(r"\d+[A-Z]{1,5}\d+", text.upper())
    return [c for c in codes if len(c) >= 8]


# =========================
# 开始处理每个文件夹
# =========================
total_success = 0

for task in tasks:

    folder = task["folder"]
    new_names_text = task["new_names_text"]

    print(f"\n=== 处理文件夹: {folder} ===")

    if not folder.exists():
        print("文件夹不存在，跳过:", folder)
        continue

    # 整理新文件名
    new_names = []
    for line in new_names_text.splitlines():
        line = line.strip()
        if line:
            if not line.lower().endswith(".pdf"):
                line += ".pdf"
            new_names.append(line)

    # 建立新文件编号列表
    new_code_list = []
    for name in new_names:
        codes = get_codes(name)
        if codes:
            new_code_list.append((codes, name))

    # 开始重命名
    success = 0

    for old_file in folder.glob("*.pdf"):

        old_codes = get_codes(old_file.name)

        if not old_codes:
            print("跳过(无编号):", old_file.name)
            continue

        match_name = None

        for codes, new_name in new_code_list:
            if set(old_codes) & set(codes):
                match_name = new_name
                break

        if not match_name:
            print("未找到对应:", old_file.name)
            continue

        new_file = folder / match_name

        if old_file == new_file:
            continue

        try:
            old_file.rename(new_file)
            print("完成:", old_file.name, "→", match_name)
            success += 1
            total_success += 1
        except Exception as e:
            print("错误:", old_file.name, e)

    print("本文件夹完成数量:", success)


print("\n================")
print("全部文件夹总完成数量:", total_success)
print("================")

input("处理完成，按 Enter 结束...")
