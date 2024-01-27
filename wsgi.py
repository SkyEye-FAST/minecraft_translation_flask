# -*- encoding: utf-8 -*-
"""手动设置环境变量并导入程序实例"""

from pathlib import Path
from dotenv import load_dotenv
from app import flask_app

dotenv_path = Path(__file__).resolve().parent / ".env"
if dotenv_path.exists():
    load_dotenv(dotenv_path)

app = flask_app
