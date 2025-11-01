import pygame
from settings import TILE_SIZE, GREEN, GRAY, BLACK

class Maze:
    def __init__(self):
        # 2 = goal, 1 = wall, 0 = open space
        self.grid = [
            [0,0,1,0,0,0,1,0,0,0],
            [1,0,1,0,1,0,1,0,1,0],
            [1,0,0,0,1,0,0,0,1,1],
            [0,0,1,1,1,1,1,0,1,0],
            [0,1,1,0,0,0,1,1,1,0],
            [0,0,0,0,1,0,0,0,0,0],
            [1,1,0,1,1,0,1,1,1,0],
            [0,0,0,0,1,0,0,0,1,0],
            [0,1,1,1,1,1,1,0,1,0],
            [0,0,0,1,0,0,0,0,1,2],
        ]

    def draw(self, surface):
        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                if tile == 1:
                    color = "BLACK"
                elif tile == 2:
                    color = "GREEN"
                else:
                    color = "GRAY"

                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(surface, color, rect)
