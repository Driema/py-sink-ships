import socket, pygame, math, time, threading, datetime
from ship import *
from board import *
from client import *

class Game:
    def __init__(self):
        pygame.init()
        self.width = 400
        self.height = 840
        self.board = Board(self.width)
        self.dis = pygame.display.set_mode((self.width, self.height))
        self.boats = [Ship(2), Ship(3), Ship(3), Ship(4), Ship(5)]
        self.client = Client()
        self.hit_index = 100
        self.miss_index = 200
        self.running = True
        self.RenderThread = threading.Thread(target=self.render)
        self.GameThread = threading.Thread(target=self.play)
        self.SocketThread = threading.Thread(target=self.check_sock)


    def log(self, msg):
        d = datetime.datetime.now()
        t = d.isoformat('T')
        print(f'{t}: {msg}')


    def choose_enemy_spot(self):
        got_spot = False
        while not got_spot and self.running:
            mouse_pos = pygame.mouse.get_pos()
            y, x = self.board.get_spot_from_pos(mouse_pos)
            if pygame.mouse.get_pressed()[0] and self.board.enemy_board[y][x] == 0:
                return str(y)+str(x)


    def mark_spot(self, spot, hit=False, player=False, enemy=False):
        spot_cord = [int(i) for i in str(spot)]
        if enemy:
            self.board.enemy_board[spot_cord[0]][spot_cord[1]] = self.hit_index if hit else self.miss_index
        elif player:
            self.board.player_board[spot_cord[0]][spot_cord[1]] = self.hit_index if hit else self.miss_index


    def check_spot(self, spot):
        spot_cord = [int(i) for i in str(spot)]
        if self.board.player_board[spot_cord[0]][spot_cord[1]] != 0 and self.board.player_board[spot_cord[0]][spot_cord[1]] not in [100, 200]:
            return True

        return False


    def play(self):
        while self.running:
            data = b""
            try:
                data = self.client.tcp_client.recv(1024)
            except:
                self.log("Error")
            if data.decode("utf-8").lower() == "play":
                spot = self.choose_enemy_spot()
                self.log(f"chose spot {spot}")
                try:
                    self.client.tcp_client.send(spot.encode())
                except:
                    self.log("Error")
            elif "check" in data.decode("utf-8").lower():
                spot = data.decode("utf-8").split(" ")[1]
                is_hit = self.check_spot(spot)
                self.log(f"checked spot {spot}, hit={is_hit}")
                try:
                    self.client.tcp_client.send(str(is_hit).encode())
                except:
                    self.log("Error")
            elif data.decode("utf-8").lower() == "hitplayer":
                self.log(f"enemy hit local player on spot {spot}")
                self.mark_spot(spot, hit=True, player=True)
            elif data.decode("utf-8").lower() == "missplayer":
                self.log(f"enemy missed local player on spot {spot}")
                self.mark_spot(spot, hit=False, player=True)
            elif data.decode("utf-8").lower() == "hitenemy":
                self.log(f"hit enemy on spot {spot}")
                self.mark_spot(spot, hit=True, enemy=True)
            elif data.decode("utf-8").lower() == "missenemy":
                self.log(f"missed enemy on spot {spot}")
                self.mark_spot(spot, hit=False, enemy=True)
            elif not data:
                self.log("exiting Game Thread")
                self.running = False


    def check_events(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
    

    def render(self):
        while self.running:
            self.board.render_player_board(self.dis)
            self.board.render_enemy_board(self.dis)
            pygame.display.update()

        self.log("exiting Render Thread")


    def check_sock(self):
        while True:
            if not self.running:
                self.client.tcp_client.close()
                self.log("exiting Socket Thread")
                return


    def run(self):
        self.board.init_random_player(self.boats)
        pygame.display.set_caption("PYrates Warfare")
        connected = self.client.connect()
        if not connected:
            exit()
        
        self.log("starting Render Thread")
        self.RenderThread.start()
        self.log("starting Game Thread")
        self.GameThread.start()
        self.log("starting Socket Thread")
        self.SocketThread.start()
        self.check_events()

        
