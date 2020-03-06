from PySide2.QtGui import QKeyEvent
from PySide2.QtCore import Qt, QEvent

a = QKeyEvent(QEvent.KeyPress, Qt.Key_Up, Qt.NoModifier)
a.__eq__()