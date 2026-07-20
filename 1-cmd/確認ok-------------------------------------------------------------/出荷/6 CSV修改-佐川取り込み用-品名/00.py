import pandas as pd


# =========================
# 文件路径
# =========================

excel_file = r"C:\c_wk\10_会社\PDF-相关\Test\test.xlsx"
csv_file = r"C:\c_wk\10_会社\PDF-相关\Test\download-.csv"


# =========================
# 自动尝试编码
# =========================

ENCODINGS = [
    "utf-8-sig",
    "utf-8",
    "cp932",
    "shift_jis",
    "ms932",
    "euc_jp",
    "utf-16",
    "utf-16le",
    "utf-16be",
    "gb18030",
    "gbk",
    "big5",
    "latin1"
]

df = None
used_encoding = None

for enc in ENCODINGS:

    try:
        df = pd.read_csv(
            csv_file,
            dtype=str,
            keep_default_na=False,
            encoding=enc
        )

        used_encoding = enc
        print(f"CSV读取成功：{enc}")
        break

    except Exception:
        pass

if df is None:
    raise Exception("CSV读取失败")


# =========================
# 删除 御中 / 様
# =========================

REMOVE_WORDS = [
    "御中",
    "様"
]

for col in df.columns:

    df[col] = df[col].astype(str)

    for word in REMOVE_WORDS:

        df[col] = df[col].str.replace(
            word,
            "",
            regex=False
        )


# =========================
# A列 + B列 → B列
# 只处理 注文No
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
# Excel读取
# =========================

master_df = pd.read_excel(
    excel_file,
    dtype=str
).fillna("")


# =========================
# Excel B列 -> E列
# =========================

master_dict = {}

for _, row in master_df.iterrows():

    if len(row) < 5:
        continue

    key = str(row.iloc[1]).strip()      # B列
    value = str(row.iloc[4]).strip()    # E列

    if key:
        master_dict[key] = value


# =========================
# CSV D列 -> G列
# =========================

if len(df.columns) >= 7:

    col_d = df.columns[3]   # D列
    col_g = df.columns[6]   # G列

    for idx in df.index:

        d_value = str(
            df.at[idx, col_d]
        ).strip()

        if not d_value:
            continue

        # 取第一个空格前面的内容
        key = d_value.split()[0]

        if key in master_dict:

            df.at[idx, col_g] = master_dict[key]


# =========================
# 保存（覆盖原文件）
# =========================

df.to_csv(
    csv_file,
    index=False,
    encoding=used_encoding
)

print("================================")
print("处理完成")
print("覆盖保存：")
print(csv_file)
print("编码：", used_encoding)
print("================================")