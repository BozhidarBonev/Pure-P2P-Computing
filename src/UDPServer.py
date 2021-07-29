import socket
import sys


class UDPServer:

    def __init__(self,ip,port):
        self.localIP = ip
        self.localPort = port
        self.bufferSize = 1024
        try:
            self.server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        except socket.error:
            print ('Failed to create socket')
            sys.exit()
        self.server.bind((self.localIP, self.localPort))
        self.bytesToSend = str.encode("Hello UDP Client")

    def Listen(self):
        print("UDP server up and listening")

        # Listen for incoming datagrams
        while(True):

            bytesAddressPair = self.server.recvfrom(self.bufferSize)

            message = bytesAddressPair[0]

            address = bytesAddressPair[1]

            clientMsg = "Message from Client:{}".format(message)
            clientIP  = "Client IP Address:{}".format(address)
            
            print(clientMsg)
            print(clientIP)   
            # Sending a reply to client
            self.server.sendto(self.bytesToSend, address)

   
