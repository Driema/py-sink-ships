import random, pygame

class Board:
    def __init__(self, width):
        self.tiles_per_row = 10
        self.tile_width = width / self.tiles_per_row
        self.player_board = [[0 for x in range(self.tiles_per_row)] for y in range(self.tiles_per_row)]
        self.enemy_board = [[0 for x in range(self.tiles_per_row)] for y in range(self.tiles_per_row)]


    def init_random_player(self, boats):
        for ship in boats:
            self.assign_to_board(ship)


    def assign_to_board(self, ship):
        direction = "ver" if random.random() < 0.5 else "hor"
        if direction == "ver":
            start_range = self.tiles_per_row - ship.size
            got_start = False
            while not got_start:
                start = random.randrange(0, start_range)
                if self.player_board[start][0] == 0:
                    got_start = True
        
            got_pos = False
            while not got_pos:
                val = random.randrange(0, self.tiles_per_row)
                occ = False
                for i in range(ship.size):
                    if self.player_board[start + i][val] != 0:
                        occ = True

                if not occ:
                    for i in range(ship.size):
                        self.player_board[start + i][val] = ship.size
                    
                    got_pos = True

        else:
            start_range = self.tiles_per_row - ship.size
            got_start = False
            while not got_start:
                start = random.randrange(0, start_range)
                if self.player_board[start][0] == 0:
                    got_start = True
        

            got_pos = False
            while not got_pos:
                val = random.randrange(0, self.tiles_per_row)
                occ = False
                for i in range(ship.size):
                    if self.player_board[val][start + i] != 0:
                        occ = True

                if not occ:
                    for i in range(ship.size):
                        self.player_board[val][start + i] = ship.size
                    
                    got_pos = True


    def get_spot_from_pos(self, mouse_pos):
        x = int(int(mouse_pos[0] // self.tile_width))
        y = int(((int(mouse_pos[1]) - 440) // self.tile_width))
        if y < 0:
            y = 0
        elif y > 9:
            y = 9
        
        if x < 0:
            x = 0
        elif x > 9:
            x = 9
        
        return y, x


    def render_player_board(self, dis):
        for i, row in enumerate(self.player_board):
            for j, col in enumerate(row):
                color = (120, 120, 120)
                if col == 100:
                    color = (255, 0, 0)
                elif col == 200:
                    color = (200, 200, 200)
                elif col != 100 and col != 200 and col != 0:
                    color = (255, 40 * col, col * 50)

                pygame.draw.rect(dis, (0, 0, 0), (j * self.tile_width, i * self.tile_width, self.tile_width, self.tile_width))
                pygame.draw.rect(dis, color, (j * self.tile_width + 0.5, i * self.tile_width + 0.5, self.tile_width - 1, self.tile_width - 1))


    def render_enemy_board(self, dis):
        for i, row in enumerate(self.enemy_board):
            for j, col in enumerate(row):
                color = (120, 120, 120)
                if col == 100:
                    color = (255, 0, 0)
                elif col == 200:
                    color = (200, 200, 200)
                elif col == 420:
                    color = (230, 230, 230, 0.2)
                
                pygame.draw.rect(dis, (0, 0, 0), (j * self.tile_width, (i + self.tiles_per_row + 1) * self.tile_width, self.tile_width, self.tile_width))
                pygame.draw.rect(dis, color, (j * self.tile_width + 0.5, (i + self.tiles_per_row + 1) * self.tile_width + 0.5, self.tile_width - 1, self.tile_width - 1))