#!/usr/bin/env python
# -.- coding: utf-8 -.-y
import socket
import math
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
parser.add_argument("-s", "--server", help="This is used to add the server and port via an argument instead of using the UI within the script.\nEX: -s server.ip:12345\n    OR -s server.ip")
parser.add_argument("-u", "--username", help="This is used to add the user via an argument instead of using the UI within the script.\nEX: -s USERNAME")
args = parser.parse_args()

if args.server:
    if ":" in args.server:
        server = args.server.split(":")[0]
        port = args.server.split(":")[1]
    else:
        server = args.server
        port = "22550"
        if port == "":
            port = "22550"
        else:
            pass
        if server == "":
            server = "127.0.0.1"
        else:
            pass
    if args.username:
        username = args.username
    else:
        username = raw_input("Name:")
else:
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

def outputscreen(messages, online):
    rows = 24
    columns = 38
    display = []
    for row in range(rows):
        display.append([])
        for column in range(columns):
            display[row].append("")
    messnum = 0
    for message in messages:
        mlines = int(math.ceil(len(message)/columns))
        if mlines  == 0:
            mlines = 1
        else:
            pass
        for lin in range(mlines):
            charnum = 0
            for char in message:
                if charnum > columns - 1:
                    messnum = messnum + 1
                    charnum = 0
                else:
                    pass
                display[messnum][charnum] = char
                charnum = charnum + 1
        messnum = messnum + 1
    rownum = 0
    for user in online:
        if len(user) > 8:
            user = " " + user[:8]
        else:
            user = " " + user
        for char in user:
            display[rownum].append(char)
        rownum = rownum + 1
    for rownum in range(len(display)):
        if len(display[rownum]) < columns + 9:
            add = columns + 9 - len(display[rownum])
            for num in range(add):
                display[rownum].append("")
        elif len(display[rownum]) > columns + 9:
            remove = columns + 9 - lendisplay[rownum]
            for num in range(remove):
                print "1"
        else:
            pass

    send = ""
    for line in display:
        for l in line:
            if l != "":
                send = send + l
            else:
                send = send + " "
        send = send + "\n"
    f = open("./outf", "w")
    f.write(send)
    f.close()
    return send
def screenrun(username, port, server, quit):
    global cv
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (server, int(port))
    sock.connect(server_address)
    sock.send("screen:")
    qu = False
    messages = []
    online = sock.recv(1024)
    online = ast.literal_eval(online)
    tmp = online
    root = Tk()
    lab = Label(root)
    lab.pack()
    while qu == False:
        servercom = sock.recv(1024)
        if servercom == "quitting:":
            quit.put("Server Shutting Down...")
            qu = True
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
                qu = True
                try:
                    sock.send("quitting:")
                except:
                    quit.put("Server already shutdown...")
            else:
                sock.send("good:")
                tmp = online
                lab.config(text=outputscreen(messages, online))

        else:
            messages.append(servercom)
            lab.configure(text=outputscreen(messages, online))
            time.sleep(.01)
        if servercom == "ping":
            sock.send("ping:pong")
        else:
            pass
        root.update()
cv = "1.1"

class connect(object):
    def __init__(self, server, port, username, quit):
        self.quit = quit
        self.server = server
        self.port = port
        self.username = username
        self.con()
    def con(self):
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
        qu = False
        while qu == False:
            inp = raw_input(">>")
            if inp == "/quit":
                qu = True
                self.quit.put(1)
                self.sock.send("quitting:")
                self.sock.close()
            elif "" == inp:
                print """\33[91m
                ***************************************************
                      Error no message entered
                ***************************************************
                """
            elif "/help" == inp:
                print """\33[91m
                ***************************************************
                      Error no help menu implemented yet
                ***************************************************
                """
            else:
                try:
                    self.sock.send("mesg:" + inp)
                except:
                    quit.put("Server disconnected out of nowhere")
                    self.sock.close()
        else:
            pass
    def ping(self):
        while True:
            if quit.empty() == False:
                break
            else:
                try:
                    self.sock.send("ping:")
                except:
                    quit.put("Ping Fail")
                time.sleep(1)
    def screen(self):
        global path
        screenrun(self.username, self.port, self.server, self.quit)
        self.qt = True
        self.quit.put("1")
def quitcheck(quit):
    while True:
        time.sleep(1)
        if quit.empty() == True:
            pass
        else:
            quitreason = quit.get()
            quit.put(quitreason)
            if quitreason == 1 or quitreason == "1":
                print "\33[97mThanks for using ChatRoom"
            else:
                print "\33[97mQuitting because " + quitreason
            time.sleep(2)
            os._exit(0)
threading.Thread(target = quitcheck, args=(quit,)).start()
threading.Thread(target=connect, args=(server, port, username, quit)).start()
