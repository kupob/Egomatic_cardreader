# -*- coding: utf-8 -*-
import socket
# from uuid import getnode as get_mac
from threading import *
from configreader import *
from collections import deque


class NetworkSender(Thread):
    # mac = get_mac()
    config = ConfigReader()
    cs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (config.get_server_host(), config.get_server_port())
    event = None

    message_deque = deque([])

    def __init__(self, event):
        self.event = event
        Thread.__init__(self)

    def run(self):
        self.cs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.cs.bind(('', self.config.get_cardreader_port()))
        self.cs.connect(self.server_address)

        while True:
            self.event.wait()
            if self.message_deque:
                message = ' '.join(str(x) for x in self.message_deque.popleft())
                try:
                    self.cs.sendto(message, self.server_address)
                except socket.error, exc:
                    print exc
            self.event.clear()

    def send_RFID(self, rfid):
        self.message_deque.append([self.config.get_message_type('MSG_RFID'), rfid])

