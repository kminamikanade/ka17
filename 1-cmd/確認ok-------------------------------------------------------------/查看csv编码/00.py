import pandas as pd
import chardet


# =========================
# 文件
# =========================

csv_file = r"C:\c_wk\10_会社\PDF-相关\Test\download.csv"


# =========================
# 检测编码
# =========================

with open(csv_file, "rb") as f:
    raw_data = f.read()

result = chardet.detect(raw_data)

print("检测结果：")
print(result)

encoding = result["encoding"]

print(f"\n使用编码：{encoding}")


# =========================
# 读取CSV
# =========================

try:

    df = pd.read_csv(
        csv_file,
        dtype=str,
        encoding=encoding
    )

    print("\n读取成功")
    print(df.head())

except Exception as e:

    print("\n读取失败")
    print(e)