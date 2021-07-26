from UDPServer import UDPServer
from UDPClient import UDPClient
from TCPServer import TCPServer
from TCPClient import TCPClient
class Node:

    def __init__(self):
        self.udpServer = UDPServer()
        self.udpClient = UDPClient()
        self.tcpServer = TCPServer()
        self.tcpClient = TCPClient()

    def TCPServer(self):
        self.tcpServer.Connect()
        self.tcpServer.Listen()

    def TCPClient(self,ip,port):
        self.tcpClient.Send("Hello from TCP client",ip,port)

    def UDPServer(self):
        self.udpServer.Listen()

    def UDPClient(self,ip,port):
        self.udpClient.Send("Hello from UDP client",ip,port)