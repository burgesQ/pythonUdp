#!/usr/bin/env python3

import socket
import ssl
import time
import sys

from .ValueHandler import ValueHandler

class Socket :
    def __init__(self, handler : ValueHandler) :
        self.handler = handler
        self.array_socket = []

    def __enter__(self) :
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        for s in self.array_socket :
            try :
                s.close()
            except :
                print ("Error while closing a socket.")

    # Create / Connect socket | SetUp ssl if needed
    def set_socket(self) :
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)

            if self.handler.get_key() == None :      # if no ssl
                self.array_socket.append(s)
                try:
                    s.connect((self.handler.get_ip(), self.handler.get_port()) )
                except ConnectionRefusedError:
                    print("No server running on this address")
                    sys.exit(-1)
                return s

            else :                # else if ssl
                # Gonna ned try catch for g_key, connect, file existe
                wrappedSocket = ssl.wrap_socket(s, keyfile=self.handler.get_key(), certfile=self.handler.get_cert(), ssl_version=ssl.PROTOCOL_TLSv1)
                print('socket wrapped')
                wrappedSocket.connect((self.handler.get_ip(), self.handler.get_port()))
                print('socket connected')
                self.array_socket.append(wrappedSocket)
                return wrappedSocket

    # Send message trought socket
    def send(self, test : str) :
        s     = self.set_socket()
        i     = 0
        size  = len(test)
        value = self.handler.get_size_async() if self.handler.get_size_async() > 0 else size

        while i < size :
            b = bytearray(test[i:(i + value)].encode())
            if (self.handler.get_key() != None) :
                s.send(b)
            else :
                s.sendall(b)
            i += value
            time.sleep(0.2)
