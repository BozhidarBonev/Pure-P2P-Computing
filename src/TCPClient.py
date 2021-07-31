import socket
import sys
import pickle
import time

class TCPClient:

    def __init__(self,port):
        self.bufferSize = 4096
        self.tcpPort = port
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print ('Failed to create socket')
            sys.exit()

    def Disconnect(self):
        self.client.close()

    def Send(self,channel,msg,ip):
        try:
            self.client.connect((ip,self.tcpPort))
            self.client.sendall(pickle.dumps([channel,msg]))
            reply = pickle.loads(self.client.recv(self.bufferSize))
            print(reply)
            self.Disconnect()
            return reply
        except EOFError:
            pass
        except socket.error:
            print ('Send/Connect Failed')

    #TO DO - NAT Traversal


#TESTING PURPOSES              
if __name__ == '__main__':
    tcp = TCPClient(585)
    tcp.Send(7,"ko staa","192.168.1.12")
    tcp.Disconnect()
