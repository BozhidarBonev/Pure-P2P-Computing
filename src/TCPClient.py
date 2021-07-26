import socket
import sys

class TCPClient:

    def __init__(self):
        self.bufferSize = 4096
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print ('Failed to create socket')
            sys.exit()

    def Disconnect(self):
        self.client.close()

    def Send(self,msg,ip,port):
        self.client.connect((ip,port))
        try :
            self.client.sendall(msg)
        except socket.error:
            print ('Send failed')
            sys.exit()
        reply = self.client.recv(self.bufferSize)
        print(reply)
