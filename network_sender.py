# -*- coding: utf-8 -*-
import socket
from uuid import getnode as get_mac
from configreader import *
from constants import *
from collections import deque


class DataSender(Thread):
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

    def send_notify_signal(self):
        self.message_deque.append([MSG_NOTIFY])

    def send_flow(self, pin, flow):
        self.message_deque.append([MSG_FLOW, pin, flow])

    def send_stop_signal(self, pin):
        self.message_deque.append([MSG_STOP_SIGNAL, pin])

