#!/usr/bin/env python
# -.- coding: utf-8 -.-y
import threading
import subprocess
import Queue
import socket
import time
import sys
import os
import datetime
from cmd import Cmd
#Created by Camerin Figueroa
cv = "1.1"
q = Queue.Queue()
q.put([[]])
errors = Queue.Queue()
errors.put([])
motd = Queue.Queue()
quit = Queue.Queue()
quit.put("")
mesg = Queue.Queue()
mesg.put("")
online = Queue.Queue()
online.put([])
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
port = 99999
configcont = "#Replace Everything behind = sign\n#Ex before: config = edit\n#Ex after: config = configinput\n\nmotd = Hello world This is a new Chat Room Server made by Camerin Figueroa\nport = 22550\n"
if os.path.isfile('./crsconfig.txt') == True:
    f = open('./crsconfig.txt', 'r')
    configuration = f.read()
    f.close()
    configuration = configuration.split("\n")
    for line in configuration:
        if "motd =" in line:
            motd.put(line[10:])
        else:
            pass
        if "port = " in line:
            port = int(line[7:])

        else:
            pass

else:
    f = open('./crsconfig.txt', 'w')
    f.write(configcont)
    f.close()
    print "Please edit crsconfig.txt"
    sys.exit()
if port != 99999:
    pass
else:
    f = open('./crsconfig.txt', 'w')
    f.write(configcont)
    f.close()
    print "Please edit crsconfig.txt"
    sys.exit()
def console(q, errors, motd):
    if __name__ == '__main__':
        prompt = consoleprompt()
        prompt.prompt = '> '
        prompt.cmdloop('Starting prompt...')
class consoleprompt(Cmd):
    def do_printdb(self, args):
        global q
        self.quit = quit
        db = q.get()
        q.put(db)
        tick = 0
        for line in db:
            for lin in line:
                if tick == 0:
                    for li in lin:
                        print li
                    tick = 1
                else:
                    print lin
    def do_online(self, args):
        global online
        on = online.get()
        online.put(on)
        print "Online:"
        for username in on:
            print username
    def do_printerrors(self, args):
        global errors
        erlist = errors.get()
        errors.put(erlist)
        print "Errors:"
        for error in erlist:
            print error
    def do_motd(self, args):
        if "-c" in args:
            global motd
            oldmotd = motd.get()
            motd.put(args[3:])
            print "motd changed from " + oldmotd + " to " + args[3:]
        else:
            print "add -c newcmd"
    def do_quit(self, args):
        global quit
        print "Quitting."
        quit.get()
        quit.put("quitting:")
        time.sleep(2)
        os._exit(0)
