import pygame
from settings import TILE_SIZE, BLUE

class Player:
    def __init__(self, x, y, maze):
        self.x = x
        self.y = y
        self.maze = maze

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy

        # Check bounds and walls
        if 0 <= new_x < len(self.maze.grid[0]) and 0 <= new_y < len(self.maze.grid):
            if self.maze.grid[new_y][new_x] != 0:
                self.x = new_x
                self.y = new_y

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.move(-1, 0)
            elif event.key == pygame.K_RIGHT:
                self.move(1, 0)
            elif event.key == pygame.K_UP:
                self.move(0, -1)
            elif event.key == pygame.K_DOWN:
                self.move(0, 1)

    def draw(self, surface):
        rect = pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(surface, BLUE, rect)
