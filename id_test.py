# -*- encoding: utf-8 -*-
"""编码语言文件键名测试"""

import json
import random

from app_base import ID_MAP_PATH

with open(ID_MAP_PATH, "r", encoding="utf-8") as f:
    id_map = json.load(f)

random_keys = random.sample(list(id_map.keys()), 10)
print(code := "".join(random_keys))

# code = input("Question Group Code: ")
code_list = [code[i : i + 3] for i in range(0, 30, 3)]
output_keys = {code: id_map[code] for code in code_list}
print(output_keys)
