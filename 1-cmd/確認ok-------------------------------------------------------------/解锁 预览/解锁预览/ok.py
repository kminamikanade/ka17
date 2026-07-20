from pathlib import Path
import os


# =========================
# 要处理的文件夹
# =========================

folders = [
    r"C:\c_wk\10_会社\PDF-相关\Test\PDF注通",
    r"C:\c_wk\10_会社\PDF-相关"
]


# =========================
# 开始处理
# =========================

count = 0


for folder in folders:

    folder_path = Path(folder)

    if not folder_path.exists():

        print("不存在:", folder)

        continue


    print("处理:", folder)


    for file in folder_path.rglob("*"):

        if file.is_file():

            try:

                # 删除 Zone.Identifier 信息
                # Windows 下载文件标记
                ads_file = str(file) + ":Zone.Identifier"

                if os.path.exists(ads_file):

                    os.remove(ads_file)

                    count += 1

                    print("解锁:", file.name)


            except Exception as e:

                print(
                    "错误:",
                    file,
                    e
                )


print()
print("===================")
print("解锁完成:", count)
print("===================")


input("按 Enter 结束...")