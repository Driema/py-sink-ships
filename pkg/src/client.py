import socket

class Client:
    def __init__(self):
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def connect(self):
        try:
            self.tcp_client.connect(("localhost", 8641))
        except:
            print("server not responding, exiting")
            return False
             
        print("connected to localhost:8641")
        return True
        
