# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'camera.ui'
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


class Ui_camera_control(object):
    def setupUi(self, camera_control):
        if camera_control.objectName():
            camera_control.setObjectName(u"camera_control")
        camera_control.resize(409, 157)
        self.gridLayout = QGridLayout(camera_control)
        self.gridLayout.setObjectName(u"gridLayout")
        self.line = QFrame(camera_control)
        self.line.setObjectName(u"line")
        self.line.setLineWidth(1)
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line, 0, 2, 7, 1)

        self.wide_normal = QPushButton(camera_control)
        self.wide_normal.setObjectName(u"wide_normal")

        self.gridLayout.addWidget(self.wide_normal, 3, 3, 1, 1)

        self.tele_normal = QPushButton(camera_control)
        self.tele_normal.setObjectName(u"tele_normal")

        self.gridLayout.addWidget(self.tele_normal, 1, 3, 1, 1)

        self.status = QTextBrowser(camera_control)
        self.status.setObjectName(u"status")

        self.gridLayout.addWidget(self.status, 0, 1, 7, 1)

        self.tele_fast = QPushButton(camera_control)
        self.tele_fast.setObjectName(u"tele_fast")

        self.gridLayout.addWidget(self.tele_fast, 0, 3, 1, 1)

        self.wide_fast = QPushButton(camera_control)
        self.wide_fast.setObjectName(u"wide_fast")

        self.gridLayout.addWidget(self.wide_fast, 4, 3, 1, 1)

        self.zoomstop = QPushButton(camera_control)
        self.zoomstop.setObjectName(u"zoomstop")

        self.gridLayout.addWidget(self.zoomstop, 2, 3, 1, 1)


        self.retranslateUi(camera_control)

        QMetaObject.connectSlotsByName(camera_control)
    # setupUi

    def retranslateUi(self, camera_control):
        camera_control.setWindowTitle(QCoreApplication.translate("camera_control", u"Form", None))
        self.wide_normal.setText(QCoreApplication.translate("camera_control", u"Zoom Out Slow", None))
        self.tele_normal.setText(QCoreApplication.translate("camera_control", u"Zoom In Slow", None))
        self.tele_fast.setText(QCoreApplication.translate("camera_control", u"Zoom In Fast", None))
        self.wide_fast.setText(QCoreApplication.translate("camera_control", u"Zoom Out Fast", None))
        self.zoomstop.setText(QCoreApplication.translate("camera_control", u"Backup Stop Zoom", None))
    # retranslateUi

