import contextlib
from functools import partial
from queue import Queue, Empty
import xml.etree.ElementTree as ET

from PySide2 import QtWidgets
from PySide2.QtCore import Qt, Signal, QTimer, QUrl, QUrlQuery, QByteArray
from PySide2 import QtGui
from PySide2.QtNetwork import QNetworkRequest, QNetworkReply

from ..ui.camera import Ui_camera_control
from ..network.ssdp import CamDesc


class MdiSubWindowCloser(QtWidgets.QMdiSubWindow):
    closed = Signal()

    def closeEvent(self, closeEvent: QtGui.QCloseEvent):
        self.closed.emit()
        super().closeEvent(closeEvent)


ZOOM_COMMANDS = ("tele_fast", "tele_normal", "wide_fast", "wide_normal", "zoomstop")


class CameraControl(QtWidgets.QWidget, Ui_camera_control):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setFocusPolicy(Qt.StrongFocus)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        self.button_signal_for_key_event(event, "pressed")

    def keyReleaseEvent(self, event: QtGui.QKeyEvent):
        self.button_signal_for_key_event(event, "released")

    def button_signal_for_key_event(self, event: QtGui.QKeyEvent, signal_name: str):
        if event.isAutoRepeat():
            return None

        button = None

        if event.key() == Qt.Key_Up:
            if event.modifiers() == Qt.ShiftModifier:
                button = self.tele_fast
            elif event.modifiers() == Qt.NoModifier:
                button = self.tele_normal
        elif event.key() == Qt.Key_Down:
            if event.modifiers() == Qt.ShiftModifier:
                button = self.wide_fast
            elif event.modifiers() == Qt.NoModifier:
                button = self.wide_normal
        elif event.key() == Qt.Key_End and event.modifiers() == Qt.NoModifier:
            button = self.zoomstop

        if button is None:
            return

        getattr(button, signal_name).emit()


class CameraController:
    PING_RATE_MS = 1000
    STATUS_MAP = {
        "Battery": "./state/batt",
        "Mode": "./state/cammode",
        "Remaining Capacity": "./state/remaincapacity",
        "Wifi Strength": "./state/wifiradio",
        "Temperature": "./state/temperature"
    }

    def __init__(self, main_controller: "MainController", camera_description: CamDesc, mdi_area: QtWidgets.QMdiArea):
        self.main_controller = main_controller
        self.camera_description = camera_description
        self.address_str = camera_description.host.toString()

        self.sub_window = sub_window = MdiSubWindowCloser()
        sub_window.setWindowTitle(self.address_str)
        sub_window.setAttribute(Qt.WA_DeleteOnClose)
        sub_window.closed.connect(self.window_closed)
        camera_control = CameraControl(parent=sub_window)

        self.status = camera_control.status

        for cmd in ZOOM_COMMANDS:
            control = getattr(camera_control, cmd)
            cmd_name = cmd.replace("_", "-")
            control.pressed.connect(partial(self.zoom_command_pressed, cmd_name))
            control.released.connect(self.zoom_command_released)

        sub_window.setWidget(camera_control)
        mdi_area.addSubWindow(sub_window)
        sub_window.show()

        self.base_url = QUrl(f"http://{self.address_str}/cam.cgi")
        self.base_request = QNetworkRequest()
        self.base_request.setRawHeader(QByteArray(b"Connection"), QByteArray(b"Keep-Alive"))
        self.base_request.setRawHeader(QByteArray(b"User-Agent"), QByteArray(b"Apache-HttpClient"))

        self.status_query_request = self.build_request({"mode": "getstate"})
        self.stop_zoom_request = self.build_request({"mode": "camcmd",
                                                     "value": "zoomstop"})

        self.ping_timer = QTimer(self.sub_window)
        self.ping_timer.timeout.connect(self.request_device_state)

        self.initial_requests = Queue()
        self.build_initial_request_list()

        request = self.get_next_request()
        self.query(request)

    def query(self, request: QNetworkRequest, ping_count=0, next_request=True, close_on_fail=True):
        reply = self.main_controller.network_access_manager.get(request)
        reply.finished.connect(lambda: self.query_response(reply, request, ping_count,
                                                           next_request, close_on_fail))

    def query_response(self, reply: QNetworkReply, original_request, ping_count, next_request, close_on_fail):
        if reply.error() != QNetworkReply.NoError:
            print(f"Error query response: {reply.errorString()}")
            if ping_count < 2:
                print(f"Failed {ping_count+1} times. Trying again.")
                self.query(original_request, ping_count+1)
            else:
                print(f"Failed {ping_count} times. Giving up.")
                if close_on_fail:
                    self.sub_window.close()

            next_request = False

        reply.deleteLater()

        if not next_request:
            return

        request = self.get_next_request()
        if request is not None:
            self.query(request)
        else:
            self.ping_timer.start(CameraController.PING_RATE_MS)

    def build_request(self, query_items):
        query = QUrlQuery()
        for k, v in query_items.items():
            query.addQueryItem(k, v)
        url = QUrl(self.base_url)
        url.setQuery(query)
        request = QNetworkRequest(self.base_request)
        request.setUrl(url)
        return request

    def build_initial_request_list(self):
        # The initial request is a custom job.
        url = QUrl(self.camera_description.location)
        request = QNetworkRequest(url)
        request.setRawHeader(QByteArray(b"User-Agent"), QByteArray(b"Panasonic Android/1 DM-CP"))
        self.initial_requests.put(request)

        r = self.build_request({
            "mode": "accctrl",
            "type": "req_acc",
            "value": "4D454930-0100-1000-8000-D453835D5F48",
            "value2": "LG-SP320"
        })
        self.initial_requests.put(r)

        r = self.build_request({
            "mode": "getinfo",
            "type": "capability"
        })
        self.initial_requests.put(r)

        r = self. build_request({
            "mode": "getinfo",
            "type": "allmenu"
        })
        self.initial_requests.put(r)

        r = self.build_request({
            "mode": "getinfo",
            "type": "curmenu"
        })
        self.initial_requests.put(r)

    def get_next_request(self):
        request = None
        with contextlib.suppress(Empty):
            request = self.initial_requests.get_nowait()

        return request

    def zoom_command_pressed(self, cmd):
        print(f"Executing {cmd}")
        r = self.build_request({"mode": "camcmd",
                                "value": cmd})
        self.query(r, next_request=False, close_on_fail=False)

    def zoom_command_released(self):
        print(f"Stopping Zoom")
        self.query(self.stop_zoom_request, next_request=False, close_on_fail=False)

    def window_closed(self):
        print("Window closed")
        self.main_controller.controller_closed(self.address_str)

    def request_device_state(self):
        reply = self.main_controller.network_access_manager.get(self.status_query_request)
        reply.finished.connect(lambda: self.handle_device_state_response(reply))

    def handle_device_state_response(self, reply: QNetworkReply):
        if reply.error() != QNetworkReply.NoError:
            print(f"Error device state response: {reply.errorString()}")
            self.status.setText(reply.errorString())
        else:
            self.status.clear()
            data = reply.readAll()
            root = ET.fromstring(data)
            result_list = []
            for label, path in CameraController.STATUS_MAP.items():
                r = root.findall(path)
                result = "ERROR"
                if len(r) > 0:
                    result = r[0].text
                result_list.append(f"{label}: {result}")

            self.status.setText("\n".join(result_list))
        reply.deleteLater()
