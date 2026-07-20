from pathlib import Path
import fitz
import re
import numpy as np
from rapidocr_onnxruntime import RapidOCR


# =========================
# PDF文件夹
# =========================

pdf_folder = Path(
    r"C:\c_wk\10_会社\PDF-相关\Test\19"
)


# =========================
# OCR
# =========================

ocr = RapidOCR()


# =========================
# 读取PDF文字
# =========================

def get_pdf_text(pdf):

    doc = fitz.open(pdf)

    text = ""

    # 先读取PDF文字层
    for page in doc:
        text += page.get_text()


    # 没有文字 -> OCR
    if not text.strip():

        for page in doc:

            pix = page.get_pixmap(
                matrix=fitz.Matrix(2, 2)
            )

            img = np.frombuffer(
                pix.samples,
                dtype=np.uint8
            )


            if pix.n == 4:

                img = img.reshape(
                    pix.height,
                    pix.width,
                    4
                )

                img = img[:, :, :3]

            else:

                img = img.reshape(
                    pix.height,
                    pix.width,
                    pix.n
                )


            result, _ = ocr(img)


            if result:

                for line in result:
                    text += line[1]


    return text



# =========================
# 批量处理
# =========================

success = 0


for pdf in pdf_folder.glob("*.pdf"):

    try:

        text = get_pdf_text(pdf)

        print("读取:", pdf.name)
        print("内容:", text)


        number = None


        # 查找编号
        m = re.search(
            r"(4540[-－]\d{4}[-－]\d+|006[-－]\d{3}[-－]\d+)",
            text
        )


        if m:

            number = m.group()

            # 全角横杠转换
            number = number.replace(
                "－",
                "-"
            )

            # 空格后内容不要
            number = re.split(
                r"[\s　]+",
                number
            )[0]


        if number:


            new_file = pdf.with_name(
                number + ".pdf"
            )


            if new_file.exists():

                print(
                    "已存在:",
                    new_file.name
                )


            else:

                pdf.rename(new_file)

                success += 1

                print(
                    "完成:",
                    pdf.name,
                    "→",
                    new_file.name
                )


        else:

            print(
                "未找到:",
                pdf.name
            )


    except Exception as e:

        print(
            "错误:",
            pdf.name,
            e
        )


print()
print("===================")
print("完成:", success)
print("===================")

input("按 Enter 结束...")