# -*- coding: utf-8 -*-
import socket
from uuid import getnode as get_mac
from threading import *
from collections import deque
from time import sleep


class EndpointWriter(Thread):
    end_point = None
    message_deque = deque([])

    def __init__(self, end_point):
        self.end_point = end_point
        Thread.__init__(self)

    def run(self):
        while True:
            if self.message_deque:
                message = self.message_deque.popleft()
                self.end_point.write(message)
                print "SEND" + str(message)
            else:
                sleep(0.1)

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
