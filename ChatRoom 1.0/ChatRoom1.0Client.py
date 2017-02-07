#!/usr/bin/env python
# -.- coding: utf-8 -.-y
import socket
import os
import time
import threading
import Queue
import sys
import argparse
from multiprocessing import Process
print """\33[91m
═════════════════════════════════════════════════════════
                ███████    ██████         ███████
               █           █     █       █ ║
              █            █════╗ █   ╔═█  ║
             █═════════════█    ╚█    ║█═══╝
             █             ██████     ║█
              █            █   █      ╚╗█  ╔═══════Server
               █════════╗  █    █      ╚═█ ║
                ███████ ║  █     █        ███████
Chat Room Client════════╝
═════════════════════════════════════════════════════════
\33[92m"""
quit = Queue.Queue()
path = os.path.realpath(__file__)
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--screen", help="This is used by the script to make a screen. Not necessarily needed for regular users.")
args = parser.parse_args()
if args.screen:
    sp = args.screen
    sp = sp.split(":")
    port = int(sp[1])
    server = sp[0]
    try:
        global cv
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (server, port)
        sock.connect(server_address)
        sock.send("screen:")
        print "\33[96m Type /stop to quit\33[91m"
        quit = False
        while quit == False:
                screenprint = sock.recv(1024)
                if screenprint == "quitting:":
                    os._exit(0)
                else:
                    print screenprint
                    time.sleep(.01)
    except:
        print "ERROR"
        sys.exit()
else:
    pass
cv = "1.0"
username = raw_input("Name:")
server = raw_input("Server IP[127.0.0.1]:")
port = raw_input("Server Port[22550]:")
if port == "":
    port = "22550"
else:
    pass
if server == "":
    server = "127.0.0.1"
else:
    pass
print port
class connect(object):
    def __init__(self, server, port, username, quit):
        self.quit = quit
        self.server = server
        self.port = port
        self.username = username
        self.con()
    def con(self):
        #try:
        global cv
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.server, int(self.port))
        self.sock.connect(server_address)
        self.sock.settimeout(60)
        self.sock.send("cv:" + cv)
        compatible = self.sock.recv(1024)
        if compatible == "comp:1":
            pass
        else:
            print """\33[91m
            ***************************************************
                  Error Server is on version """ + compatible[7:] + """
            ***************************************************
            """
            sys.exit()
        self.sock.send("user:" + self.username)
        nc = self.sock.recv(1024)
        if "error:" in nc:
            print """\33[91m
            ***************************************************
                  Error while sending username:
                  """ + nc[6:] + """
            ***************************************************
            """
        threading.Thread(target = self.screen, args=()).start()
        #self.screen.start()
        quit = False
        while quit == False:
            inp = raw_input(">>")
            if inp == "/quit":
                quit = True
            elif "" == inp:
                """\33[91m
                ***************************************************
                      Error no message entered
                ***************************************************
                """
            elif "/help" == inp:
                """\33[91m
                ***************************************************
                      Error no help menu implemented yet
                ***************************************************
                """
            else:
                self.sock.send("mesg:" + inp)
        else:
            os._exit(0)

        '''except:
            print """\33[91m
            ***************************************************
                  Error while initiating connecting with server
            ***************************************************
            """
            sys.exit()'''
    def screen(self):
        global path
        os.system("xterm -e python " + "./ChatRoom1.0Client.py" + " -s " + self.server + ":" + self.port)
        self.quit.put("1")
def quitcheck(quit):
    while True:
        time.sleep(1)
        if quit.empty() == True:
            pass
        else:
            os._exit(0)
threading.Thread(target = quitcheck, args=(quit,)).start()
threading.Thread(target=connect, args=(server, port, username, quit)).start()
'''while True:
    time.sleep(1)
    print "quitcheck..."
    print quit.empty()
    if quit.empty() == True:
        pass
    else:
        print "1"
        os._exit(0)
'''
