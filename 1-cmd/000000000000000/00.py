from pathlib import Path
import pandas as pd
import chardet

print("测试版本")

csv_folder = Path(
    r"C:\c_wk\10_会社\PDF-相关\Test\Test19"
)

success = 0

for csv_file in csv_folder.glob("*.csv"):

    try:

        # 自动检测编码（读取全部内容以提高准确率）
        with open(csv_file, "rb") as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)

        enc = result["encoding"]
        confidence = result["confidence"]

        # ★ 关键修改：如果检测不到编码，回退到 shift_jis
        if enc is None or confidence < 0.5:
            enc = "shift_jis"
            print(f"检测编码: 失败 → 回退使用 {enc}")
        else:
            print(f"检测编码: {enc} (置信度: {confidence})")

        df = pd.read_csv(
            csv_file,
            dtype=str,
            encoding=enc
        )

        # G列 + H列 → H列
        df.iloc[:, 7] = (
            df.iloc[:, 6].fillna("")
            +
            df.iloc[:, 7].fillna("")
        )

        # G列清空
        df.iloc[:, 6] = ""

        df.to_csv(
            csv_file,
            index=False,
            encoding=enc
        )

        success += 1
        print("完成:", csv_file.name)

    except Exception as e:
        print("错误:", csv_file.name, e)

print()
print("===================")
print("完成:", success)
print("===================")

input("按 Enter 结束...")