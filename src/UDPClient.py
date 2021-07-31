import socket
import sys


class UDPClient:

    def __init__(self):
        self.port = 465
        self.bufferSize = 1024
        try:
            self.client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        except socket.error:
            print ('Failed to create socket')
            sys.exit()


    def Send(self,msg,ip):
        print("Sending message")
        serverAddressPort   = (ip, self.port)
        bytesToSend = str.encode(msg)
        # Send to server using created UDP socket
        self.client.sendto(bytesToSend, serverAddressPort)
        msgFromServer = self.client.recvfrom(self.bufferSize)
        msg = "Message from Server {}".format(msgFromServer[0])
        print(msg)

 