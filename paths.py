from pathlib import Path
from PyQt5 import uic

BASE_DIR = Path(__file__).resolve().parent
UI_DIR = BASE_DIR / "ui"
DB_PATH = BASE_DIR / "proect.db"


def load_ui(widget, ui_file: str) -> None:
    """Загружает .ui-файл из папки ui/ в указанный виджет."""
    uic.loadUi(str(UI_DIR / ui_file), widget)