class Server(object):
    def __init__(self, host, port, q, motd, errors, mesg, quit, online):
        self.motd = motd
        self.quit = quit
        self.errors = errors
        self.host = host
        self.port = port
        self.q = q
        self.mesg = mesg
        self.online = online
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
    def listen(self):
        self.sock.listen(5)
        while True:
            try:
                client, address = self.sock.accept()
                client.settimeout(60)
                threading.Thread(target = self.listenToClient,args = (client,address)).start()
            except:
                pass
    def listenToClient(self, client, address):
        global cv
        cmd = self.motd.get()
        self.motd.put(cmd)
        rcv = client.recv(128)
        if str(cv) != rcv[3:] and "cv:" in rcv:
            client.send("comp:0:" + str(cv))
        elif rcv == "screen:":
            online = self.online.get()
            self.online.put(online)
            client.send(str(online))
            cmessage = self.mesg.get()
            self.mesg.put(cmessage)
            lm = cmessage
            tick = 0
            qi = False
            try:
                while qi == False:
                    cmessage = self.mesg.get()
                    self.mesg.put(cmessage)
                    online = self.online.get()
                    self.online.put(online)
                    if cmessage != lm:
                        csend = cmessage.split(":")
                        client.send(csend[1] + ":" + csend[2])
                        lm = cmessage
                    else:
                        pass
                    quit = self.quit.get()
                    self.quit.put(quit)
                    if tick == 1000:
                        client.send("online:" + str(online))
                        onlinecheck = client.recv(1024)
                        if onlinecheck == "quitting:":
                            quit = "quitting:"
                            qi = True
                        else:
                            pass
                        tick = 0
                    else:
                        pass
                    tick = tick + 1
                    if quit == "quitting:":
                        client.send("quitting:")
                        client.close()
                        qi = True
                    else:
                        pass
                    time.sleep(.001)
            except:
                error = self.errors.get()
                error.append("A screen raised an error")
                self.errors.put(error)
                pass
        else:
            client.send("comp:1")
            name = client.recv(1024)
            if "user:" not in name:
                client.send("error:wrong type of packet received. 'user:' was not within the packet")
                erlist = errors.get()
                erlist.append(client.getpeername() + ":wrong type of packet received. 'user:' was not within the packet")
                errors.put(erlist)
            else:
                name = name[5:]
                used = False
                online = self.online.get()
                self.online.put(online)
                for user in online:
                    if user == name:
                        used = True
                    else:
                        pass
                if used == True:
                    client.send("error:Username has already been used before.")
                    client.close()
                    erlist = errors.get()
                    erlist.append(name + ":" + name + ":Username has already been used before.")
                    errors.put(erlist)
                    check = False
                else:
                    client.send("user:" + name)
                    check = True
            if check == True:
                db = q.get()
                q.put(db)
                leng = 1
                for nam in db[0]:
                    if name in nam:
                        nl = leng
                    else:
                        leng = leng
                if 'nl' in locals():
                    db[0][nl - 1].append(address)
                else:
                    nl = leng
                    db.append([name,])
                    db[0].append([name, address])
                    q.get()
                    q.put(db)
                try:
                    online = self.online.get()
                    online.append(name)
                    self.online.put(online)
                    while True:
                            rmesg = client.recv(1024)
                            if "" == rmesg:
                                pass
                            elif "/help" == rmesg:
                                pass
                            elif "quitting:" == rmesg:
                                on = online.get()
                                on.remove(name)
                                online.put(on)
                            elif "ping:" == rmesg:
                                pass
                            else:
                                curtime = str(int(time.time()))
                                curmes = self.mesg.get()
                                if curmes.split(":")[0] == curtime:
                                    self.mesg.put(curmes)
                                else:
                                    db = q.get()
                                    db[leng].append(name + ":" + rmesg[5:])
                                    q.put(db)
                                    self.mesg.put(curtime + ":" + name + ":" + rmesg[5:])
                except:
                    online = self.online.get()
                    if name in online:
                        online.remove(name)
                    else:
                        pass
                    self.online.put(online)
            else:
                pass
def writeoutput(q, errors):
    if os.path.isdir("./logs") == False:
        subprocess.Popen(['mkdir', './logs'], stdout=subprocess.PIPE,).communicate()[0]
    else:
        pass
    tim = str(datetime.datetime.now())
    tim = tim.replace(" ", "")
    log = "./logs/log" + tim + ".txt"
    while True:
        try:
            time.sleep(10)
            tta = q.get()
            q.put(tta)
            error = errors.get()
            errors.put(error)
            fw = "Users:\n"
            errs = ""
            for err in error:
                errs = errs + err + "\n"
            for line in tta:
                for lin in line:
                    fw = fw + str(lin) + "\n"
            fw = fw + "═════════════════════════════════════════════════════════\nErrors:\n" + errs
            f = open(log, 'w')
            f.write(fw)
            f.close()
        except:
            error = errors.get()
            error.append("Error while writing output\n")
            errors.put(error)
if __name__ == "__main__":
    threading.Thread(target = writeoutput,args = (q,errors)).start()
    threading.Thread(target = console,args = (q, errors, motd)).start()
    Server('',port,q,motd,errors,mesg, quit, online).listen()
