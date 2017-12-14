#!/usr/bin/env python3

import socket
import sys
import getopt
import time
import difflib
import errno
import os
import ssl

tests = [

    # simple test

    [ "Simple string. Expected : ", 1,
      "+APEND\r\n" ],
    [ "Simple string, no string. Expected : ", 1,
      "+\r\n" ],

    [ "Error message. Expected : ", 1,
      "-APEND\r\n" ],
    [ "Error message, no message. Expected : ", 1,
      "-\r\n" ],

    [ "Integer. Expected : ", 1,
      ":10\r\n" ],
    [ "Integer, minus one. Expected : ", 1,
      ":-1\r\n" ],
    [ "Integer, no value. Expected : ", 1,
      ":\r\n" ],

    [ "BulkString. Expected : ", 1,
      "$5\r\nAPEND\r\n" ],
    [ "BulkString, no string. Expected : ", 1,
      "$0\r\n\r\n" ],
    [ "BulkString, -1. Expected : ", 1,
      "$-1\r\n" ],
    [ "BulkString, 0. Expected : ", 1,
      "$0\r\n\r\n" ],

    [ "Array, 0. Expected : ", 1,
      "*0\r\n" ],
    [ "Array, -1 w/ CRLF. Expected : ", 1,
      "*-1\r\n" ],
    [ "Array, 0 w/ string. Expected : ", 1,
      "*0\r\n+APEND\r\n" ],
    [ "Array, 0 w/ integer. Expected : ", 1,
      "*0\r\n:10\r\n" ],
    [ "Array, 0 w/ bulkStrung. Expected : ", 1,
      "*0\r\n$5\r\nAPEND\r\n" ],
    [ "Multi array, 0 w/ string, integer, bulkStrung. Expected : ", 1,
      "*0\r\n+APEND\r\n:100\r\n$5\r\nAPEND\r\n" ],

    # error test

    # [ "Simple string, bad cmd. Expected : ", 0,
    #   "+foobar\r\n" ],
    # [ "Simple string, no symbole. Expected : ", 0,
    #   "foobar\r\n" ],

    # [ "Error message, no symbole. Expected : ", 0,
    #   "foobar\r\n" ],

    # [ "Integer, no symbole. Expected : ", 0,
    #   "10\r\n" ],
    # [ "Integer, letters in number. Expected : ", 0,
    #   ":1a0\r\n" ],

    # [ "BulkString, not enough char. Expected : ", 0,
    #   "$4\r\nAPEND\r\n" ],
    # [ "BulkString, integer, missing carrier return. Expected : ", 0,
    #   "$5\nAPEND\r\n" ],
    # [ "BulkString, integer, missing integer. Expected : ", 0,
    #   "$\r\nAPEN\r\n" ],

    # [ "BulkString, -1 w/ string. Expected : ", 0,
    #   "$-1\r\naa\r\n" ],
    # [ "BulkString, 0 w/ string. Expected : ", 0,
    #   "$0\r\naa\r\n" ],

    # [ "Array, 0 w/ data. Expected : ", 0,
    #   "*0\r\nazaz\r\n" ],

]

help = """Usage : ./test [-i ip][-p port][-o output_file][-a sizeChunk][-k key.pem -c cert.pem][-h]

          -i --ip      : Ip address to connect.
          -p --port    : Port to connect.
          -o --output  : Output file from the server.
          -a --async   : Asynchronus test. Must be > 0
          -k --key     : SSL key
          -c --cert    : SSL certificat
          -h --help    : Display this screen."""

def usage() :
    sys.stderr.write(help)

# Manage main | Should use a class, srsly Q..
def setUp() :

    global g_ok                 # array expected output
    global g_compare            # -o; output file server
    global g_ip                 # ip address to connect
    global g_port               # port to connect
    global g_sizeAsync          # size chunk async
    global g_key                # key.pem for SSL
    global g_cert               # cert.pem for SSL

    g_ok        = []
    g_compare   = None
    g_ip        = "localhost"
    g_port      = 4242
    g_async     = False
    g_sizeAsync = 0
    g_key       = None
    g_cert      = None
    arguments   = sys.argv[1:]

    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   'i:p:o:a:k:c:h',
                                   ['ip', 'port', 'output', 'async', 'key', 'cert', 'help'])
    except getopt.GetoptError as e:
        print ('\n' + str(e) + '\n')
        usage()
        sys.exit(-1)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(0)
        elif opt in ('-i', '--ip'):
            g_ip = arg
            print(arg)
        elif opt in ('-p', '--port'):
            g_port = arg
        elif opt in ('-o', '--output'):
            g_compare = arg
            g_ok = []
        elif opt in ('-a', '--async'):
            if arg.isdigit() == False or int(arg) < 1 :
                usage()
                sys.exit(-1)
            g_sizeAsync = int(arg)
        elif opt in ('-k', '--key'):
            g_key = arg
        elif opt in ('-c', '--cert'):
            g_cert = arg
        else:
            usage()
            sys.exit(2)

# Send message trought socket
def send(s, test) :
    i = 0
    size = len(test)
    value = g_sizeAsync if g_sizeAsync > 0 else size
    while i < size :

        b = bytearray(test[i:(i + value)].encode())

        if (g_key != None) :
            s.send(b)
        else :
            s.sendall(b)

        i += value
        time.sleep(0.2)


# Create / Connect socket | SetUp ssl if needed
def setSocket(arraySocket) :
        s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        s.settimeout(10)

        if g_key == None :      # if no ssl
            arraySocket.append(s)
            try:
                s.connect( ( g_ip, g_port) )
            except ConnectionRefusedError:
                print("No server running on this address")
                sys.exit(-1)
            return s

        else :                # else if ssl
            # Gonna ned try catch for g_key, connect, file existe
            wrappedSocket = ssl.wrap_socket(s, keyfile=g_key, certfile=g_cert, ssl_version=ssl.PROTOCOL_TLSv1)
            print('socket wrapped')
            wrappedSocket.connect((g_ip, g_port))
            print('socket connected')
            arraySocket.append(wrappedSocket)
            return wrappedSocket

# Main loop
def run() :
    count = 1
    arraySocket = []
    for test in tests :

        print("({0}) + {1} {2}.".format(count, test[0][:-1], "OK" if test[1] == 1 else "KO"))
        g_ok.append("Test {0} : {1}\n".format(count, "OK" if test[1] == 1 else "KO"))

        send(setSocket(arraySocket), test[2])

        count += 1

    for key in arraySocket :
        try :
            key.close()
        except :
            print ("okok")

# Compare the output file from the server to the expected answers
def diffFile() :
    fail = 0
    if g_compare != None :          # if -o as been actived
        time.sleep(1)
        try :
            compare = open(g_compare, 'r')
        except :
            print("Missing files")
            return -1
        i = 0
        print("Running check :")
        for line in compare :
            try :
                if line != g_ok[i] :
                    print ("Invalid test, expexted :{0}\n".format(oneLine))
                    fail += 1
            except :
                pass
            i += 1
        print("All okay" if fail == 0 else "Their is {} failed test".format(fail))
    return fail

def main() :
    setUp()
    run()
    sys.exit(diffFile())

if __name__ == "__main__":
   main()
