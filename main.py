import sys

from PySide2 import QtWidgets
from main_controller import MainController

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    main = MainController()
    main.show()

    sys.exit(app.exec_())
