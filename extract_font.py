# -*- encoding: utf-8 -*-
"""字体子集生成器"""

import json
from pathlib import Path
from fontTools import subset

P = Path(__file__).resolve().parent

# 读取语言文件
with open(P / "lang" / "lzh.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# 提取字符串中包含的所有字符
all_char = {char for value in data.values() for char in str(value)}
all_char.discard("\n")  # 去除换行符

outpur_path = str(P / "static" / "fonts" / "I.Ming-8.00.subset.woff2")
args = [
    "I.Ming-8.00.ttf",
    f"--text={" ".join(all_char)}",
    f"--output-file={outpur_path}",
    "--flavor=woff2",
]

subset.main(args)
