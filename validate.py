# -*- encoding: utf-8 -*-
"""验证并提取语言文件"""

import re
import json
from base import LANG_DIR_FULL, LANG_DIR_VALID, language_list


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


# 文件夹
LANG_DIR_VALID.mkdir(exist_ok=True)

# 修改语言文件
for lang_name in language_list:
    with open(LANG_DIR_FULL / f"{lang_name}.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    edited_data = {k: v for k, v in data.items() if is_valid_key(k)}
    with open(LANG_DIR_VALID / f"{lang_name}.json", "w", encoding="utf-8") as f:
        json.dump(edited_data, f, ensure_ascii=False, indent=4)
