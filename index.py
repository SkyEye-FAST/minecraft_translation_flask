# -*- encoding: utf-8 -*-
"""供Vercel使用的索引文件"""

import sys
from pathlib import Path
from app import flask_app

sys.path.append(str(Path(__file__).resolve().parent.parent))

app = flask_app
