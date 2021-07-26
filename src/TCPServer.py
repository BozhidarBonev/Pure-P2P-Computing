import socket
import sys

class TCPServer:

    def __init__(self):
        self.localIP = socket.gethostbyname(socket.gethostname())
        self.localPort = 34197
        self.bufferSize = 4096
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       

    def Connect(self):
        #Bind socket to local host and port
        try:
            self.server.bind((self.localIP,self.localPort))
        except socket.error as msg:
            print ('Bind failed. Error Code : ') + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()

    def Disconnect(self):
        self.server.close()

    def Listen(self):
        self.server.listen()
        conn, addr = self.server.accept()
        while True:
            data = conn.recv(self.bufferSize)
            print( "Client sent: {}".format(data) )
            if not data:
                break
            conn.sendall("Received")

            

