import sys

from PySide2 import QtWidgets
from main_controller import MainController


def main():
    app = QtWidgets.QApplication(sys.argv)

    main = MainController()
    main.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
