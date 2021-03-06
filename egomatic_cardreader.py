# -*- coding: utf-8 -*-

import sys
sys.path.remove('/usr/local/lib/python2.7/dist-packages')
sys.path.insert(0, '/usr/local/lib/python2.7/dist-packages')

import usb.core
import usb.util
from endpoint_reader import *
from endpoint_writer import *
from network_sender import *
import time
import threading
from math import pow as math_pow

# find our device
dev = usb.core.find(idVendor=0x04d8, idProduct=0x000a)

# was it found?
if dev is None:
    raise ValueError('Device not found')

if dev.is_kernel_driver_active(0):
    reattach = True
    dev.detach_kernel_driver(0)

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

# get an endpoint instance
cfg = dev.get_active_configuration()

writer = None
writer_event = threading.Event()
readers = {}

for cfg in dev:
    for i in cfg:
        for e in i:
            # print e.bEndpointAddress
            if usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT:
                writer = EndpointWriter(e, writer_event)
                writer.daemon = True
                writer.start()
            else:
                reader = EndpointReader(e)
                reader.daemon = True
                reader.start()
                readers[e.bEndpointAddress] = reader

sender_event = threading.Event()
net_sender = NetworkSender(sender_event)
net_sender.daemon = True
net_sender.start()

reader_states = {
    0x00 : "Reader ok. No card",
    0x01 : "Reader error",
    0x02 : "Pull timeout from PC",
    0x04 : "Checksum error",
    0x08 : "Input buffer overflow",
    0x10 : "Reserved for error code",
    0x40 : "Reserved for error code",
    0x20 : "Reserved for error code",
    0x80 : "Reader ok. Card data available",
}

if not writer:
    print "Error: no OUT endpoint"
    quit()

last_timeout_time = 0

writer.send_greeting()
writer_event.set()
while True:
    current_time = int(time.time() * 1000)
    if current_time - last_timeout_time > 40:
        writer.send_card_request()
        last_timeout_time = current_time
    elif current_time - last_timeout_time < 30:
        writer_event.set()
        time.sleep(0.002)

    for e_address in readers:
        reader = readers[e_address]
        while reader.message_deque:
            message_array = reader.message_deque.popleft()
            # print message_array

            if message_array[0] != 0xF2:   # Invalid start byte... skeep
                continue
            if message_array[1] != 0xFF:  # Invalid start byte... skeep
                continue

            length = message_array[2]
            cmd = message_array[3]
            packet = message_array[0:4 + length]

            if cmd != 0xF0:  # Invalid command type, want 0xF0. Skeep
                continue

            reader_state = packet[4]
            reader_type = packet[5]
            code_length = packet[6]
            cs = packet[length + 3]

            cs_calc = length
            cs_calc ^= cmd
            for i in range(4, length + 3):
                cs_calc ^= packet[i]

            if cs != cs_calc:
                print "Check sum error, got = " + str(cs) + ", but calculated = " + str(cs_calc)
                continue

            reader_state_string = reader_states[reader_state]

            if reader_state == 0x02:
                writer.send_greeting()
            elif reader_state == 0x80:
                code = packet[7:7 + code_length/8]
                code_int = 0
                for i in range(0, code_length/8):
                    code_int += int(code[i] * math_pow(1024, code_length/8 - 1 - i))
                net_sender.send_RFID(code_int)
                sender_event.set()
