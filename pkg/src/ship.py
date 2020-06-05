import pygame


class Ship:
    def __init__(self, size):
        self.size = size
        self.positions = [[0, 0] for x in range(self.size)]
