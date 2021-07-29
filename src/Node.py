import socket
from UDPServer import UDPServer
from UDPClient import UDPClient
from TCPServer import TCPServer
from TCPClient import TCPClient
import requests
import time
import psutil
import threading
class Node:

    def __init__(self):
        self.myIP =  self.GetLocalIP()
        self.tcpPort = 585
        self.udpPort = 465
        self.udpServer = UDPServer(self.myIP,self.udpPort)
        self.udpClient = UDPClient()
        self.tcpServer = TCPServer(self.myIP,self.tcpPort)
        self.tcpClient = TCPClient(self.tcpPort)
        self.bootstrapDomain = "www.example.com"
        self.bootstrapIP = ""
        self.connections = []
        self.isBSP = False
        self.isGuardian = False
        self.guardians = []
        
    #REGULAR NODE CODE ----------------------------------------------------------------------------------------------------
  
    def GetLocalIP():
        #TO DO
        pass

    def TCPServer(self):
        self.tcpServer.Connect()
        self.tcpServer.Listen()

    def UDPServer(self):
        self.udpServer.Listen()

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
            #TO DO
            pass
        else:
            self.isGuardian = True
            self.bootstrapIP = socket.gethostbyname(self.bootstrapDomain)
            self.guardians = self.tcpClient.Send(4,self.bootstrapIP)
            #TO DO
            #launch thread on CheckGuards()
            #launch thread on CheckBSP
        

    def BecomeBSP(self):
        if self.isGuardian == True:
            self.isBSP = True
            self.UpdateDDNS()
            for i in range(len(self.guardians)):
                self.tcpClient.Send(5,self.guardians[i])

    def UpdateDDNS(self):
        #TO DO
        pass

    #GUARDIANS CODE ----------------------------------------------------------------------------------------------------

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
                

    def CheckGuards():
        #TO DO
        pass

    def GetNewBSP(self,ip):
        if self.isGuardian == True:
            self.bootstrapIP = ip


     #BOOTSTRAPPING NODE(BSP) CODE ----------------------------------------------------------------------------------------------------
