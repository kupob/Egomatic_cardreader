# -*- coding: utf-8 -*-
import socket
from uuid import getnode as get_mac
from threading import *
from collections import deque
import time


class EndpointWriter(Thread):
    end_point = None
    event = None
    message_deque = deque([])

    def __init__(self, end_point, event):
        self.end_point = end_point
        self.event = event
        Thread.__init__(self)

    def run(self):
        while True:
            self.event.wait()
            if self.message_deque:
                message = self.message_deque.popleft()
                self.end_point.write(message)
                # print "SENT " + str(time.time())
            self.event.clear()

    def send_greeting(self):
        # write the data
        ba = bytearray()
        ba.append(0xF2)
        ba.append(0xFF)
        ba.append(3)
        ba.append(1)
        ba.append(0)
        ba.append(32)
        cs = 3
        cs ^= 1
        cs ^= 0
        cs ^= 32
        ba.append(cs)
        self.message_deque.append(ba)

    def send_card_request(self):
        # write the data
        ba = bytearray()
        ba.append(0xF2)
        ba.append(0xFF)
        ba.append(1)
        ba.append(2)
        cs = 1
        cs ^= 2
        ba.append(cs)
        self.message_deque.append(ba)



