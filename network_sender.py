# -*- coding: utf-8 -*-
import socket
from uuid import getnode as get_mac
from threading import *
from configreader import *
from collections import deque


class NetworkSender(Thread):
    mac = get_mac()
    config = ConfigReader()
    cs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (config.get_server_host(), config.get_server_port())

    message_deque = deque([])

    def run(self):
        self.cs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.cs.connect(self.server_address)

        while True:
            if self.message_deque:
                message = str(self.mac) + ' ' + str(self.message_deque.popleft()).strip('[]')
                try:
                    self.cs.sendto(message, self.server_address)
                except socket.error, exc:
                    print exc

    def send_RFID(self, rfid):
        self.message_deque.append([self.config.get_msg_RFID_code(), rfid])

