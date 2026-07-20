from pathlib import Path
from PyPDF2 import PdfMerger
import re


# =========================
# 总文件夹
# =========================

root = Path(
    r"C:\c_wk\10_会社\PDF-相关\Test\19"
)


# 输出位置

output_folder = root


# =========================
# 收集PDF
# =========================

pdf_files = list(
    root.rglob("*.pdf")
)


groups = {}


for pdf in pdf_files:


    # 文件名里面找编号
    m = re.search(
        r"(4540-\d{4}-\d+)",
        pdf.stem
    )


    if m:

        number = m.group(1)

        if number not in groups:

            groups[number] = []


        groups[number].append(pdf)



# =========================
# 合并
# =========================

success = 0


for number, files in groups.items():


    # 只有一个的不处理
    if len(files) < 2:
        continue


    # 找带日期的文件名
    date_name = None


    for f in files:

        m = re.search(
            r"\(\d{8}\)",
            f.stem
        )

        if m:

            date_name = m.group()
            break



    if date_name:

        output_name = (
            number
            + date_name
            + ".pdf"
        )

    else:

        output_name = (
            number
            + ".pdf"
        )


    output = output_folder / output_name



    merger = PdfMerger()


    for f in files:

        print(
            "合并:",
            f
        )

        merger.append(f)



    merger.write(output)

    merger.close()


    success += 1


    print(
        "完成:",
        output.name
    )



print()
print("================")
print(
    "完成:",
    success
)
print("================")


input("按 Enter 结束...")