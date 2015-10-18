#!/usr/bin/env python2

import socket, select, random

CONNECTION_LIST = []
PORT = 17

def get_quotes():
    with open("quotes.txt") as f:
        return ["\n{}\n\n".format(a.strip()) for a in f.read().split("\n\n")]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", PORT))
s.listen(10)

CONNECTION_LIST.append(s)

try:
    while 1:
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
        for sock in read_sockets:
            if sock == s:
                client, addr = s.accept()
                CONNECTION_LIST.append(client)
                try:
                    quotes = get_quotes()
                    picked = random.choice(quotes) if len(quotes) > 1 else "\n<blha303> Hm, doesn't seem to be any quotes. Want to add one? http://qotd.home.blha303.biz\n\n"
                    client.send(picked)
                    client.close()
                    CONNECTION_LIST.remove(client)
                    print "Sent {}... to {}:{}".format(picked[:20].replace("\n", " "), *addr)
                except Exception, e:
                    client.close()
                    CONNECTION_LIST.remove(client)
                    print "Exception while sending to {}:{}".format(*addr)
                    print e.message
                    continue
except KeyboardInterrupt:
    print " Interrupt received, aborting"
finally:
    for sock in CONNECTION_LIST:
        sock.close()
