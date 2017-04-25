# -*- coding: utf-8 -*-
import socket
from uuid import getnode as get_mac
from threading import *
from collections import deque
import time


class EndpointReader(Thread):
    end_point = None
    message_deque = deque([])

    def __init__(self, end_point):
        self.end_point = end_point
        Thread.__init__(self)

    def run(self):
        while True:
            try:
                message = self.end_point.read(32, 10000000)
                if message:
                    self.message_deque.append(message)
                else:
                    time.sleep(0.005)
            except Exception:
                print "Read timeout"
