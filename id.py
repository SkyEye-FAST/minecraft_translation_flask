# -*- encoding: utf-8 -*-
"""编码语言文件键名"""

import hashlib
import json
from typing import Dict

from app_base import P
from app_init import data

BASE62 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"


def sha256_to_base62(input_string: str, length: int = 3) -> str:
    """生成SHA-256哈希值，并用Base62映射压缩"""

    # 计算SHA-256哈希值
    sha256_hash = hashlib.sha256(input_string.encode()).digest()

    # 将哈希值转换为整数，并映射到较小范围内
    hash_int = int.from_bytes(sha256_hash, byteorder="big")
    base62_length = len(BASE62)
    base62_string = ""

    # 不断对base62_length取模，并将结果转换为相应字符
    while hash_int > 0:
        remainder = hash_int % base62_length
        base62_string = BASE62[remainder] + base62_string
        hash_int = hash_int // base62_length

    # 确保字符串长度为指定的长度（不足则填充）
    base62_string = base62_string.zfill(length)

    return base62_string[:length]


code_to_key_map: Dict[str, str] = {sha256_to_base62(key): key for key in data["en_us"]}

for code, key in code_to_key_map.items():
    print(f"编码: {code} -> 键: {key}")

with open(P / "static" / "id.json", "w", encoding="utf-8") as f:
    json.dump(code_to_key_map, f, ensure_ascii=False, indent=4)
