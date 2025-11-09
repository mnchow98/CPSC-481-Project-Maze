import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
from maze import Maze
from player import Player

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Maze Game")
    font = pygame.font.Font(None, 36)

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
        
        # Cost display with white background
        cost_text = font.render(f"Cost: {player.total_cost}", True, BLACK)
        text_rect = cost_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        pygame.draw.rect(screen, WHITE, text_rect.inflate(10, 5))
        screen.blit(cost_text, text_rect)
        
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()
