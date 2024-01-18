import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.join(current_dir, "..")
sys.path.append(parent_dir)

from app import app

app = app
