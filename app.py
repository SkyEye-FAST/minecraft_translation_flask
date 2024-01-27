# -*- encoding: utf-8 -*-
"""Minecraft中文标准译名查询网页，使用Flask编写的后端框架"""

from os import getenv
from datetime import date

from flask import Flask, g, render_template, request, send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

from flask_babel import Babel, lazy_gettext, format_date
from babel.dates import get_timezone_name

from base import data, is_valid_key, get_translation

flask_app = Flask(__name__)
flask_app.config["SECRET_KEY"] = getenv("SECRET_KEY", "dev")


def get_locale():
    """语言选择器"""
    user = getattr(g, "user", None)
    if user is not None:
        return user.locale
    return request.accept_languages.best_match(["zh", "en"])


babel = Babel(flask_app, locale_selector=get_locale)


class QueryForm(FlaskForm):
    """查询表单"""

    source_string = StringField(lazy_gettext("Source string content to be queried: "))
    submit = SubmitField(lazy_gettext("QUERY"))


@flask_app.route("/", methods=["GET", "POST"])
def index():
    """主页面"""
    timezone = request.headers.get("Time-Zone")

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
        date_str_t=format_date(date.today(), "long"),
        timezone_str=get_timezone_name(timezone, locale=get_locale()),
    )


@flask_app.route("/favicon.ico")
def favicon():
    """favcion.ico重定向"""
    return send_from_directory("static", "favicon.ico")


if __name__ == "__main__":
    flask_app.run(debug=True)
