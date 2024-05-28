# -*- encoding: utf-8 -*-
"""基础文件"""

from pathlib import Path

# 当前绝对路径
P = Path(__file__).resolve().parent

# 语言文件文件夹
LANG_DIR = P / "lang"
LANG_DIR_FULL = LANG_DIR / "full"
LANG_DIR_VALID = LANG_DIR / "valid"

# 语言列表
language_list = [
    "en_us",
    "zh_cn",
    "zh_hk",
    "zh_tw",
    "lzh",
    "ja_jp",
    "ko_kr",
    "vi_vn",
]
