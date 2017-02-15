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
try:
    from Tkinter import *
except:
    try:
        os.system("pip install tkinter")
    except:
        print "Please Install Tkinter\nYou can do this with by typing 'pip install tkinter' or finding the library online."

import ast
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

def outputscreen(messages, online):
    rows, columns = os.popen('stty size', 'r').read().split()
    rows = int(rows)
    rows = rows - 1
    columns = int(columns)
    if len(messages) > rows:
        messages = messages[len(messages) - rows:]
        #print messages
    else:
        pass
    if len(online) > rows:
        online = online[len(online) - rows:]
        #print online
    else:
        pass
    output = []
    for line in range(rows):
        output.append(["", ""])
    tick = 0
    for message in messages:
        output[tick][0] = message
        tick = tick + 1
        #print tick
    if len(output) <= len(online):
        #print "less or equal output then online"
        for l in range(len(online) - len(output)):
            output.append(["", ""])
        #print output
        #for num in range(len(online)):
        tick = 0
        #print output
        for user in online:
            output[tick][1] = user
            tick = tick + 1
        #print output
    else:
        #print "more output then online"
        #print rows
        #for num in range(len(output)):
        tick = 0
        for user in online:
            output[tick][1] = user
            tick = tick + 1
    printout = ""
    for line in output:
        space = int(columns)
        outleng = len(line[0]) + len(line[1])
        space = space - outleng
        printout = printout + line[0] + " "*space + line[1] + "\n"
    #lab = 1
    return printout
#if args.screen:
def screenrun(username, port, server):
    #sp = args.screen
    #sp = sp.split(":")
    #user = sp[2]
    #port = int(sp[1])
    #server = sp[0]
    global cv
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (server, int(port))
    sock.connect(server_address)
    sock.send("screen:")
    #print "\33[96m Type /stop to quit\33[91m"
    quit = False
    messages = []

    online = sock.recv(1024)
    online = ast.literal_eval(online)
    tmp = online
    root = Tk()
    lab = Label(root)
    lab.pack()
    while quit == False:
        servercom = sock.recv(1024)
        #print servercom
        if servercom == "quitting:":
            quit.put("1")
            quit = True
            #os._exit(0)
        elif "online:" in servercom:
            online = ast.literal_eval(servercom[7:])
            if tmp != online:
                for line in tmp:
                    if line not in online:
                        messages.append(line + " has left the server...")
                    else:
                        pass
                for line in online:
                    if line not in tmp:
                        messages.append(line + " has joined the server...")
                    else:
                        pass
            else:
                pass
            if username not in online:
                quit = True
                sock.send("quitting:")
            else:
                sock.send("good:")
                tmp = online
                lab.config(text=outputscreen(messages, online))
                #root.after(1000, screenrun)

        else:
            messages.append(servercom)
            lab.configure(text=outputscreen(messages, online))
            #root.after(1000, )
            time.sleep(.01)
        if servercom == "ping":
            sock.send("ping:pong")
        else:
            pass
        #lab.pack()
        #root.update_idletasks()
        root.update()
#else:
#    pass
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
            os._exit(0)
        threading.Thread(target = self.ping, args=()).start()
        threading.Thread(target = self.screen, args=()).start()
        #self.screen.start()
        qu = False
        while qu == False:
            inp = raw_input(">>")
            if inp == "/quit":
                qu = True
                self.quit.put("1")
                self.sock.send("quitting:")
                self.sock.close()
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
            #os._exit(0)
            pass

        '''except:
            print """\33[91m
            ***************************************************
                  Error while initiating connecting with server
            ***************************************************
            """
            sys.exit()'''
    def ping(self):
        while True:
            if quit.empty() == False:
                break
            else:
                self.sock.send("ping:")
                time.sleep(1)
    def screen(self):
        global path
        #os.system("xterm -e python " + "./ChatRoom1.1Client.py" + " -s " + self.server + ":" + self.port + ":" + self.username)
        screenrun(self.username, self.port, self.server)
        self.qt = True
        self.quit.put("1")
def quitcheck(quit):
    while True:
        time.sleep(1)
        if quit.empty() == True:
            pass
        else:
            time.sleep(2)
            os._exit(0)
threading.Thread(target = quitcheck, args=(quit,)).start()
threading.Thread(target=connect, args=(server, port, username, quit)).start()
