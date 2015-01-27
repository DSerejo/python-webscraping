from twisted.spread import pb
from twisted.internet import reactor
from collections import deque
import subprocess,os

def handleData(kwargs):
    print (kwargs)
    pass
class CrawlerServer(pb.Root):
    def __init__(self,maxSpiders=0,workerPath='',handleData=handleData):
        self.maxSpiders=maxSpiders
        self.workerPath=workerPath
        self.scrapParamsQueue=deque()

        self.spidersRunning = 0
        self.handleData=handleData
        self.reservedParams={}
        self.checkSpidersAvailable()

    #Adding scrapParams
    #@paramsList (list(dict)) : mandatory
    def appendParams(self,paramsList):
        for params in paramsList:
            self.scrapParamsQueue.append(params)
        self.checkSpidersAvailable()
    #Receives response from spider.
    #@error(string) : optional
    #@scrapParams(dict) : mandatory -> must be the same as scrapParams received by spider on start() function
    #@another_args : optional -> any args to be processed at handleData function
    def remote_spiderResponse(self,kwargs):
        if 'error' in kwargs:
            print (kwargs['error'])
            self.scrapParamsQueue.append(kwargs['scrapParams'])
        else:
            self.spidersRunning=self.spidersRunning-1
            self.handleData(kwargs)

    #Check how many spiders are available, and start a detached process to each of them
    #Reserves scrapParams to each spider
    def checkSpidersAvailable(self):
        while self.spidersRunning<self.maxSpiders and len(self.scrapParamsQueue)>0:
            id=self.spidersRunning
            params = self.scrapParamsQueue.popleft()
            self.reservedParams.update({id:params})
            self.spidersRunning=id+1
            args = ["python.exe", self.workerPath, str(id)]
            subprocess.Popen(args, close_fds=True)

    #A new spider is now connected. Pass reserved data to it
    def remote_spiderConnected(self,spider):
        spiderId = -1
        d=spider.callRemote("id")
        def s(d):
            spiderId=d
            spider.callRemote('start',self.reservedParams[int(spiderId)])
            self.reservedParams.pop(int(spiderId))
        d.addCallback(s)



reactor.listenTCP(8800, pb.PBServerFactory(CrawlerServer(1,'C:\pyworkspace\selenium\server2\client.py',handleData)))
#reactor.listenTCP(8800, pb.PBServerFactory(CrawlerServer()))

reactor.run()
