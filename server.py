#!/usr/bin/env python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from twisted.spread import pb
from twisted.internet import reactor
from collections import deque
import subprocess,psutil,random,math

class CrawlerServer(pb.Root):
    def __init__(self,maxSpiders,workerPath,handleData):
        self.maxSpiders=maxSpiders
        self.workerPath=workerPath
        self.scrapParamsQueue=deque()

        self.spidersRunning = 0
        self.handleData=handleData
        self.reservedParams={}
        self.checkSpidersAvailable()
        self.scrapedsUrls=[]

    #Adding scrapParams
    #@paramsList (list(dict)) : mandatory
    #dict->
        #  must contain @templatePath (template file to do the dirty work)
        #  must contain @url
    def appendParams(self,paramsList):
        for params in paramsList:
            self.scrapParamsQueue.append(params)
        self.checkSpidersAvailable()
    #Receives response from spider.
    #@error(string) : optional
    #@scrapParams(dict) : mandatory -> must be the same as scrapParams received by spider on start() function
    #@another_args : optional -> any args to be processed at handleData function
    def remote_spiderResponse(self,kwargs):
        p = psutil.Process(kwargs['scrapParams']['pid'])
        p.terminate()  #or p.kill()
        self.spidersRunning=self.spidersRunning-1
        if 'error' in kwargs:
            print kwargs['error']
            self.scrapParamsQueue.append([kwargs['scrapParams']])
        else:

            if 'links2add' in kwargs:
                self.appendParams(kwargs['links2add'])

            self.handleData(kwargs)
        self.checkSpidersAvailable()

    #Check how many spiders are available, and start a detached process to each of them
    #Reserves scrapParams to each spider
    def checkSpidersAvailable(self):
        while self.spidersRunning<self.maxSpiders and len(self.scrapParamsQueue)>0:
            id=int(math.floor(random.uniform(1, 10)*1000))
            params = self.scrapParamsQueue.popleft()
            while(params['url'] in self.scrapedsUrls and len(self.scrapParamsQueue)>0):
                params = self.scrapParamsQueue.popleft()
            if params['url'] in self.scrapedsUrls:
                break
            self.reservedParams.update({int(id):params})
            self.spidersRunning=self.spidersRunning+1
            args = ["python.exe", self.workerPath, str(id)]
            params['pid']= subprocess.Popen(args, close_fds=True).pid

    #A new spider is now connected. Pass reserved data to it
    def remote_spiderConnected(self,spider):
        spiderId = -1
        d=spider.callRemote("id")
        def s(d):
            spiderId=d
            spider.callRemote('start',self.reservedParams[int(spiderId)])
            self.reservedParams.pop(int(spiderId))
        d.addCallback(s)
def start(server):
    reactor.listenTCP(8800, pb.PBServerFactory(server))
    #reactor.listenTCP(8800, pb.PBServerFactory(CrawlerServer()))
    reactor.run()


