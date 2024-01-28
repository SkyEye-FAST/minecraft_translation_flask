# -*- encoding: utf-8 -*-
"""Minecraft中文标准译名查询网页，使用Flask编写的后端框架"""

from os import getenv
from datetime import datetime

from flask import Flask, session, render_template, request, send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

from flask_babel import Babel, lazy_gettext as _l
from babel.dates import format_date, get_timezone, get_timezone_name
import geoip2.database
import geoip2.errors

from base import P, data, is_valid_key, get_translation

flask_app = Flask(__name__)
flask_app.config["SECRET_KEY"] = getenv("SECRET_KEY", "dev")


def get_locale():
    """语言选择器"""
    return request.accept_languages.best_match(["zh", "en", "ja", "ru", "fr"])


def get_timezone_from_ip():
    """根据IP获取时区"""
    ip = request.remote_addr
    try:
        with geoip2.database.Reader(P / "GeoLite2-City.mmdb") as reader:
            response = reader.city(ip)
        return response.location.time_zone
    except geoip2.errors.AddressNotFoundError:
        return request.headers.get("Time-Zone")


babel = Babel(
    flask_app, locale_selector=get_locale, timezone_selector=get_timezone_from_ip
)


@flask_app.before_request
def determine_locale_and_timezone():
    """将语言和时区存入会话"""
    session["locale"] = get_locale()
    session["timezone"] = get_timezone_from_ip()


class QueryForm(FlaskForm):
    """查询表单"""

    source_string = StringField(_l("Source string content to be queried: "))
    submit = SubmitField(_l("QUERY"))


@flask_app.route("/", methods=["GET", "POST"])
def index():
    """主页面"""

    # 时区
    tzinfo = get_timezone(session["timezone"])
    timezone_str = get_timezone_name(session["timezone"], locale=session["locale"])
    date_tz = datetime.now(tz=tzinfo).date()
    date_str_t = format_date(date_tz, "long", locale=session["locale"])

    form = QueryForm()

    query_str = form.source_string.data
    selected_option = request.form.get("options", "")
    if not query_str:
        selected_option = ""  # 清空下拉列表选择项

    # 获取翻译
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
        date_str=date_tz,
        date_str_t=date_str_t,
        timezone_str=timezone_str,
    )


@flask_app.route("/favicon.ico")
def favicon():
    """favcion.ico重定向"""
    return send_from_directory("static", "favicon.ico")


if __name__ == "__main__":
    flask_app.run()
