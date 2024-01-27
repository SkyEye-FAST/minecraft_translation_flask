# -*- encoding: utf-8 -*-
"""基础文件"""

import re
import json
import sys
import tomllib as tl
from pathlib import Path

# 当前绝对路径
P = Path(__file__).resolve().parent

# 加载配置
CONFIG_DIR = P / "configuration.toml"
if not CONFIG_DIR.exists():
    print("\n无法找到配置文件，请将配置文件放置在与此脚本同级的目录下。")
    sys.exit()
with open(CONFIG_DIR, "rb") as f:
    config = tl.load(f)

LANG_DIR = P / config["language_folder"]
IGNORE_SUPPLEMENTS = config["ignore_supplements"]

# 读取语言文件
print("开始读取语言文件。")
file_list = [
    "en_us.json",
    "zh_cn.json",
    "zh_hk.json",
    "zh_tw.json",
    "lzh.json",
]
data = {}
for file in file_list:
    with open(LANG_DIR / file, "r", encoding="utf-8") as f:
        data[file.split(".", maxsplit=1)[0]] = json.load(f)

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
