# -*- encoding: utf-8 -*-
"""初始化文件"""

import json
from typing import Dict

from app_base import LANG_DIR, LANG_DIR_VALID, ID_MAP_PATH, language_list

# 是否忽略补充字符串
IGNORE_SUPPLEMENTS: bool = True

# 读取语言文件
data: Dict[str, Dict[str, str]] = {}
for lang_name in language_list:
    with open(LANG_DIR_VALID / f"{lang_name}.json", "r", encoding="utf-8") as f:
        data[lang_name] = json.load(f)

# 读取ID映射
with open(ID_MAP_PATH, "r", encoding="utf-8") as f:
    id_map = json.load(f)

# 读取补充字符串
if not IGNORE_SUPPLEMENTS:
    language_list.remove("en_us")
    with open(LANG_DIR / "supplements.json", "r", encoding="utf-8") as f:
        supplements: Dict[str, Dict[str, str]] = json.load(f)
    for lang in language_list:
        data[lang].update(supplements[lang])
    print(f"已补充{len(supplements['zh_cn'])}条字符串。")


def get_translation(
    query_str: str, query_lang: str = "en_us"
) -> Dict[str, Dict[str, str]]:
    """
    在语言文件中匹配含有输入内容的源字符串。

    Args:
        query_str (str): 查询的字符串。

    Returns:
        Dict[str, Dict[str, str]]: 匹配的翻译结果字典。
    """

    translation: Dict[str, Dict[str, str]] = {}
    if query_lang == "key":
        for k in data["en_us"]:
            if query_str.lower() in k:
                element = {lang: content.get(k, "？") for lang, content in data.items()}
                translation[k] = element
    else:
        for k, v in data[query_lang].items():
            if query_str.lower() in v.lower():
                element = {lang: content.get(k, "？") for lang, content in data.items()}
                translation[k] = element
    return translation
