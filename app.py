# -*- encoding: utf-8 -*-
"""Minecraft标准译名查询网页，使用Flask编写的后端框架"""

from os import getenv
from datetime import datetime, timezone
from typing import Optional
from random import sample

from flask import (
    Flask,
    session,
    render_template,
    request,
    send_from_directory,
    redirect,
    url_for,
    jsonify,
)
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from flask_babel import Babel, lazy_gettext as _l
from babel.dates import format_date, get_timezone, get_timezone_name
import geoip2.database
import geoip2.errors

from app_base import P
from app_init import data, id_map, rating, get_translation

# 初始化 Flask 应用
flask_app = Flask(__name__)
flask_app.config["SECRET_KEY"] = getenv("SECRET_KEY", "dev")


def get_locale() -> str:
    """
    语言选择器，根据请求的接受语言，返回最匹配的语言代码。

    Returns:
        str: 返回匹配的语言代码，默认返回 "en"。
    """

    locale = request.accept_languages.best_match(
        ["zh_CN", "zh_TW", "zh", "en"], default="zh_CN"
    )
    if locale == "zh":
        return "zh_CN"
    return "en"


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


def handle_category(selected_option: str) -> str:
    """
    处理字符串分类，以便显示表格。

    Args:
        selected_option (str): 字符串对应的键名

    Returns:
        str: 字符串所属的分类。
    """

    mappings = {"filled_map": "item", "trim_pattern": "item", "upgrade": "item"}
    category = selected_option.split(".")[0]
    category = mappings.get(category, category)

    return category


class QueryForm(FlaskForm):
    """
    查询表单，用于获取用户输入的查询字符串和是否启用附加语言的选项。
    """

    input_string: StringField = StringField(_l("Content to be queried: "))
    jkv_check: BooleanField = BooleanField(_l("Enable additional languages"))
    submit: SubmitField = SubmitField(_l("QUERY"))


@flask_app.route("/", methods=["GET", "POST"])
def index() -> str:
    """
    主页面路由，处理查询表单的提交并渲染主页面模板。

    Returns:
        str: 渲染后的主页面 HTML。
    """

    form = QueryForm()
    results = {}
    query_mode = "source"
    query_lang = "zh_cn"
    query_str = ""
    enable_jkv = False
    selected_option = ""

    if form.validate_on_submit():
        query_str = form.input_string.data
        query_mode = request.form.get("query-mode", "source")
        enable_jkv = form.jkv_check.data
        selected_option = request.form.get("option", "")
        if query_str:
            if query_mode == "source":
                results = get_translation(query_str)
            elif query_mode == "transl":
                query_lang = request.form.get("query-lang", "zh_cn")
                results = get_translation(query_str, query_lang)
            elif query_mode == "key":
                results = get_translation(query_str, "key")
        else:
            selected_option = ""  # 清空下拉列表选择项

    source_str = data["en_us"].get(selected_option, "")
    keys = data["en_us"].keys() if not form.validate_on_submit() else results.keys()

    timezone_str = get_timezone_name(session["timezone"], locale=session["locale"])
    date_tz = datetime.now(tz=get_timezone(session["timezone"])).date()

    context = {
        "action": "/",
        "form": form,
        "mode": query_mode,
        "lang": query_lang,
        "source": source_str,
        "key": selected_option,
        "input_value": query_str,
        "keys": keys,
        "translation": results.get(selected_option, {}),
        "date_str": date_tz,
        "date_str_t": format_date(date_tz, "long", locale=session["locale"]),
        "timezone_str": timezone_str,
        "enable_jkv": enable_jkv,
        "category": handle_category(selected_option),
    }

    return render_template("index.html", **context)


def validate_language_code(lang_code: str) -> bool:
    """
    判断语言代码是否有效的函数，有效则返回True，否则返回False。

    Args:
        lang_code (str): 语言代码。

    Returns:
        bool: 是否有效。
    """

    valid_lang_codes = ["zh_cn", "zh_hk", "zh_tw", "lzh"]
    if lang_code in valid_lang_codes:
        return True
    return False


@flask_app.route("/p", methods=["GET", "POST"])
def index_param() -> str:
    """
    主页面（可传参）路由，处理查询表单的提交并渲染主页面模板。

    Returns:
        str: 渲染后的主页面 HTML。
    """

    form = QueryForm()
    results = {}
    query_mode = request.args.get("mode", "source")
    query_lang = request.args.get("lang", "zh_cn") if query_mode == "transl" else ""
    query_str = request.args.get("input", "")
    enable_jkv = request.args.get("enable_jkv", "false").lower() in ["true", "1", "yes"]
    selected_option = request.args.get("option", "")

    if form.validate_on_submit():
        query_str = form.input_string.data
        query_mode = request.form.get("query-mode", "source")
        enable_jkv = form.jkv_check.data
        selected_option = request.form.get("option", "")

        if query_mode == "transl":
            query_lang = request.form.get("query-lang", "zh_cn")
            if not validate_language_code(query_lang):
                query_lang = "zh_cn"
            return redirect(
                url_for(
                    "index_param",
                    mode=query_mode,
                    lang=query_lang,
                    input=query_str,
                    enable_jkv=enable_jkv,
                    option=selected_option,
                )
            )
        return redirect(
            url_for(
                "index_param",
                mode=query_mode,
                input=query_str,
                enable_jkv=enable_jkv,
                option=selected_option,
            )
        )

    form.input_string.data = query_str
    form.jkv_check.data = enable_jkv

    if query_str:
        if query_mode == "source":
            results = get_translation(query_str)
        elif query_mode == "transl":
            results = get_translation(query_str, query_lang)
        elif query_mode == "key":
            results = get_translation(query_str, "key")
    else:
        selected_option = ""

    source_str = data["en_us"].get(selected_option, "")
    keys = results.keys()

    timezone_str = get_timezone_name(session["timezone"], locale=session["locale"])
    date_tz = datetime.now(tz=get_timezone(session["timezone"])).date()

    context = {
        "action": "/p",
        "form": form,
        "mode": query_mode,
        "lang": query_lang,
        "source": source_str,
        "key": selected_option,
        "input_value": query_str,
        "keys": keys,
        "translation": results.get(selected_option, {}),
        "date_str": date_tz,
        "date_str_t": format_date(date_tz, "long", locale=session["locale"]),
        "timezone_str": timezone_str,
        "enable_jkv": enable_jkv,
        "category": handle_category(selected_option),
    }

    return render_template("index.html", **context)


