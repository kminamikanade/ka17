#获取送り状 或者 控 的 15xxx 并命名为 15AFGxxxxxx

from pathlib import Path
import fitz
from rapidocr_onnxruntime import RapidOCR
import re
import numpy as np


# =========================
# 设置
# =========================

input_folder = Path(
    r"C:\c_wk\10_会社\PDF-相关\test18"
)


ocr = RapidOCR()


success = 0
skip = 0



# =========================
# 扫描PDF
# =========================

for pdf_file in input_folder.rglob("*.pdf"):

    try:

        doc = fitz.open(pdf_file)

        # 只读取第一页
        page = doc[0]


        pix = page.get_pixmap(
            matrix=fitz.Matrix(3, 3)
        )


        img = np.frombuffer(
            pix.samples,
            dtype=np.uint8
        )


        img = img.reshape(
            pix.height,
            pix.width,
            pix.n
        )


        result, _ = ocr(img)


        text = ""


        if result:

            for line in result:

                text += line[1]



        doc.close()



        # =========================
        # OCR文字整理
        # =========================

        text_clean = text.upper()


        text_clean = (
            text_clean
            .replace("Ｏ", "O")
            .replace("０", "0")
            .replace("Ｉ", "I")
            .replace(" ", "")
        )


        text_clean = re.sub(
            r"\s+",
            "",
            text_clean
        )



        print()
        print("====================")
        print("文件:", pdf_file.name)
        print(text_clean)
        print("====================")



        # =========================
        # 搜索15A编号
        # =========================

        # =========================
        # 搜索15A编号
        # =========================

        code_match = re.search(
            r"15A[A-Z0-9]+",
            text_clean,
            re.IGNORECASE
        )

        code = None

        if code_match:
            code = code_match.group(0).upper()

            # 只保留前 11 位（例如 15AFG32452）
            code = re.match(r"15A[A-Z0-9]{0,8}", code).group(0)



        print(
            "15A编号:",
            code if code else "没有"
        )



        # =========================
        # 没找到跳过
        # =========================

        if not code:

            print(
                "没有15A编号，跳过:",
                pdf_file.name
            )

            skip += 1
            continue



        # =========================
        # 新文件名
        # =========================

        new_name = code + ".pdf"


        new_file = (
            pdf_file.parent
            /
            new_name
        )



        # 防止覆盖

        if new_file.exists():

            print(
                "已存在:",
                new_name
            )

            skip += 1
            continue



        # =========================
        # 改名
        # =========================

        pdf_file.rename(
            new_file
        )


        success += 1


        print(
            "完成改名:",
            new_name
        )



    except Exception as e:

        skip += 1

        print(
            "错误:",
            pdf_file.name,
            e
        )



print()
print("===================")
print("完成数量:", success)
print("未识别:", skip)
print("===================")


input("按 Enter 结束...")