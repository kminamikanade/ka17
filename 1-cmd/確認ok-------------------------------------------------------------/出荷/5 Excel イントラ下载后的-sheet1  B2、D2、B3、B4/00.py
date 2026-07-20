import xlwings as xw
from pathlib import Path
import shutil


# ================= 配置 =================








SourceFolder = Path(
    r"C:\c_wk\10_会社\PDF-相关\Test"
)

TargetFolder = Path(
    r"C:\c_wk\10_会社\PDF-相关\Test\异常文件"
)


SheetName = "51"


# D20判断
D20_Length = 16


# B2/D2/B3/B4判断
Check_Length = 18


# ======================================


print("开始处理...")


TargetFolder.mkdir(
    exist_ok=True
)


app = None


try:

    app = xw.App(
        visible=False,
        add_book=False
    )

    app.display_alerts = False


    files = list(
        SourceFolder.glob("*.xlsx")
    )


    print(
        "发现文件:",
        len(files)
    )



    for file in files:


        # 跳过Excel临时文件
        if file.name.startswith("~$"):
            continue


        # 跳过异常文件夹
        if TargetFolder in file.parents:
            continue


        print("================")
        print("处理:", file.name)


        wb = None

        move_flag = False


        try:


            wb = app.books.open(
                str(file)
            )


            if SheetName not in [
                s.name for s in wb.sheets
            ]:

                print(
                    "找不到Sheet:",
                    SheetName
                )

                continue



            ws = wb.sheets[SheetName]



            # =================================
            # 检查 B2 D2 B3 B4
            # =================================


            check_cells = [
                "B2",
                "D2",
                "B3",
                "B4"
            ]


            for addr in check_cells:


                value = ws.range(addr).value


                if value is not None:


                    text = str(value).strip()


                    print(
                        addr,
                        ":",
                        text,
                        "长度:",
                        len(text)
                    )


                    if len(text) > Check_Length:


                        print(
                            addr,
                            "超过18字符"
                        )


                        move_flag = True




            # =================================
            # 检查 D20
            # =================================


            d20_value = ws.range(
                "D20"
            ).value



            if d20_value:


                d20_text = str(
                    d20_value
                ).strip()


                print(
                    "D20:",
                    d20_text,
                    "长度:",
                    len(d20_text)
                )



                if len(d20_text) > D20_Length:


                    print(
                        "D20超过16，开始移动下面内容"
                    )



                    last_row = (
                        ws.used_range
                        .last_cell
                        .row
                    )


                    last_col = (
                        ws.used_range
                        .last_cell
                        .column
                    )



                    # ==========================
                    # 从下往上复制整行
                    # ==========================

                    for r in range(
                        last_row,
                        20,
                        -1
                    ):


                        source = ws.range(
                            (r, 1),
                            (r, last_col)
                        )


                        target = ws.range(
                            (r + 1, 1),
                            (r + 1, last_col)
                        )


                        source.copy(
                            target
                        )



                    # 清空D21
                    ws.range(
                        "D21"
                    ).clear_contents()



                    print(
                        "D21已清空"
                    )


                    move_flag = True




            # 保存

            wb.save()



        except Exception as e:


            print(
                "错误:",
                e
            )



        finally:


            if wb:

                wb.close()



        # =================================
        # 移动文件
        # =================================

        if move_flag:


            target = (
                TargetFolder /
                file.name
            )


            shutil.move(
                str(file),
                str(target)
            )


            print(
                "移动完成:",
                target.name
            )


        else:


            print(
                "正常文件"
            )



finally:


    if app:

        app.quit()



print("================")
print("全部处理完成")
print("================")


input(
    "按 Enter 结束..."
)