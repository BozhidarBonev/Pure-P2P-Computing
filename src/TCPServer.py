import socket
import sys
import pickle
#from Node import Node
class TCPServer:

    def __init__(self,ip,port):
        self.localPort = port
        self.localIP = ip
        self.bufferSize = 4096
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.node = Node()

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
        while True:
            try:
                conn, addr = self.server.accept()
                data = pickle.loads(conn.recv(self.bufferSize))
                print( "Client sent: {}".format(data) )
                if not data:
                    break
                if data == 1:
                    conn.send(pickle.dumps(1))
                    
                if data == 2:
                    #MLW TO DO
                    pass
                    connections = ["192.168.1.xx","10.0.0.xx"]
                    conn.sendall(pickle.dumps(connections))
                if data == 3:
                    #Bootstapping Node TO DO
                    conn.sendall("Received")
                if data == 4:
                    #Bootstapping TO DO
                    conn.sendall("Received")
                if data == 5:
                    #Bootstapping TO DO
                    conn.sendall("Received")
            except EOFError:
                continue
            except socket.error:
                print("Error")
        conn.close()
        
      
#TESTING PURPOSES            
if __name__ == '__main__':
    tcp = TCPServer("192.168.1.xx")
    tcp.Connect()
    tcp.Listen()
    sys.exit()
