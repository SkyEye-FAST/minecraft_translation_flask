# -*- encoding: utf-8 -*-
"""字体子集生成器"""

import json
from typing import Dict
from fontTools import subset

from app_base import P, LANG_DIR_VALID


def main() -> None:
    """主函数"""

    # 读取语言文件
    with open(LANG_DIR_VALID / "lzh.json", "r", encoding="utf-8") as file:
        data: Dict[str, str] = json.load(file)

    # 提取字符串中包含的所有字符
    all_char = {char for value in data.values() for char in str(value)}
    all_char.discard("\n")  # 去除换行符

    # 输出路径
    output_path = str(P / "static" / "fonts" / "I.Ming-8.10.subset.woff2")

    # 命令参数
    args = [
        str(P / "I.Ming-8.10.ttf"),
        f"--text=夏{"".join(all_char)}",
        f"--output-file={output_path}",
        "--flavor=woff2",
        "--no-subset-tables+=meta",
    ]

    # 生成字体子集文件
    subset.main(args)


if __name__ == "__main__":
    main()
