#!/usr/bin/env python3

import sys
import getopt
import sys

help = """Usage : ./test [-i ip][-p port][-o output_file][-a sizeChunk][-k key.pem -c cert.pem][-h][-v]

          -i --ip      : Ip address to connect.
          -p --port    : Port to connect.
          -o --output  : Output file from the server.
          -a --async   : Asynchronus test. Must be > 0.
          -k --key     : SSL key.
          -c --cert    : SSL certificat.
          -h --help    : Display this screen.
          -v --version : Display the version of the script."""

class ValueHandler:
    def __init__(self, av : sys.argv):
        self.ok         = []             # array expected output
        self.compare    = None           # -o; output file server
        self.ip         = "localhost"    # ip address to connect
        self.port       = 4242           # port to connect
        self.async      = False          # enable async paquets
        self.size_async = 0              # size chunk async
        self.key        = None           # key.pem for SSL
        self.cert       = None           # cert.pem for SSL
        self.arguments  = av[1:]
        self.version    = "1.1"

    def __enter__(self) :
        return self

    def usage(self, val) :
        sys.stderr.write(help)
        sys.exit(val)

    def set_up(self) :
        try:
            opts, args = getopt.getopt(self.arguments,
                                       'i:p:o:a:k:c:hv',
                                       ['ip', 'port', 'output', 'async', 'key', 'cert', 'help', 'version'])
        except getopt.GetoptError as e:
            print ('\n' + str(e) + '\n')
            self.usage(-1)

        for opt, arg in opts:
            if opt in ('-h', '--help'):
                self.usage(0)
            elif opt in ('-i', '--ip'):
                self.ip = arg
            elif opt in ('-p', '--port'):
                self.port = arg
            elif opt in ('-o', '--output'):
                self.compare = arg
            elif opt in ('-a', '--async'):
                if arg.isdigit() == False or int(arg) < 1 :
                    self.usage(-1)
                self.size_async = int(arg)
            elif opt in ('-k', '--key'):
                self.key = arg
            elif opt in ('-c', '--cert'):
                self.cert = arg
            elif opt in ('-v', '--version'):
                print(self.version)
                sys.exit(0)
            else:
                self.usage(2)

    def append_to_ok(self, content : str) :
        self.ok.append(content)

    def get_key(self) -> str :
        return self.key

    def get_ip(self) -> str :
        return self.ip

    def get_port(self) -> int :
        return self.port

    def get_cert(self) -> str :
        return self.cert

    def get_size_async(self) -> int :
        return self.size_async

    def get_compare(self) -> str :
        return self.compare

    def ger_ok() :
        return self.ok

    def get_ok(i : int) :
        return self.ok[i]
