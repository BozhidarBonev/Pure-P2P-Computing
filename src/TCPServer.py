
import socket
import subprocess
import sys
import pickle
import psutil
import Node
import LocalIP
"""
    ------Server Communication Channels----------

        #-----General Channels-----#
        # 1 - Check node activity



        #-----BSP and Guardian Channels-----#
        # 2 - Get connections from BSP at bootstrap(Join network)
        # 3 - Should I become guardian?
        # 4 - Announce becoming guardian
        # 5 - Announce becoming BSP
        # 6 - Send new guardian's IP to other guardians 



        #-----Work Channels-----#
        # 7 - 
        # 8 -

"""



class TCPServer:

    def __init__(self):
        self.localPort = 585
        self.localIP = LocalIP.GetLocalIP()
        print(self.localIP)
        self.bufferSize = 4096
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def Connect(self):
        try:
            self.server.bind((self.localIP,self.localPort))
        except socket.error as msg:
            print ('Bind failed. Error Code : ') + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()

    def Disconnect(self):
        self.server.close()

    def Listen(self):
        node = Node.Node
        self.server.listen()
        while True:
            try:
                conn, addr = self.server.accept()
                data = pickle.loads(conn.recv(self.bufferSize))
                print( "Client sent: {}".format(data) )
                if not data:
                    continue


                #-----General Channels-----#
                if data[0] == 1:
                    conn.send(pickle.dumps(1))
                    



                #-----BSP and Guardian Channels-----#
                if data[0] == 2:
                    #MLW
                    #TO DO
                    pass
                if data[0] == 3:
                    reply = node.CheckActiveGuards(addr)
                    conn.sendall(pickle.dumps(reply))
                if data[0] == 4:
                    guards = node.GetGuardians()
                    conn.sendall(pickle.dumps(guards))
                    node.AnnounceNewGuardian(addr)
                if data[0] == 5:
                    node.GetNewBSP(addr)
                if data[0] == 6:
                    node.AddNewGuardian(data[1])



                #-----Work Channels-----#


                conn.close()
            except EOFError:
                continue
            except socket.error:
                print("Error")
        
      
#TESTING PURPOSES            
if __name__ == '__main__':
    tcp = TCPServer()
    tcp.Connect()
    tcp.Listen()
    sys.exit()
