# -*- encoding: utf-8 -*-
"""基础文件"""

import re
import json
from pathlib import Path

# 当前绝对路径
P = Path(__file__).resolve().parent

# 语言文件文件夹
LANG_DIR = P / "lang"

# 是否忽略补充字符串
IGNORE_SUPPLEMENTS = True

# 读取语言文件
print("开始读取语言文件。")
data = {}
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
for lang_name in language_list:
    with open(LANG_DIR / f"{lang_name}.json", "r", encoding="utf-8") as f:
        data[lang_name] = json.load(f)
print("语言文件读取成功。")

# 读取补充字符串
if not IGNORE_SUPPLEMENTS:
    with open(LANG_DIR / "supplements.json", "r", encoding="utf-8") as f:
        supplements = json.load(f)
    for lang in ["zh_cn", "zh_hk", "zh_tw", "lzh"]:
        data[lang].update(supplements[lang])
    print(f"已补充{len(supplements['zh_cn'])}条字符串。")


def is_valid_key(translation_key: str):
    """判断是否为有效键名"""

    prefixes = (
        "block.",
        "item.minecraft.",
        "entity.minecraft.",
        "biome.",
        "effect.minecraft.",
        "enchantment.minecraft.",
        "trim_pattern.",
        "upgrade.",
    )

    if (
        translation_key.startswith(prefixes)
        and not re.match(
            r"(block\.minecraft\.|item\.minecraft\.|entity\.minecraft\.)[^.]*\.",
            translation_key,
        )
        and translation_key
        not in ["block.minecraft.set_spawn", "entity.minecraft.falling_block_type"]
        and "pottery_shard" not in translation_key
    ):
        return True

    # 匹配进度键名
    if re.match(r"advancements\.(.*)\.title", translation_key):
        return True

    return False


def get_translation(query_str: str):
    """在语言文件中匹配含有输入内容的源字符串"""
    translation = {}
    for k, v in data["en_us"].items():
        if query_str.lower() in v.lower():
            element = {lang: content.get(k, "？") for lang, content in data.items()}
            translation[k] = element
    return translation
