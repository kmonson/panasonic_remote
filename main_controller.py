from PySide2 import QtWidgets
from PySide2.QtCore import QTimer, Qt, Signal
from PySide2.QtNetwork import QNetworkAccessManager

from camera_controller import CameraController
from ui.main_ui import Ui_MainWindow
from network.ssdp import SSDPInterface, CamDesc


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class MainController:
    PING_RATE_MS = 3000

    def __init__(self):
        self.window = MainWindow()
        self.network_access_manager = QNetworkAccessManager(self.window)
        self.window.controllers_mdi.tileSubWindows()
        self.ping_timer = QTimer(self.window)
        self.detected_devices = {}
        self.open_devices = {}
        self.ssdp_interface = SSDPInterface(parent=self.window)
        self.ssdp_interface.new_device.connect(self.device_info_received)
        self.window.refresh_button.clicked.connect(self.refresh_clicked)
        self.ping_timer.timeout.connect(self.ssdp_interface.ping_devices)
        self.window.auto_ping.stateChanged.connect(self.auto_ping_changed)
        self.window.camera_list.itemDoubleClicked.connect(self.item_double_clicked)
        if self.window.auto_ping.isChecked():
            print("Starting auto ping")
            self.ping_timer.start(MainController.PING_RATE_MS)

    def refresh_clicked(self):
        self.window.camera_list.clear()
        self.detected_devices.clear()
        self.ssdp_interface.ping_devices()

    def auto_ping_changed(self, state):
        if state == Qt.Checked:
            if not self.ping_timer.isActive():
                print("Starting auto ping")
                self.ping_timer.start(MainController.PING_RATE_MS)
        else:
            print("Stopping auto ping")
            self.ping_timer.stop()

    def show(self):
        self.window.show()

    def device_info_received(self, cam_desc: CamDesc):
        add_string = cam_desc.host.toString()
        if add_string not in self.detected_devices:
            self.detected_devices[add_string] = cam_desc
            self.window.camera_list.addItem(add_string)
        if self.window.open_automatically.isChecked():
            self.open_controller(add_string)

    def item_double_clicked(self, item: QtWidgets.QListWidgetItem):
        self.open_controller(item.text())

    def open_controller(self, add_string):
        if add_string in self.open_devices:
            return

        print(f"Opening controller for {add_string}")
        cam_controller = CameraController(self, self.detected_devices[add_string], self.window.controllers_mdi)
        self.open_devices[add_string] = cam_controller

    def controller_closed(self, add_string):
        self.open_devices.pop(add_string)

