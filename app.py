# -*- encoding: utf-8 -*-
"""Minecraft中文标准译名查询网页，使用Flask编写的后端框架"""

from os import getenv
from datetime import date

from flask import Flask, render_template, request, send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

from base import data, is_valid_key, get_translation

flask_app = Flask(__name__)
flask_app.config["SECRET_KEY"] = getenv("SECRET_KEY", "dev")

page_lang = {
    "zh_cn": {
        "lang_name": "简体中文（中国大陆）",
        "query_input_label": "查询的源字符串内容：",
        "translation_key_select_label": "选择本地化键名：",
        "query_button": "查询",
    },
    "en_us": {
        "lang_name": "English (United States)",
        "query_input_label": "Source string content to be queried: ",
        "translation_key_select_label": "Select translation key：",
        "query_button": "QUERY",
    },
}


class QueryForm(FlaskForm):
    """查询表单"""

    source_string = StringField("查询的源字符串内容：")
    submit = SubmitField("查询")


@flask_app.route("/", methods=["GET", "POST"])
def index():
    """主页面"""
    form = QueryForm()

    query_str = form.source_string.data
    selected_option = request.form.get("options", "")
    if not query_str:
        selected_option = ""  # 清空下拉列表选择项

    if form.validate_on_submit():
        translation = get_translation(query_str)
        keys = [k for k in translation if is_valid_key(k)]
        selected_translation = translation.get(selected_option, {})
        source_str = data["en_us"].get(selected_option, "")
    else:
        keys = [k for k in data["en_us"].keys() if is_valid_key(k)]
        selected_translation = {}
        source_str = ""

    return render_template(
        "index.html",
        form=form,
        source=source_str,
        key=selected_option,
        input_value=query_str,
        keys=keys,
        translation=selected_translation,
        date_str=date.today(),
        date_str_zh=date.today().strftime("%Y年%#m月%#d日（UTC）"),
    )


@flask_app.route("/favicon.ico")
def favicon():
    """favcion.ico重定向"""
    return send_from_directory("static", "favicon.ico")


if __name__ == "__main__":
    flask_app.run()
