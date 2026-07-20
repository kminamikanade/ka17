import pandas as pd
import re


# =========================
# CSV文件
# =========================

csv_file = r"C:\c_wk\10_会社\PDF-相关\Test\input.csv"



# =========================
# 自动读取编码
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

        print("读取成功:", enc)

        break

    except Exception:
        pass


if df is None:

    raise Exception("CSV读取失败")



# =========================
# 确保有H列
# =========================

while len(df.columns) < 8:

    df[f"空列{len(df.columns)+1}"] = ""



# =========================
# 列
# =========================

col_a = df.columns[0]
col_b = df.columns[1]
col_d = df.columns[3]
col_e = df.columns[4]
col_h = df.columns[7]



# =========================
# A列数字每4位加-
# =========================

def add_dash_every_4(text):

    if text is None:
        return ""

    text = str(text).strip()


    # 科学计数法
    if re.fullmatch(
        r"\d+\.\d+E\+\d+",
        text,
        re.I
    ):
        try:
            text = str(int(float(text)))
        except:
            pass


    if re.fullmatch(r"\d+", text):

        return "-".join(
            text[i:i+4]
            for i in range(
                0,
                len(text),
                4
            )
        )


    return text



df[col_a] = df[col_a].apply(
    add_dash_every_4
)



# =========================
# 公司名处理
# =========================

def format_company(text):

    if text is None:
        return ""


    text = str(text).strip()


    # 删除全角空格后面的内容
    if "　" in text:

        text = text.split("　")[0]


    # 删除半角空格后面的内容
    if " " in text:

        text = text.split(" ")[-1]


    # 株式会社转换
    text = text.replace(
        "株式会社",
        "(株)"
    )


    return text



# =========================
# 处理B/E/H
# =========================

for idx in df.index:


    # D列保持原样
    d_value = str(
        df.at[idx, col_d]
    ).strip()



    # ---------------------
    # B列
    # ---------------------

    old_b = str(
        df.at[idx, col_b]
    ).strip()


    company = format_company(
        old_b
    )


    if d_value:

        df.at[idx, col_b] = (
            d_value
            + " "
            + company
        )

    else:

        df.at[idx, col_b] = company



    # ---------------------
    # E列
    # D列空格前
    # ---------------------

    if d_value:

        df.at[idx, col_e] = (
            d_value.split()[0]
        )

    else:

        df.at[idx, col_e] = ""



    # ---------------------
    # H列
    # 删除旧数据
    # 复制A列
    # ---------------------

    df.at[idx, col_h] = ""

    df.at[idx, col_h] = (
        df.at[idx, col_a]
    )



# =========================
# 覆盖保存
# =========================

df.to_csv(
    csv_file,
    index=False,
    encoding=used_encoding
)


print("====================")
print("完成")
print("文件:", csv_file)
print("编码:", used_encoding)
print("====================")