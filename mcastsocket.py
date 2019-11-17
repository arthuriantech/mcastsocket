from struct import Struct
from socket import *


ip_mreq_pack = Struct('4sL').pack
ip_mreq_load = Struct('4sL').unpack


class MulticastSocket:
    _dumps = bytes
    _loads = bytes
    addr = None
    socket = None

    def __init__(self, addr=None):
        self.resocket()

        if addr:
            self.bind(addr)

    @classmethod
    def set_default_serializer(cls, dumps, loads):
        cls._dumps = dumps
        cls._loads = loads

    def set_serializer(self, dumps, loads):
        self._dumps = dumps
        self._loads = loads

    def resocket(self):
        if self.socket:
            self.socket.close()

        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.fileno = self.socket.fileno

    def bind(self, addr):
        self.socket.bind(addr)

        group = inet_aton(addr[0])
        ip_mreq = ip_mreq_pack(group, INADDR_ANY)
        self.socket.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP, ip_mreq)

    def receive(self, dgramsize):
        dgram, addr = self.socket.recvfrom(dgramsize)
        return self._loads(dgram), addr

    def sendto(self, addr, data):
        self.socket.sendto(self._dumps(data), addr)

    def close(self):
        if self.socket:
            self.socket.close()

