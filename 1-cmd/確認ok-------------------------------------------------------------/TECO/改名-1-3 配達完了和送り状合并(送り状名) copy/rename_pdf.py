from pathlib import Path
from PyPDF2 import PdfMerger
import re


root = Path(
    r"C:\c_wk\10_会社\PDF-相关\Test\19"
)


pdf_files = list(
    root.rglob("*.pdf")
)


okuri_files = []
delivery_files = []


for pdf in pdf_files:


    # 送り状
    if re.search(
        r"15A[A-Z0-9]+",
        pdf.stem
    ):

        okuri_files.append(pdf)



    # 配達完了
    elif re.search(
        r"\(\d{8}\)",
        pdf.stem
    ):

        delivery_files.append(pdf)



print("送り状:", len(okuri_files))
print("配達完了:", len(delivery_files))



success = 0



for delivery in delivery_files:


    # 配達完了から番号取得

    m = re.search(
        r"(4540-\d{4}-\d+|006-\d{3}-\d+)",
        delivery.stem
    )


    if not m:

        print(
            "编号なし:",
            delivery.name
        )

        continue



    number = m.group()



    # 找送り状

    okuri = None


    for f in okuri_files:


        if number in f.stem:

            okuri = f
            break



    if not okuri:

        print(
            "送り状未找到:",
            number
        )

        continue



    # 15A

    m15 = re.search(
        r"(15A[A-Z0-9]+)",
        okuri.stem
    )


    if not m15:

        continue



    name15 = m15.group()



    # 日期

    date = re.search(
        r"\d{8}",
        delivery.stem
    ).group()



    output = root / (
        name15
        + " ("
        + date
        + ").pdf"
    )



    merger = PdfMerger()


    # 送り状先

    merger.append(okuri)


    # 配達完了后

    merger.append(delivery)


    merger.write(output)

    merger.close()



    success += 1


    print(
        "完成:",
        output.name
    )



print()
print("================")
print("完成:", success)
print("================")


input("按 Enter 结束...")