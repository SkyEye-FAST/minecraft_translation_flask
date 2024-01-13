# -*- encoding: utf-8 -*-
"""Minecraft中文标准译名查询网页，使用Flask编写的后端框架"""

import json
import re
from pathlib import Path
from flask import Flask, render_template, request

LANG_DIR = Path(__file__).resolve().parent / "lang"

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
with open(LANG_DIR / "supplements.json", "r", encoding="utf-8") as f:
    supplements = json.load(f)
for lang in ["zh_cn", "zh_hk", "zh_tw", "lzh"]:
    data[lang].update(supplements[lang])
print(f"已补充{len(supplements['zh_cn'])}条字符串。")


app = Flask(__name__)


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


@app.route("/", methods=["GET", "POST"])
def index():
    selected_option = request.form.get("options", "")
    query_str = request.form.get("query-input", "")
    if not query_str:
        selected_option = ""  # 清空下拉列表选择项

    if request.method == "POST":
        translation = get_translation(query_str)
        keys = [k for k in translation.keys() if is_valid_key(k)]
        selected_translation = translation.get(selected_option, {})
        source_str = data["en_us"].get(selected_option, "")
    else:
        keys = [k for k in data["en_us"].keys() if is_valid_key(k)]
        selected_translation = {}
        source_str = ""

    return render_template(
        "index.html",
        source=source_str,
        key=selected_option,
        input_value=query_str,
        keys=keys,
        translation=selected_translation,
    )


if __name__ == "__main__":
    app.run(debug=True)
