import json
import re
from pathlib import Path
from flask import Flask, render_template, request, redirect

P = Path(__file__).resolve().parent
LANG_DIR = P / "lang"

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

# 修正语言文件
updated_data = data

for lang in ["en_us", "zh_cn", "zh_hk", "zh_tw", "lzh"]:
    netherite_upgrade_str = data[lang]["upgrade.minecraft.netherite_upgrade"]
    smithing_template_str = data[lang]["item.minecraft.smithing_template"]
    music_disc_str = data[lang]["item.minecraft.music_disc_5"]
    banner_pattern_str = data[lang]["item.minecraft.mojang_banner_pattern"]
    updated_data[lang]["item.minecraft.netherite_upgrade_smithing_template"] = (
        netherite_upgrade_str + " " + smithing_template_str
        if lang == "en_us"
        else netherite_upgrade_str + smithing_template_str
    )
    trim_keys = [key for key in data[lang].keys() if "trim_smithing_template" in key]
    keys_to_add = {
        key: data[lang][
            f"trim_pattern.minecraft.{key.split('.')[2].split('_', maxsplit=1)[0]}"
        ]
        + " "
        + smithing_template_str
        if lang == "en_us"
        else data[lang][
            f"trim_pattern.minecraft.{key.split('.')[2].split('_', maxsplit=1)[0]}"
        ]
        + smithing_template_str
        for key in trim_keys
    }
    updated_data[lang].update(keys_to_add)

    keys_to_delete = [
        key
        for key in data[lang].keys()
        if key.startswith("item.minecraft.music_disc")
        or re.match(r"item\.minecraft\.(.*)_banner_pattern", key)
    ]
    for key in keys_to_delete:
        del updated_data[lang][key]
    del updated_data[lang]["item.minecraft.smithing_template"]

    updated_data[lang]["item.minecraft.music_disc_*"] = music_disc_str
    updated_data[lang]["item.minecraft.*_banner_pattern"] = banner_pattern_str

data = updated_data

# 读取补充字符串
with open(LANG_DIR / "supplements.json", "r", encoding="utf-8") as f:
    supplements = json.load(f)
for lang in ["zh_cn", "zh_hk", "zh_tw", "lzh"]:
    data[lang].update(supplements[lang])
print(f"已补充{len(supplements['zh_cn'])}条字符串。")

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    keys = translation = selected_translation = {}
    selected_option = None
    query_str = ""

    if request.method == "POST":
        query_str = request.form.get("query-input")
        if not query_str:
            query_str = ""
        selected_option = request.form.get("options")

        for k, v in data["en_us"].items():
            if query_str.lower() in v.lower():
                element = {lang: content.get(k, "？") for lang, content in data.items()}
                translation.update({k: element})

        keys = list(translation.keys())
        if selected_option:
            selected_translation = translation.get(selected_option)

    return render_template(
        "index.html",
        source=data["en_us"][selected_option],
        key=selected_option,
        input_value=query_str,
        keys=keys,
        translation=selected_translation,
    )


if __name__ == "__main__":
    app.run(debug=True)
