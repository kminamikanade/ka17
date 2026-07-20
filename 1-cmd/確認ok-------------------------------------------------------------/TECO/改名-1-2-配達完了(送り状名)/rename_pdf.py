from pathlib import Path
import fitz
import re
import numpy as np
from rapidocr_onnxruntime import RapidOCR


pdf_folder = Path(
    r"C:\c_wk\10_会社\PDF-相关\Test\19"
)


ocr = RapidOCR()


def get_pdf_text(pdf):

    text = ""


    with fitz.open(pdf) as doc:

        for page in doc:

            pix = page.get_pixmap(
                matrix=fitz.Matrix(3, 3),
                alpha=False
            )


            img = np.frombuffer(
                pix.samples,
                dtype=np.uint8
            )


            img = img.reshape(
                pix.height,
                pix.width,
                3
            )


            result, _ = ocr(img)


            if result:

                for line in result:

                    text += line[1] + "\n"


    return text



success = 0


for pdf in pdf_folder.glob("*.pdf"):


    try:

        text = get_pdf_text(pdf)


        print("================")
        print(pdf.name)
        print(text)


        number = None
        date = None


        # 编号
        m = re.search(
            r"4540[-－]\d{4}[-－]\d+",
            text
        )


        if m:

            number = (
                m.group()
                .replace("－", "-")
            )


        # 日期
        d = re.search(
            r"(\d{1,2})月(\d{1,2})日",
            text
        )


        if d:

            date = (
                "2026"
                + d.group(1).zfill(2)
                + d.group(2).zfill(2)
            )


        if number:


            if date:

                new_name = (
                    number
                    + "("
                    + date
                    + ").pdf"
                )

            else:

                new_name = number + ".pdf"



            new_file = pdf.with_name(
                new_name
            )


            count = 2


            while new_file.exists():

                new_file = pdf.with_name(
                    new_name.replace(
                        ".pdf",
                        f"_{count}.pdf"
                    )
                )

                count += 1



            pdf.rename(new_file)


            success += 1


            print(
                "改名:",
                new_file.name
            )


        else:

            print(
                "没有找到编号"
            )


    except Exception as e:

        print(
            "错误:",
            pdf.name,
            e
        )



print("================")
print("完成:", success)

input("按 Enter 结束...")