import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, GRAY, GREEN, TILE_SIZE
import pathfinding
from maze import Maze
from player import Player

def draw_foreground_texts(screen, font, lines, padding=8, margin_top=8):
    text_surfaces = [font.render(line, True, BLACK) for line in lines]
    width = max(surf.get_width() for surf in text_surfaces) + padding * 2
    height = sum(surf.get_height() for surf in text_surfaces) + padding * (len(text_surfaces) + 1)

    box_rect = pygame.Rect(10, margin_top, width, height)

    pygame.draw.rect(screen, WHITE, box_rect)
    pygame.draw.rect(screen, BLACK, box_rect, 1)

    y = margin_top + padding
    for surf in text_surfaces:
        screen.blit(surf, (10 + padding, y))
        y += surf.get_height() + padding

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Maze Game")
    font = pygame.font.Font(None, 36)

    clock = pygame.time.Clock()
    maze = Maze()
    start = (0, 0)
    end = (len(maze.grid[0]) - 1, len(maze.grid) - 1)
    player = Player(start[0], start[1], maze)

    running = True
    finished = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            player.handle_input(event)

        screen.fill(WHITE)
        maze.draw(screen)
        player.draw(screen)

        cost_line = f"Cost: {player.total_cost}"
        draw_foreground_texts(screen, font, [cost_line], padding=6, margin_top=6)

        pygame.display.flip()

        if (player.x, player.y) == end:
            finished = True
            running = False
        clock.tick(10)

    if finished:
        selected = False
        algorithm = None
        while not selected:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_u:
                        algorithm = 'ucs'
                        selected = True
                    elif event.key == pygame.K_a:
                        algorithm = 'astar'
                        selected = True
            screen.fill(WHITE)
            maze.draw(screen)
            prompt_text = "Select algorithm: U (UCS) or A (A*)"
            draw_foreground_texts(screen, font, [prompt_text], padding=10, margin_top=SCREEN_HEIGHT - 60)
            pygame.display.flip()
            clock.tick(10)

        path_ucs, visited_ucs = pathfinding.solve_ucs(maze, start, end)
        path_astar, visited_astar = pathfinding.solve_a_star(maze, start, end)

        if algorithm == 'ucs':
            first_path, first_visited, first_name = path_ucs, visited_ucs, "UCS"
            second_path, second_visited, second_name = path_astar, visited_astar, "A*"
        else:
            first_path, first_visited, first_name = path_astar, visited_astar, "A*"
            second_path, second_visited, second_name = path_ucs, visited_ucs, "UCS"

        screen.fill(WHITE)
        maze.draw(screen)
        for node in first_visited:
            x, y = node
            pygame.draw.rect(screen, GRAY, pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        for node in first_path:
            x, y = node
            pygame.draw.rect(screen, GREEN, pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        cost_user = player.total_cost
        cost_first = sum(maze.grid[y][x] for (x, y) in first_path[1:]) if first_path else 0

        lines = [f"User: {cost_user}   {first_name}: {cost_first}",
                 f"Press {'A' if second_name=='A*' else 'U'} to run {second_name}"]
        draw_foreground_texts(screen, font, lines, padding=8, margin_top=8)

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if (second_name == "A*" and event.key == pygame.K_a) or (second_name == "UCS" and event.key == pygame.K_u):
                        waiting = False
            clock.tick(10)

        screen.fill(WHITE)
        maze.draw(screen)
        for node in first_visited:
            x, y = node
            pygame.draw.rect(screen, GRAY, pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        for node in first_path:
            x, y = node
            pygame.draw.rect(screen, GREEN, pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        for node in second_path:
            x, y = node
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        cost_ucs = sum(maze.grid[y][x] for (x, y) in path_ucs[1:]) if path_ucs else 0
        cost_astar = sum(maze.grid[y][x] for (x, y) in path_astar[1:]) if path_astar else 0

        final_lines = [f"User: {cost_user}   A*: {cost_astar}   UCS: {cost_ucs}"]
        draw_foreground_texts(screen, font, final_lines, padding=8, margin_top=8)

        pygame.display.flip()

        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()
