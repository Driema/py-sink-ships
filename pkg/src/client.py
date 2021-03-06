import socket, sys

class Client:
    def __init__(self):
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def connect(self):
        if len(sys.argv) < 3:
            exit()

        host = sys.argv[1]
        port = sys.argv[2]
        try:
            self.tcp_client.connect((host, int(port)))
        except:
            print("server not responding, exiting")
            return False
             
        print("connected to localhost:8641")
        return True
        
