from pathlib import Path
import os


# =========================
# PDF总文件夹
# =========================

root = Path(
    r"C:\c_wk\10_会社\PDF-相关\Test\19"
)


# =========================
# 输出TXT
# =========================

output = Path(
    r"C:\c_wk\10_会社\PDF-相关\PDF文件名单.txt"
)



names = []


# =========================
# 扫描PDF文件
# =========================

for pdf in root.rglob("*.pdf"):


    # 去掉 .pdf

    name = pdf.stem


    # 遇到括号停止
    name = name.split("(")[0]


    # 去除前后空格

    name = name.strip()


    if name:

        names.append(name)



# =========================
# 去重复排序
# =========================

names = sorted(
    set(names)
)



# =========================
# 写入TXT
# =========================

with open(
    output,
    "w",
    encoding="utf-8"
) as f:


    for name in names:

        f.write(
            name
            +
            "\n"
        )



print(
    "完成:",
    len(names),
    "个"
)


print(
    "保存:",
    output
)



# =========================
# 自动打开记事本
# =========================

os.startfile(
    output
)


input("按 Enter 结束...")