# -*- coding: utf-8 -*-
# Egomatic conf file read module
import os.path


class ConfigReader:  # Singleton
    class __ConfigReader:
        __SERVER_HOST = ""
        __SERVER_PORT = 0
        __MSG_RFID_CODE = -1

        def __init__(self):
            file_name = '../settings.conf'

            if os.path.isfile(file_name):
                file = open(file_name, 'r')
                for line in file:
                    if line[0] == '#':
                        continue

                    line_split = line.split()

                    if not line_split:
                        continue

                    code = line_split[0]
                    value = line_split[1]

                    if code == "SERVER_HOST":
                        self.__SERVER_HOST = value
                    elif code == "SERVER_PORT":
                        self.__SERVER_PORT = int(value)
                    elif code == "MSG_RFID":
                        self.__MSG_RFID_CODE = int(value)

        def get_server_host(self):
            return self.__SERVER_HOST

        def get_server_port(self):
            return self.__SERVER_PORT

        def get_msg_RFID_code(self):
            return self.__MSG_RFID_CODE

    instance = None

    def __init__(self):
        if not ConfigReader.instance:
            ConfigReader.instance = ConfigReader.__ConfigReader()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)
