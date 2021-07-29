import socket
import sys
import pickle
import time
    #------Server Communication Channels----------
    # 1 - check if actiev
    # 2 - get connections from BSP at bootstrap
    # 3 - are there enough guardians?
    # 4 - get guardians list
    # 5 - tell guardians I am new BSP
    # 6 - 
    # 7 - 
    # 8 -

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

    def Send(self,msg,ip):
        try:
            self.client.connect((ip,self.tcpPortort))
            self.client.sendall(pickle.dumps(msg))
            reply = pickle.loads(self.client.recv(self.bufferSize))
            print(reply)
            self.Disconnect()
            return reply
        except socket.error as msg:
            print ('Send/Connect Failed')

    #TO DO - NAT Traversal


#TESTING PURPOSES              
if __name__ == '__main__':
    tcp = TCPClient()
    tcp.Send(1,"192.168.1.xx",585)
    tcp.Disconnect()
