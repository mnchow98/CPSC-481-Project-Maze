import pygame
import random
from settings import GRID_WIDTH, GRID_HEIGHT, TILE_SIZE, GREEN, GRAY, BLACK

class Maze:
    def __init__(self, width=None, height=None):
        self.width = width if width else GRID_WIDTH
        self.height = height if height else GRID_HEIGHT
        self.grid = self.generate_maze()
        
        #self._add_weighted_costs()
        
    def generate_maze(self):
        maze_width = self.width if self.width % 2 == 1 else self.width - 1
        maze_height = self.height if self.height % 2 == 1 else self.height - 1
        
        grid = [[0 for _ in range(maze_width)] for _ in range(maze_height)]
        
        self.carve_path(grid, 1, 1)
        
        grid[0][0] = 1
        grid[0][1] = 1
        grid[maze_height - 1][maze_width - 1] = 1
        grid[maze_height - 1][maze_width - 2] = 1
        
        return grid
    
    def carve_path(self, grid, x, y):
        grid[y][x] = 1
        directions = [(2,0), (0,2), (-2,0), (0,-2)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            
            if (0 <= new_x < len(grid[0]) and
                0 <= new_y < len(grid) and
                grid[new_y][new_x] == 0):
            
                wall_x, wall_y = x + dx // 2, y + dy // 2
                grid[wall_y][wall_x] = 1
            
                self.carve_path(grid, new_x, new_y)
                    
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


if __name__ == "__main__":
    test_maze = Maze(width=18, height=10)
    for y, row in enumerate(test_maze.grid):
        line = ''
        for x, cell in enumerate(row):
            if y == 0 and x == 0:
                line += 'S'  # Start
            elif y == len(test_maze.grid)-1 and x == len(row)-1:
                line += 'E'  # End
            else:
                line += '#' if cell == 0 else '.'
        print(line)