#!/usr/bin/env python2

import socket, select, random, signal, errno

CONNECTION_LIST = []
PORT = 17

with open("quotes.txt") as f:
    quotes = ["\n{}\n\n".format(a.strip()) for a in f.read().split("\n\n")]

def reload(*args):
    pass

signal.signal(signal.SIGHUP, reload)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", PORT))
s.listen(10)

CONNECTION_LIST.append(s)

try:
    while 1:
        try:
            read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
        except select.error, v:
            break
        for sock in read_sockets:
            if sock == s:
                client, addr = s.accept()
                CONNECTION_LIST.append(client)
                try:
                    picked = random.choice(quotes)
                    client.send(picked)
                    client.close()
                    CONNECTION_LIST.remove(client)
                    print "Sent {}... to {}:{}".format(picked[:20].replace("\n", " "), *addr)
                except:
                    client.close()
                    CONNECTION_LIST.remove(client)
                    print "Exception while sending to {}:{}".format(*addr)
                    continue
except KeyboardInterrupt:
    print " Interrupt received, aborting"
finally:
    for sock in CONNECTION_LIST:
        sock.close()
