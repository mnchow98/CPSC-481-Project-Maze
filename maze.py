import pygame
import random
from settings import GRID_WIDTH, GRID_HEIGHT, TILE_SIZE, GREEN, GRAY, BLACK

class Maze:
    def __init__(self, width=None, height=None):
        self.width = width if width else GRID_WIDTH
        self.height = height if height else GRID_HEIGHT
        self.grid = self.generate_maze()
        
        self.add_weighted_costs()
        
        self.wall_sprite = pygame.image.load('assets/wall.jpg')
        self.wall_sprite = pygame.transform.scale(self.wall_sprite, (TILE_SIZE, TILE_SIZE))
        
        self.grass_sprite = pygame.image.load('assets/grass.jpg')
        self.grass_sprite = pygame.transform.scale(self.grass_sprite, (TILE_SIZE, TILE_SIZE))
        
        self.mud_sprite = pygame.image.load('assets/mud.jpg')
        self.mud_sprite = pygame.transform.scale(self.mud_sprite, (TILE_SIZE, TILE_SIZE))
        
        self.rock_sprite = pygame.image.load('assets/rock.jpg')
        self.rock_sprite = pygame.transform.scale(self.rock_sprite, (TILE_SIZE, TILE_SIZE))
        
    def generate_maze(self):
        maze_width = self.width if self.width % 2 == 1 else self.width - 1
        maze_height = self.height if self.height % 2 == 1 else self.height - 1
        
        grid = [[0 for _ in range(maze_width)] for _ in range(maze_height)]
        
        self.carve_path(grid, 1, 1)
        
        grid[0][0] = 1
        grid[0][1] = 1
        grid[maze_height - 1][maze_width - 1] = 1
        grid[maze_height - 1][maze_width - 2] = 1

        self.add_complexity(grid, loop_prob=0.08, extend_prob=0.18, max_extend_len=6)
        
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

    def add_complexity(self, grid, loop_prob=0.08, extend_prob=0.18, max_extend_len=6):
        height = len(grid)
        width = len(grid[0])

        for y in range(1, height - 1):
            for x in range(1, width - 1):
                if grid[y][x] == 0:
                    if grid[y][x-1] != 0 and grid[y][x+1] != 0:
                        if random.random() < loop_prob:
                            grid[y][x] = 1
                    elif grid[y-1][x] != 0 and grid[y+1][x] != 0:
                        if random.random() < loop_prob:
                            grid[y][x] = 1

        dead_ends = []
        for y in range(height):
            for x in range(width):
                if grid[y][x] != 0:
                    neighbors = 0
                    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] != 0:
                            neighbors += 1
                    if neighbors == 1:
                        dead_ends.append((x,y))

        for (x, y) in dead_ends:
            if random.random() >= extend_prob:
                continue
            directions = [(-1,0),(1,0),(0,-1),(0,1)]
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if not (0 <= nx < width and 0 <= ny < height):
                    continue
                if grid[ny][nx] == 0:
                    length = random.randint(1, max_extend_len)
                    carved = 0
                    cx, cy = nx, ny
                    while carved < length and 0 <= cx < width and 0 <= cy < height and grid[cy][cx] == 0:
                        grid[cy][cx] = 1
                        carved += 1
                        cx += dx
                        cy += dy

    def add_weighted_costs(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.grid[y][x] == 1:
                    rand = random.random()
                    
                    if rand < 0.15:
                        self.grid[y][x] = 5
                    elif rand < 0.35:
                        self.grid[y][x] = 3

    def get_grid(self):
        return self.grid

    def get_cost(self, pos):
        x, y = pos
        return self.grid[y][x]

    def get_valid_neighbors(self, pos):
        (x, y) = pos
        neighbors = []
        width = len(self.grid[0])
        height = len(self.grid)
        if x > 0 and self.grid[y][x-1] != 0:
            neighbors.append((x-1, y))
        if x < width - 1 and self.grid[y][x+1] != 0:
            neighbors.append((x+1, y))
        if y > 0 and self.grid[y-1][x] != 0:
            neighbors.append((x, y-1))
        if y < height - 1 and self.grid[y+1][x] != 0:
            neighbors.append((x, y+1))
        return neighbors

    def draw(self, surface):
        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                if tile == 0:
                    surface.blit(self.wall_sprite, (x * TILE_SIZE, y * TILE_SIZE))
                elif tile == 1:
                    surface.blit(self.grass_sprite, (x * TILE_SIZE, y * TILE_SIZE))
                elif tile == 3:
                    surface.blit(self.mud_sprite, (x * TILE_SIZE, y * TILE_SIZE))
                elif tile == 5:
                    surface.blit(self.rock_sprite, (x * TILE_SIZE, y * TILE_SIZE))



if __name__ == "__main__":
    maze = Maze(width=39, height=23)
    symbols = {0: '#', 1: '.', 3: '~', 5: '^'}
    for row in maze.grid:
        print(''.join([symbols.get(cell, '?') for cell in row]))
