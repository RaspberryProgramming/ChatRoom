#!/usr/bin/env python
# -.- coding: utf-8 -.-y
import random
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
tick = Queue.Queue()
path = os.path.realpath(__file__)
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--screen", help="This is used by the script to make a screen. Not necessarily needed for regular users.")
args = parser.parse_args()
cv = "1.1"
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
    def __init__(self, server, port, username, quit, tick):
        self.tick = tick
        self.quit = quit
        self.server = server
        self.port = port
        self.username = username
        self.con()
    def con(self):
        #try:
        global cv
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server_address = (self.server, int(self.port))
            self.sock.connect(server_address)
        except:
            print "Error...\nUnable to connect to " + self.server
            os._exit(0)
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
            os._exit(0)
        self.sock.send("user:" + str(random.randint(0, 9999999)))
        nc = self.sock.recv(1024)
        if "error:" in nc:
            print """\33[91m
            ***************************************************
                  Error while sending username:
                  """ + nc[6:] + """
            ***************************************************
            """
            os._exit(0)
        #threading.Thread(target = self.ping, args=()).start()
        threading.Thread(target = self.con, args=()).start()
        #self.screen.start()
        quit = False
        while True:
            #inp = raw_input(">>")
            #time.sleep(.2)
            #send = str(random.randint(0, 9))
            #self.sock.send(send)
            #print send
            time.sleep(1)
        else:
            os._exit(0)
def quitcheck(quit):
    while True:
        time.sleep(1)
        if quit.empty() == True:
            pass
        else:
            os._exit(0)
threading.Thread(target = quitcheck, args=(quit,)).start()
threading.Thread(target=connect, args=(server, port, username, quit, tick)).start()
