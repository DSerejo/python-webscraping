#!/usr/bin/env python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from twisted.spread import pb
from twisted.internet import reactor
import sys
class ErrorHandler:

    def __init__(self,fileName):
        self.fileName = fileName
        self.handler = open(self.fileName, "a")
    def write(self, string):
        self.handler = open(self.fileName, "a")
        self.handler.write(string)
        self.handler.close()
    # not sure if these are necessary:
    def close(self):
        pass
    def flush(self):
        pass

class Client(pb.Referenceable):
    def __init__(self,id):
        self.id=id

    def remote_id(self):
        id = self.id
        return id
    #kwargs must contain @templatePath, that have to contain run(kwargs) function
    def remote_start(self,kwargs):
        temlate = __import__(kwargs['templatePath'], fromlist=["run"])
        resp = temlate.run(kwargs)
        d=self.server.callRemote("spiderResponse",resp)
        def s(a):
            global connect
            connect.disconnect()

            exit()
        d.addCallback(s)

    def connect(self,server):
        self.server=server
        server.callRemote("spiderConnected",self)

def main():
    f=open('teste.txt','w')
    f.write(str(sys.argv))
    f.close()
    id=sys.argv[1]
    #sys.stderr =  ErrorHandler('err.txt')
    #sys.stdout = ErrorHandler('out.txt')
    #id=0
    factory = pb.PBClientFactory()
    c = Client(id)
    global connect
    connect = reactor.connectTCP("localhost", 8800, factory)
    server = factory.getRootObject()
    server.addCallback(c.connect)
    reactor.run()


main()