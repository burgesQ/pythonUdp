#!/usr/bin/env python3

import difflib
from time import sleep

from .ValueHandler import ValueHandler

class Tester:
    def __init__(self, handler : ValueHandler):
        self.handler = handler
        pass

    # Compare the output file from the server to the expected answers
    def diffFile(self) :
        fail = 0
        if self.handler.get_compare != None :          # if -o as been actived
            sleep(1)
            try :
                compare = open(self.handler.get_compare(), 'r')
            except :
                print("Missing files")
                return -1
            i = 0
            print("Running check :")
            for line in compare :
                try :
                    if line != self.handler.get_ok(i) :
                        print ("Invalid test, expected :{0}\n".format(oneLine))
                        fail += 1
                except :
                    pass
                i += 1
                print("All okay" if fail == 0 else "Their is {} failed test".format(fail))
        return fail
