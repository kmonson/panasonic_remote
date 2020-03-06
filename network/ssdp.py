from PySide2.QtNetwork import QUdpSocket, QHostAddress, QNetworkDatagram, QNetworkInterface, QAbstractSocket
from PySide2.QtCore import QObject, Signal, QByteArray
import http.client
import io
from functools import partial
from typing import NamedTuple, Optional


class _FakeSocket(io.BytesIO):
    def makefile(self, *args, **kw):
        return self


def create_message(address, port, mx, service):
    return "\r\n".join([
        'M-SEARCH * HTTP/1.1',
        f'HOST: {address}:{port}',
        'MAN: "ssdp:discover"',
        f'MX: {mx}',
        f'ST: {service}',
        '', '']).encode('ANSI')


class CamDesc(NamedTuple):
    location: str
    host: QHostAddress


class SSDPInterface(QObject):
    ADDRESS = "239.255.255.250"
    PORT = 1900
    SERVICE = "urn:schemas-upnp-org:device:MediaServer:1"
    new_device = Signal(CamDesc)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ping_message = create_message(SSDPInterface.ADDRESS, SSDPInterface.PORT, 2, SSDPInterface.SERVICE)
        self.broadcast_datagram = QNetworkDatagram(QByteArray(ping_message),
                                                   QHostAddress(SSDPInterface.ADDRESS),
                                                   SSDPInterface.PORT)
        self.udp_sockets = socks = []
        for host_address in QNetworkInterface.allAddresses():
            if host_address.isLoopback() or host_address.protocol() != QAbstractSocket.IPv4Protocol:
                continue
            sock = QUdpSocket(self)
            sock.bind(host_address, 50000)
            # lambdas will not work in this case as they are late binding.
            func = partial(self.packet_received, sock)
            sock.readyRead.connect(func)
            socks.append(sock)
            print(f"Connected to interface at host address: {host_address.toString()}")

    def packet_received(self, sock):
        while sock.hasPendingDatagrams():
            datagram = sock.receiveDatagram()
            result = self.process_datagram(datagram)
            if result is not None:
                self.new_device.emit(result)

    def process_datagram(self, datagram: QNetworkDatagram) -> Optional[CamDesc]:
        data = datagram.data().data()
        r = http.client.HTTPResponse(_FakeSocket(data))
        try:
            r.begin()
        except Exception as e:
            print("Failed to parse HTTPResponse header:", repr(e))
            return None

        if r.status != 200:
            print(f"Failed HTTP parse status: {r.status}")
            return None

        server = r.getheader("server", "")
        if "Panasonic" not in server:
            print(f"Rejecting non-Panasonic device: {server}")
            return None

        return CamDesc(
                r.getheader("location", ""),
                datagram.senderAddress()
            )

    def ping_devices(self):
        for sock in self.udp_sockets:
            print(f"Pinging through interface {sock.localAddress().toString()}")
            sock.writeDatagram(self.broadcast_datagram)

