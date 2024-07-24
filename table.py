# -*- encoding: utf-8 -*-
"""生成表格"""

import csv

from app_base import P, language_list
from app_init import data


def main() -> None:
    """主函数"""

    with open(P / "static" / "table.tsv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        headers = ["key"] + language_list
        writer.writerow(headers)
        for key in data["en_us"]:
            line = [key]
            for lang_data in data.values():
                value = lang_data.get(key, "？")
                line.append(value)
            writer.writerow(line)


if __name__ == "__main__":
    main()
