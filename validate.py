# -*- encoding: utf-8 -*-
"""验证并提取语言文件"""

import re
import json
from typing import Tuple, Dict, Set

from app_base import LANG_DIR_FULL, LANG_DIR_VALID, language_list

# 定义常量
PREFIXES: Tuple[str, ...] = (
    "block.",
    "item.minecraft.",
    "entity.minecraft.",
    "biome.",
    "effect.minecraft.",
    "enchantment.minecraft.",
    "trim_pattern.",
    "upgrade.",
    "filled_map",
)

# 定义正则模式
INVALID_BLOCK_ITEM_ENTITY_PATTERN = re.compile(
    r"(block\.minecraft\.|item\.minecraft\.|entity\.minecraft\.)[^.]*\."
)
ITEM_EFFECT_PATTERN = re.compile(r"item\.minecraft\.[^.]*\.effect\.[^.]*")
ADVANCEMENTS_TITLE_PATTERN = re.compile(r"advancements\.(.*)\.title")

# 定义排除项
EXCLUSIONS: Set[str] = {
    "block.minecraft.set_spawn",
    "entity.minecraft.falling_block_type",
    "filled_map.id",
    "filled_map.level",
    "filled_map.locked",
    "filled_map.scale",
    "filled_map.unknown",
}


def is_valid_key(translation_key: str) -> bool:
    """
    判断是否为有效键名。

    Args:
        translation_key (str): 需要验证的键名。

    Returns:
        bool: 如果键名有效，返回 True；否则返回 False。
    """

    if ADVANCEMENTS_TITLE_PATTERN.match(translation_key):
        return True

    if not translation_key.startswith(PREFIXES):
        return False

    if translation_key in EXCLUSIONS or "pottery_shard" in translation_key:
        return False

    if ITEM_EFFECT_PATTERN.match(translation_key):
        return True

    if INVALID_BLOCK_ITEM_ENTITY_PATTERN.match(translation_key):
        return False

    return True


# 文件夹
LANG_DIR_VALID.mkdir(exist_ok=True)

# 修改语言文件
for lang_name in language_list:
    with open(LANG_DIR_FULL / f"{lang_name}.json", "r", encoding="utf-8") as f:
        data: Dict[str, str] = json.load(f)
    edited_data: Dict[str, str] = {k: v for k, v in data.items() if is_valid_key(k)}
    with open(LANG_DIR_VALID / f"{lang_name}.json", "w", encoding="utf-8") as f:
        json.dump(edited_data, f, ensure_ascii=False, indent=4)
