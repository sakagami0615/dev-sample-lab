"""app/ を sys.path に追加し、`services` / `models` をトップレベルパッケージとして
import できるようにする(app.py が streamlit 実行時に行うのと同じ解決方法)。
"""
import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent / "app"
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))
