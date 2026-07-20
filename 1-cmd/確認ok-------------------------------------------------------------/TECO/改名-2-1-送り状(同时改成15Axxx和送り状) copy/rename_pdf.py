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


ocr = RapidOCR()



# =========================
# PDF读取
# =========================

def get_pdf_text(pdf):

    text = ""


    with fitz.open(pdf) as doc:


        for page in doc:

            text += page.get_text()


        if not text.strip():


            for page in doc:


                pix = page.get_pixmap(
                    matrix=fitz.Matrix(3,3),
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



# =========================
# 批量处理
# =========================

success = 0


for pdf in pdf_folder.glob("*.pdf"):


    try:


        text = get_pdf_text(pdf)


        print("读取:", pdf.name)



        number_15A = None
        inquiry = None



        # =====================
        # 15A
        # 空格前停止
        # =====================

        m1 = re.search(
            r"(15A[A-Z0-9]+)",
            text
        )


        if m1:

            number_15A = m1.group()



        # =====================
        # お問い合わせ番号
        # =====================

        m2 = re.search(
            r"(4540[-－]\d{4}[-－]\d+|006[-－]\d{3}[-－]\d+)",
            text
        )


        if m2:

            inquiry = (
                m2.group()
                .replace(
                    "－",
                    "-"
                )
            )



        # =====================
        # 没有15A 不处理
        # =====================

        if not number_15A:

            print(
                "跳过(没有15A):",
                pdf.name
            )

            continue



        # =====================
        # 文件名
        # =====================

        if inquiry:


            new_name = (
                number_15A
                + " "
                + inquiry
                + ".pdf"
            )


        else:


            print(
                "跳过(没有お問い合わせ番号):",
                pdf.name
            )

            continue



        new_file = pdf.with_name(
            new_name
        )



        # =====================
        # 重名
        # =====================

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
            "完成:",
            pdf.name,
            "→",
            new_file.name
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