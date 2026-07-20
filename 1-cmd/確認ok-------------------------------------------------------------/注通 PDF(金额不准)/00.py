from pathlib import Path
import fitz
import re
from rapidocr_onnxruntime import RapidOCR


# =========================
# 设置
# =========================

PDF_FOLDER = Path(
    r"C:\c_wk\10_会社\PDF-相关\Test\PDF注通"
)


# 检查文字
CHECK_WORDS = [
    "人工"
    "国外",
    "2025年",
    "関東サービス",
    "作業",
    "交換作業",
    "派遣"
]


# 金额限制
LIMIT_AMOUNT = 3000000


ocr = RapidOCR()



# =========================
# 获取第一页文字
# =========================

def get_first_page_text(pdf_path):

    doc = fitz.open(pdf_path)

    page = doc[0]


    # 先读取PDF文字
    text = page.get_text()


    # 扫描PDF -> OCR
    if len(text.strip()) < 20:


        pix = page.get_pixmap(
            dpi=300
        )


        img_bytes = pix.tobytes("png")


        result, _ = ocr(img_bytes)


        text = ""


        if result:

            for item in result:

                text += item[1] + "\n"


    doc.close()


    return text



# =========================
# 查找关键词
# =========================

def find_words(text):

    result = []


    for word in CHECK_WORDS:

        if word in text:

            result.append(word)


    return result



# =========================
# 查找100万以上金额
# =========================

def find_money(text):

    result = []


    # OCR文字整理
    text = (
        text
        .replace("，", ",")
        .replace("￥", "")
        .replace("¥", "")
    )


    # 查找金额
    numbers = re.findall(
        r'\d[\d,]{6,}',
        text
    )


    for n in numbers:


        value = int(
            n.replace(",", "")
        )


        if value >= LIMIT_AMOUNT:

            result.append(value)



    # 去重复
    return list(set(result))



# =========================
# 主处理
# =========================

pdf_count = 0
find_count = 0


for pdf in PDF_FOLDER.rglob("*.pdf"):


    pdf_count += 1


    text = get_first_page_text(pdf)


    words = find_words(text)


    money = find_money(text)



    if words or money:


        find_count += 1


        print()
        print("====================")
        print("文件：", pdf.name)


        if words:

            print(
                "包含：",
                "、".join(words)
            )


        if money:

            print(
                "金额：",
                "、".join(
                    f"{m:,}円"
                    for m in money
                )
            )


        print("====================")



print()
print("--------------------")
print("PDF数量:", pdf_count)
print("发现数量:", find_count)
print("检查完成")