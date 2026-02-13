import sys
import os
import math
from PyQt5.QtWidgets import  QScrollArea
from PyQt5.QtGui import QPixmap, QPainter

def resource_path(relative_path):
    """Get the absolute path to a resource in the bundled app or the local filesystem."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def cell_has_value(val):
    """Считает, что в ячейке есть значение: не пусто, не 0, не NaN (пустая ячейка из Excel)."""
    if val is None:
        return False
    try:
        if isinstance(val, float) and math.isnan(val):
            return False
    except (TypeError, ValueError):
        pass
    if val == 0 or val == '0':
        return False
    if isinstance(val, str) and val.strip() == '':
        return False
    return True



class BackgroundScrollArea(QScrollArea):
    def __init__(self, background_image_path, *args, **kwargs):
        super(BackgroundScrollArea, self).__init__(*args, **kwargs)
        self.background_image = QPixmap(background_image_path)

    def paintEvent(self, event):
        painter = QPainter(self.viewport())
        painter.drawPixmap(0, 0, self.viewport().width(), self.viewport().height(), self.background_image)
        super(BackgroundScrollArea, self).paintEvent(event)