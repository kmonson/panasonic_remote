import sys

from PySide2 import QtWidgets
from controllers.main_controller import MainController


def main():
    app = QtWidgets.QApplication(sys.argv)

    main_controller = MainController()
    main_controller.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
