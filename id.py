# -*- encoding: utf-8 -*-
"""编码语言文件键名"""

import hashlib
from typing import Dict

import ujson

BASE62 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"


def sha256_to_base62(input_string: str, length: int = 3) -> str:
    """
    生成SHA-256哈希值，并用Base62映射压缩为指定长度的字符串。

    Args:
        input_string (str): 需要生成哈希值的输入字符串。
        length (int): 生成的Base62字符串的长度，默认为3。

    Returns:
        str: 压缩后的Base62字符串。
    """

    sha256_hash = hashlib.sha256(input_string.encode()).digest()
    hash_int = int.from_bytes(sha256_hash)
    base62_string = ""

    while hash_int > 0:
        hash_int, remainder = divmod(hash_int, len(BASE62))
        base62_string = BASE62[remainder] + base62_string

    return base62_string.zfill(length)[:length]


if __name__ == "__main__":
    from app_base import ID_MAP_PATH
    from app_init import data

    code_to_key_map: Dict[str, str] = {
        sha256_to_base62(key): key for key in data["en_us"]
    }

    for code, key in code_to_key_map.items():
        print(f"编码: {code} -> 键: {key}")

    with open(ID_MAP_PATH, "w", encoding="utf-8") as f:
        ujson.dump(code_to_key_map, f, ensure_ascii=False, indent=4)
