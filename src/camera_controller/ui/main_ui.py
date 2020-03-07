# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_ui.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1040, 511)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.camera_list = QListWidget(self.centralwidget)
        self.camera_list.setObjectName(u"camera_list")

        self.gridLayout.addWidget(self.camera_list, 0, 0, 1, 2)

        self.refresh_button = QPushButton(self.centralwidget)
        self.refresh_button.setObjectName(u"refresh_button")

        self.gridLayout.addWidget(self.refresh_button, 1, 0, 2, 1)

        self.open_automatically = QCheckBox(self.centralwidget)
        self.open_automatically.setObjectName(u"open_automatically")

        self.gridLayout.addWidget(self.open_automatically, 1, 1, 1, 1)

        self.auto_ping = QCheckBox(self.centralwidget)
        self.auto_ping.setObjectName(u"auto_ping")
        self.auto_ping.setChecked(True)

        self.gridLayout.addWidget(self.auto_ping, 2, 1, 1, 1)

        self.controllers_mdi = QMdiArea(self.centralwidget)
        self.controllers_mdi.setObjectName(u"controllers_mdi")

        self.gridLayout.addWidget(self.controllers_mdi, 0, 2, 3, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1040, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.refresh_button.setText(QCoreApplication.translate("MainWindow", u"Refresh", None))
        self.open_automatically.setText(QCoreApplication.translate("MainWindow", u"Open New Cameras Automatically", None))
        self.auto_ping.setText(QCoreApplication.translate("MainWindow", u"Auto Discovery", None))
    # retranslateUi

