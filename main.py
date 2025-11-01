import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE
from maze import Maze
from player import Player

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Maze Game")

    clock = pygame.time.Clock()
    maze = Maze()
    player = Player(0, 0, maze)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            player.handle_input(event)

        screen.fill(WHITE)
        maze.draw(screen)
        player.draw(screen)
        pygame.display.flip()
        clock.tick(10)  # FPS

    pygame.quit()

if __name__ == "__main__":
    main()
