import pandas as pd


# =========================
# 文件
# =========================

input_file = r"C:\c_wk\10_会社\PDF-相关\Test\download-.csv"


# =========================
# 自动识别编码
# =========================

ENCODINGS = [
    "utf-8-sig",
    "utf-8",
    "cp932",
    "shift_jis",
    "ms932",
    "euc_jp",
    "iso2022_jp",
    "gb18030",
    "gbk",
    "big5",
    "utf-16",
    "utf-16le",
    "utf-16be",
    "latin1"
]

df = None
used_encoding = None

for enc in ENCODINGS:

    try:

        df = pd.read_csv(
            input_file,
            dtype=str,
            keep_default_na=False,
            encoding=enc
        )

        used_encoding = enc

        print(f"读取成功：{enc}")

        break

    except Exception:

        pass

if df is None:

    raise Exception("无法读取文件，请确认文件是否真的是CSV。")


# =========================
# 删除文字
# =========================

REMOVE_WORDS = [
    "御中",
    "様"
]


def clean_text(text):

    if text is None:
        return ""

    text = str(text)

    for word in REMOVE_WORDS:
        text = text.replace(word, "")

    return text


# =========================
# 全表删除 御中 / 様
# =========================

for col in df.columns:

    df[col] = df[col].apply(clean_text)


# =========================
# 只处理注文No行
# =========================

if len(df.columns) >= 2:

    col_a = df.columns[0]
    col_b = df.columns[1]

    for idx in df.index:

        a = str(df.at[idx, col_a]).strip()
        b = str(df.at[idx, col_b]).strip()

        if "注文No" in a:

            merged = a + b

            if len(merged) > 16:

                if not merged.startswith("【超过16位】"):

                    merged = (
                        "【超过16位】"
                        + merged
                    )

            df.at[idx, col_b] = merged

            df.at[idx, col_a] = ""


# =========================
# 用原编码覆盖保存
# =========================

df.to_csv(
    input_file,
    index=False,
    encoding=used_encoding
)

print("================================")
print("处理完成")
print("文件已覆盖保存")
print(f"编码：{used_encoding}")
print("================================")