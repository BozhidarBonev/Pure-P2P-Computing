import socket
from UDPClient import UDPClient
from TCPClient import TCPClient
import requests
import time
import psutil
import threading
import LocalIP
from random import randrange

def singleton(c):
    return c()

@singleton
class Node:

    def __init__(self):
        self.udpClient = UDPClient()
        self.tcpClient = TCPClient()
        self.bootstrapDomain = "www.example.com"
        self.bootstrapIP = ""
        self.connections = []
        self.isBSP = False
        self.isGuardian = False
        self.guardians = []
        self.ddnsCreds = ["username","password"]
        self.myIP = LocalIP.GetLocalIP()
        self.canBeGuardian = self.CanBeGuardian()
        
    #REGULAR NODE CODE ----------------------------------------------------------------------------------------------------

    def CanBeGuardian(self):
        return psutil.cpu_count()<= 2

    def BootstrapClient(self):
        self.bootstrapIP = socket.gethostbyname(self.bootstrapDomain)
        reply = self.tcpClient.Send(1,None,self.bootstrapIP)
        if reply == 1:
            self.connections = self.tcpClient.Send(2,None,self.bootstrapIP)
            if self.canBeGuardian:
                self.CheckBecomeGuardian()
        else:
            seconds = 3 + randrange(0,5) #seconds = maximum time needed to become BSP + random(n seconds)
            time.sleep(seconds) 
            self.bootstrapIP = socket.gethostbyname(self.bootstrapDomain)
            reply =  self.tcpClient.Send(1,None,self.bootstrapIP)
            if reply == 1:
                self.connections = self.tcpClient.Send(2,None,self.bootstrapIP)
                if self.canBeGuardian:
                    self.CheckBecomeGuardian()
            else:
                self.BecomeBSP()

    def CheckBecomeGuardian(self):
        reply = self.tcpClient.Send(3,None,self.bootstrapIP)
        if reply == 1:
            seconds = 3 + randrange(0,5) #seconds = random(maximum time needed to become guardian + random(n seconds))
            time.sleep(randrange(seconds)) 
            reply = self.tcpClient.Send(3,None,self.bootstrapIP)
            if reply == 1:
                self.BecomeGuardian()

    def BecomeGuardian(self):
            self.isGuardian = True
            self.bootstrapIP = socket.gethostbyname(self.bootstrapDomain)
            self.guardians = self.tcpClient.Send(4,None,self.bootstrapIP)
            t1 = threading.Thread(target=self.CheckGuards)
            t1.daemon = True
            t2 = threading.Thread(target=self.CheckBSP)
            t2.daemon = True
            t1.start()
            t2.start()

    #GUARDIANS CODE ----------------------------------------------------------------------------------------------------

    def BecomeBSP(self):
            if self.isGuardian == True:
                if self.UpdateDDNS() == requests.codes.ok:
                    self.isBSP = True
                    self.isGuardian = False
                    self.guardians.remove(self.myIP)
                    for i in range(len(self.guardians)):
                        self.tcpClient.Send(5,None,self.guardians[i])
                else:
                    time.sleep(1)
                    if self.UpdateDDNS() == requests.codes.ok:
                        self.isBSP = True
                        self.isGuardian = False
                        self.guardians.remove(self.myIP)
                        for i in range(len(self.guardians)):
                            self.tcpClient.Send(5,None,self.guardians[i])
                    else:
                        pass
                        #THROW ERROR/SIGNAL DDNS IS DOWN

    def UpdateDDNS(self):
        #Must be exec no more than 1 time per minute
        r = requests.get("http://{}:{}@dynupdate.no-ip.com/nic/update?hostname={}&myip={}".format(self.ddnsCreds[0],self.ddnsCreds[1],self.bootstrapDomain,self.myIP))
        return r.status_code

    def CheckBSP(self):
        while self.isGuardian:
            self.bootstrapIP = socket.gethostbyname(self.bootstrapDomain)
            reply = self.tcpClient.Send(1,None,self.bootstrapIP)
            if reply != 1:
                seconds = 3 + randrange(0,5) #seconds = random(time interval between checks + random(n seconds))
                time.sleep(randrange(seconds)) 
                self.bootstrapIP = socket.gethostbyname(self.bootstrapDomain)
                reply = self.tcpClient.Send(1,None,self.bootstrapIP)
                if reply != 1:
                    self.BecomeBSP()
                    break
            else:
                time.sleep(3) # time interval between checks
                

    def CheckGuards(self):
        while self.isGuardian:
            self.bootstrapIP = socket.gethostbyname(self.bootstrapDomain)
            reply = self.tcpClient.Send(3,None,self.bootstrapIP)
            if reply==1:
                seconds = 3 + randrange(0,5) #seconds = random(maximum time needed to become guardian + random(n seconds))
                time.sleep(randrange(seconds)) 
                self.bootstrapIP = socket.gethostbyname(self.bootstrapDomain)
                reply = self.tcpClient.Send(3,None,self.bootstrapIP)
                if reply==1:
                    #assign random peer/cluster as guardian (depends on MLW)
                    break


    def GetNewBSP(self,ip):
        if self.isGuardian == True:
            self.bootstrapIP = ip
            self.guardians.remove(ip)

    def AddNewGuardian(self,addr):
        if self.isGuardian == True or self.isBSP == True:
            self.guardians.append(addr)
    
    def RemoveGuardian(self,ip):
        if self.isGuardian == True or self.isBSP == True:
            self.guardians.remove(ip)

    #BOOTSTRAPPING NODE(BSP) CODE ----------------------------------------------------------------------------------------------------

    def CheckActiveGuards(self,addr):
        activeGuards = []
        guardsNeeded = 5 #TO DO
        for i in range(len(self.guardians)):
            if self.guardians[i] != addr:
                reply = self.tcpClient.Send(1,None,self.guardians[i])
                if reply == 1:
                    activeGuards.append(self.guardians[i])
        if len(activeGuards) < guardsNeeded - 1:
            return 1
        else:
            return 0

    def GetGuardians(self):
        return self.guardians

    def AnnounceNewGuardian(self,addr):
        for i in range(len(self.guardians)):
            self.tcpClient.Send(6,addr,self.guardians[i])
            self.AddNewGuardian(addr)