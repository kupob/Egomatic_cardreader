# -*- coding: utf-8 -*-
import socket
from uuid import getnode as get_mac
from threading import *
from collections import deque


class EndpointReader(Thread):
    end_point = None
    message_deque = deque([])

    def __init__(self, end_point):
        self.end_point = end_point
        Thread.__init__(self)

    def run(self):
        while True:
            message = self.end_point.read(32, 1000000)
            if message:
                self.message_deque.append(message)
