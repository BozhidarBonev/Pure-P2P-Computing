import socket
from UDPServer import UDPServer
from UDPClient import UDPClient
from TCPServer import TCPServer
from TCPClient import TCPClient
import requests
import time
import psutil
import threading
import subprocess
import LocalIP

def singleton(c):
    return c()

@singleton
class Node:

    def __init__(self):
        self.udpClient = UDPClient(465)
        self.tcpClient = TCPClient(585)
        self.bootstrapDomain = "www.example.com"
        self.bootstrapIP = ""
        self.connections = []
        self.isBSP = False
        self.isGuardian = False
        self.guardians = []
        self.ddnsProvider = ["https://dynupdate.no-ip.com/nic/update",443]
        self.ddnsCreds = ["username","password"]
        self.myIP = LocalIP.GetLocalIP()
        
    #REGULAR NODE CODE ----------------------------------------------------------------------------------------------------

    def BootstrapClient(self):
        self.bootstrapIP = socket.gethostbyname(self.bootstrapDomain)
        reply = self.tcpClient.Send(1,self.bootstrapIP)
        if reply == 1:
            self.connections = self.tcpClient.Send(2,self.bootstrapIP)
            self.CheckBecomeGuardian()
        else:
            time.sleep(4) #seconds = maximum time needed to become BSP + random(n seconds)
            self.bootstrapIP = socket.gethostbyname(self.bootstrapDomain)
            reply =  self.tcpClient.Send(1,self.bootstrapIP)
            if reply == 1:
                self.connections = self.tcpClient.Send(2,self.bootstrapIP)
                self.CheckBecomeGuardian()
            else:
                self.BecomeBSP()

    def CheckBecomeGuardian(self):
        reply = self.tcpClient.Send(3,self.bootstrapIP)
        if reply == 1:
            time.sleep(4) #seconds = random(maximum time needed to become guardian + random(n seconds))
            reply = self.tcpClient.Send(3,self.bootstrapIP)
            if reply == 1:
                self.BecomeGuardian()

    def BecomeGuardian(self):
        if psutil.cpu_count()<= 2:
            self.tcpClient.Send(6,self.bootstrapIP)
        else:
            self.isGuardian = True
            self.bootstrapIP = socket.gethostbyname(self.bootstrapDomain)
            self.guardians = self.tcpClient.Send(4,self.bootstrapIP)
            t1 = threading.Thread(target=self.CheckGuards)
            t1.daemon = True
            t2 = threading.Thread(target=self.CheckBSP)
            t2.daemon = True
            t1.start()
            t2.start()

    #GUARDIANS CODE ----------------------------------------------------------------------------------------------------
    def BecomeBSP(self):
            if self.isGuardian == True:
                self.isBSP = True
                self.UpdateDDNS()
                for i in range(len(self.guardians)):
                    self.tcpClient.Send(5,self.guardians[i])

    def UpdateDDNS(self):
        #Must be exec no more than 1 time per minute
        r = requests.get("http://{}:{}@dynupdate.no-ip.com/nic/update?hostname={}&myip={}".format(self.ddnsCreds[0],self.ddnsCreds[1],self.ddnsProvider,self.myIP))
        if r.status_code != requests.codes.ok:
            print(r.content)

    def CheckBSP(self):
        if self.isGuardian == True:
            while True:
                self.bootstrapIP = socket.gethostbyname(self.bootstrapDomain)
                reply = self.tcpClient.Send(1,self.bootstrapIP)
                if reply != 1:
                    time.sleep(5) #seconds = random(time interval between checks + random(n seconds))
                    self.bootstrapIP = socket.gethostbyname(self.bootstrapDomain)
                    reply = self.tcpClient.Send(1,self.bootstrapIP)
                    if reply != 1:
                        self.BecomeBSP()
                        break
                else:
                    time.sleep(3) # time interval between checks
                

    def CheckGuards(self):
        if self.isGuardian == True:
            while True:
                self.bootstrapIP = socket.gethostbyname(self.bootstrapDomain)
                reply = self.tcpClient.Send(3,self.bootstrapIP)
                if reply==1:
                    time.sleep(4) #seconds = random(maximum time needed to become guardian + random(n seconds))
                    self.bootstrapIP = socket.gethostbyname(self.bootstrapDomain)
                    reply = self.tcpClient.Send(3,self.bootstrapIP)
                    if reply==1:
                        #assign random peer as guardian
                        pass


    def GetNewBSP(self,ip):
        if self.isGuardian == True:
            self.bootstrapIP = ip

    def GetNewGuardian(self,addr):
        if self.isGuardian == True:
            self.guardians.append(addr)

    #BOOTSTRAPPING NODE(BSP) CODE ----------------------------------------------------------------------------------------------------

    def CheckActiveGuards(self,addr):
        activeGuards = []
        guardsNeeded = 5 #TO DO
        for i in range(len(self.guardians)):
            if self.guardians[i] != addr:
                reply = self.tcpClient.Send(1,self.guardians[i])
                if reply == 1:
                    activeGuards.append(self.guardians[i])
        if len(activeGuards) < guardsNeeded - 1:
            return 1
        else:
            return 0

    def AnnounceNewGuardian(self,addr):
        for i in range(len(self.guardians)):
            self.tcpClient.Send(7,addr,self.guardians[i])