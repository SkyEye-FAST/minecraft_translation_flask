# -*- encoding: utf-8 -*-
"""Minecraft标准译名查询网页，使用Flask编写的后端框架"""

from os import getenv
from datetime import datetime
from typing import Optional

from flask import Flask, session, render_template, request, send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from flask_babel import Babel, lazy_gettext as _l
from babel.dates import format_date, get_timezone, get_timezone_name
import geoip2.database
import geoip2.errors

from app_base import P
from app_init import data, get_translation

# 初始化 Flask 应用
flask_app = Flask(__name__)
flask_app.config["SECRET_KEY"] = getenv("SECRET_KEY", "dev")


def get_locale() -> str:
    """
    语言选择器，根据请求的接受语言，返回最匹配的语言代码。

    Returns:
        str: 返回匹配的语言代码，默认返回 "en"。
    """

    return request.accept_languages.best_match(["zh", "en"], default="en")


def get_timezone_from_ip() -> Optional[str]:
    """
    根据客户端 IP 地址获取对应的时区信息。

    Returns:
        Optional[str]: 返回对应的时区字符串，如果无法获取则返回请求头中的 "Time-Zone" 信息。
    """

    ip = request.remote_addr
    try:
        with geoip2.database.Reader(P / "GeoLite2-City.mmdb") as reader:
            response = reader.city(ip)
            return response.location.time_zone
    except geoip2.errors.AddressNotFoundError:
        return request.headers.get("Time-Zone")


# 初始化 Babel
babel = Babel(
    flask_app, locale_selector=get_locale, timezone_selector=get_timezone_from_ip
)


@flask_app.before_request
def determine_locale_and_timezone() -> None:
    """
    在每次请求前确定语言和时区，并将其存储在会话中。
    """

    session["locale"] = get_locale()
    session["timezone"] = get_timezone_from_ip()


class QueryForm(FlaskForm):
    """
    查询表单，用于获取用户输入的查询字符串和是否启用附加语言的选项。
    """

    jkv_check: BooleanField = BooleanField(_l("Enable additional languages"))
    source_string: StringField = StringField(
        _l("Source string content to be queried: ")
    )
    submit: SubmitField = SubmitField(_l("QUERY"))


@flask_app.route("/", methods=["GET", "POST"])
def index() -> str:
    """
    主页面路由，处理查询表单的提交和渲染主页面模板。

    Returns:
        str: 渲染后的主页面 HTML。
    """

    form = QueryForm()
    query_str: Optional[str] = form.source_string.data
    enable_jkv: bool = form.jkv_check.data
    selected_option: str = request.form.get("options", "")

    if not query_str:
        selected_option = ""  # 清空下拉列表选择项

    translation, source_str = {}, ""
    if form.validate_on_submit() and query_str:
        translation = get_translation(query_str)
        source_str = data["en_us"].get(selected_option, "")

    keys = data["en_us"].keys() if not form.validate_on_submit() else translation.keys()
    mappings = {"filled_map": "item", "trim_pattern": "item", "upgrade": "item"}
    category = selected_option.split(".")[0]
    category = mappings.get(category, category)

    tzinfo = get_timezone(session["timezone"])
    timezone_str = get_timezone_name(session["timezone"], locale=session["locale"])
    date_tz = datetime.now(tz=tzinfo).date()
    date_str_t = format_date(date_tz, "long", locale=session["locale"])

    context = {
        "form": form,
        "source": source_str,
        "key": selected_option,
        "input_value": query_str,
        "keys": keys,
        "translation": translation.get(selected_option, {}),
        "date_str": date_tz,
        "date_str_t": date_str_t,
        "timezone_str": timezone_str,
        "enable_jkv": enable_jkv,
        "category": category,
    }

    return render_template("index.html", **context)


@flask_app.route("/table")
def table() -> str:
    """
    表格界面路由，渲染表格页面模板。

    Returns:
        str: 渲染后的表格页面 HTML。
    """

    tzinfo = get_timezone(session["timezone"])
    date_tz = datetime.now(tz=tzinfo).date()

    return render_template("table.html", date_str=date_tz)


@flask_app.route("/favicon.ico")
def favicon() -> str:
    """
    favicon.ico 重定向路由。

    Returns:
        str: 静态文件 favicon.ico 的路径。
    """

    return send_from_directory("static", "favicon.ico")


@flask_app.route("/table.tsv")
def table_tsv() -> str:
    """
    table.tsv 重定向路由。

    Returns:
        str: 静态文件 table.tsv 的路径。
    """

    return send_from_directory("static", "table.tsv")


if __name__ == "__main__":
    flask_app.run()
