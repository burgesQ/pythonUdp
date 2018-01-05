#!/usr/bin/env python3

from .ValueHandler import ValueHandler
from .Socket import Socket
from .Tester import Tester

tests = [
    # [ Title of the test, expected output, content send ]
    [ "Test one. Simple string. Expected : ", "PONG", "PING" ],
]

class Snaky :
    def __init__(self, handler : ValueHandler) :
        self.handler = handler
        self.socket  = Socket(handler)
        self.tester  = Tester(handler)

    def __enter__(self) :
        return self

    # Main loop
    def run(self) :
        count = 1
        arraySocket = []
        for test in tests :
            print("({0}) + {1} {2}.".format(count, test[0][:-1], "OK" if test[1] == 1 else "KO"))
            self.handler.append_to_ok("Test {0} : {1}\n".format(count, "OK" if test[1] == 1 else "KO"))
            self.socket.send(test[2])
            count += 1
        return self.tester.test()
