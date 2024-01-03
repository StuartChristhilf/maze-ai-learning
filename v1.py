import pygame

# Define maze parameters
MAZE_WIDTH = 50
MAZE_HEIGHT = 50
CELL_SIZE = 10
MAZE = [[1] * MAZE_WIDTH for _ in range(MAZE_HEIGHT)]  # Initialize with walls

# Pygame setup
pygame.init()
WINDOW_SIZE = (MAZE_WIDTH * CELL_SIZE, MAZE_HEIGHT * CELL_SIZE)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("AI Maze Learning")

def generate_maze():
    # Create a single path from top left to top right
    for x in range(MAZE_WIDTH):
        MAZE[0][x] = 0  # Set the path to white

def draw_maze():
    # Draw the maze
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            if MAZE[y][x] == 0:
                color = (255, 255, 255)  # White for the path
            else:
                color = (0, 0, 0)  # Black for walls
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Main loop
generate_maze()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))  # Fill the screen with white
    draw_maze()

    pygame.display.flip()

pygame.quit()
