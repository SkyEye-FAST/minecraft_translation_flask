# -*- encoding: utf-8 -*-
"""初始化文件"""

import json
from base import LANG_DIR, LANG_DIR_VALID, language_list

# 是否忽略补充字符串
IGNORE_SUPPLEMENTS = True

# 读取语言文件
data = {}
for lang_name in language_list:
    with open(LANG_DIR_VALID / f"{lang_name}.json", "r", encoding="utf-8") as f:
        data[lang_name] = json.load(f)

# 读取补充字符串
if not IGNORE_SUPPLEMENTS:
    language_list.remove("en_us")
    with open(LANG_DIR / "supplements.json", "r", encoding="utf-8") as f:
        supplements = json.load(f)
    for lang in language_list:
        data[lang].update(supplements[lang])
    print(f"已补充{len(supplements['zh_cn'])}条字符串。")


def get_translation(query_str: str):
    """在语言文件中匹配含有输入内容的源字符串"""
    translation = {}
    for k, v in data["en_us"].items():
        if query_str.lower() in v.lower():
            element = {lang: content.get(k, "？") for lang, content in data.items()}
            translation[k] = element
    return translation