@flask_app.route("/api", methods=["GET"])
def api():
    """
    API 路由。

    Returns:
        ~flask.Response
    """

    results = {}

    query_mode = request.args.get("mode", "source")
    if query_mode not in ["source", "transl", "key"]:
        return jsonify({"error": "Invalid query mode"}), 400

    query_lang = request.args.get("lang", "zh_cn") if query_mode == "transl" else ""
    if query_mode == "transl" and not validate_language_code(query_lang):
        return jsonify({"error": "Invalid language code"}), 400

    query_str = request.args.get("input", "")
    if not query_str:
        return jsonify({"error": "Missing input parameter"}), 400

    if query_str:
        if query_mode == "source":
            results = get_translation(query_str)
        elif query_mode == "transl":
            results = get_translation(query_str, query_lang)
        elif query_mode == "key":
            results = get_translation(query_str, "key")

    output = {
        "request_time": datetime.now(timezone.utc).isoformat(),
        "result": results,
    }
    return jsonify(output)


@flask_app.route("/table")
def table() -> str:
    """
    表格页面路由，渲染表格页面模板。

    Returns:
        str: 渲染后的表格页面 HTML。
    """

    tzinfo = get_timezone(session["timezone"])
    date_tz = datetime.now(tz=tzinfo).date()

    return render_template("table.html", date_str=date_tz)


QUESTION_AMOUNT = 10  # 测验题组含题目数量


def get_questions() -> str:
    """
    获取题目函数。

    从 ID 映射中随机抽取以生成题组。

    Returns:
        str: 题组编号。
    """

    keys = list(id_map.keys())
    random_keys = sorted(sample(keys, QUESTION_AMOUNT), key=lambda x: id_map[x])
    return "".join(random_keys)


@flask_app.route("/quiz")
def quiz_portal() -> str:
    """
    测验门户页面路由。

    Returns:
        str: 渲染后的测验门户页面 HTML。
    """
    p1 = _l("Enter question group code...")

    return render_template(
        "quiz_portal.html",
        placeholder=p1,
        locale=session["locale"],
        random_code=get_questions(),
    )


@flask_app.route("/quiz/")
def quiz_redirect():
    """
    重定向`/quiz/`至`/quiz`的路由。
    """

    return redirect(url_for("quiz_portal"))


@flask_app.route("/quiz/<code>", methods=["GET"])
def quiz_sub(code: str) -> str:
    """
    测验子页面路由。

    Args:
        code (str): 题组编号。

    Returns:
        str: 渲染后的测验子页面页面 HTML。
    """

    lang = request.args.get("l", "zh_cn")
    if not validate_language_code(lang):
        lang = "zh_cn"

    if len(code) != 3 * QUESTION_AMOUNT:
        return render_template("quiz_error.html")

    code_list = [code[i : i + 3] for i in range(0, 3 * QUESTION_AMOUNT, 3)]
    if any(seg not in id_map for seg in code_list):
        return render_template("quiz_error.html")

    keys = [id_map[seg] for seg in code_list]
    questions = {
        key: {"source": data["en_us"][key], "translation": data[lang][key]}
        for key in keys
    }
    if lang == "zh_cn":
        for k, d in questions.items():
            d["rating"] = rating[k]

    p2 = _l("Enter translation here...")

    return render_template(
        "quiz_sub.html",
        lang=lang.replace("_", "-"),
        locale=session["locale"],
        questions=questions,
        placeholder=p2,
        random_code=get_questions(),
    )


@flask_app.route("/favicon.ico")
def favicon() -> str:
    """
    favicon.ico 重定向路由。

    Returns:
        str: 静态文件 favicon.ico 的路径。
    """

    return send_from_directory("static", "favicon.ico")


@flask_app.route("/apple-touch-icon.png")
def apple_touch_icon() -> str:
    """
    apple-touch-icon.png 重定向路由。

    Returns:
        str: 静态文件 apple-touch-icon.png 的路径。
    """

    return send_from_directory("static", "apple-touch-icon.png")


@flask_app.route("/table.tsv")
def table_tsv() -> str:
    """
    table.tsv 重定向路由。

    Returns:
        str: 静态文件 table.tsv 的路径。
    """

    return send_from_directory("static", "table.tsv")


@flask_app.errorhandler(404)
def error_404(e) -> str:
    """
    404 重定向路由。

    Returns:
        str: 渲染后的 404 页面 HTML。
    """

    print(e)
    return render_template("404.html"), 404


if __name__ == "__main__":
    flask_app.run()
