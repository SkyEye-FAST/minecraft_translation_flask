import json
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
    selected_option = source_str = ""
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
            source_str = data["en_us"][selected_option]

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
