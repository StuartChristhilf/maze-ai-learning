import pygame
import random
import numpy as np

# Initialize pygame
pygame.init()

# Define the dimensions of the maze
width, height = 600, 400
rows, cols = 30, 20
cell_width, cell_height = width // cols, height // rows

# Set up the display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Random Maze Generator")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Define the Cell class
class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.visited = False
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}

    def draw(self):
        x, y = self.col * cell_width, self.row * cell_height
        # Check if the cell is the starting or ending cell
        if self.row == 0 and self.col == 0:
            # Starting cell, color it green
            pygame.draw.rect(screen, GREEN, (x, y, cell_width, cell_height))
        elif self.row == rows - 1 and self.col == cols - 1:
            # Ending cell, color it red
            pygame.draw.rect(screen, RED, (x, y, cell_width, cell_height))
        elif self.visited:
            pygame.draw.rect(screen, WHITE, (x, y, cell_width, cell_height))
        
        # Draw the walls
        if self.walls['top']:
            pygame.draw.line(screen, BLACK, (x, y), (x + cell_width, y), 2)
        if self.walls['right']:
            pygame.draw.line(screen, BLACK, (x + cell_width, y), (x + cell_width, y + cell_height), 2)
        if self.walls['bottom']:
            pygame.draw.line(screen, BLACK, (x + cell_height, y + cell_height), (x, y + cell_height), 2)
        if self.walls['left']:
            pygame.draw.line(screen, BLACK, (x, y + cell_height), (x, y), 2)


def remove_walls(a, b):
    dx = a.col - b.col
    dy = a.row - b.row
    if dx == 1:
        a.walls['left'] = False
        b.walls['right'] = False
    elif dx == -1:
        a.walls['right'] = False
        b.walls['left'] = False
    if dy == 1:
        a.walls['top'] = False
        b.walls['bottom'] = False
    elif dy == -1:
        a.walls['bottom'] = False
        b.walls['top'] = False

def get_unvisited_neighbors(cell):
    neighbors = []
    row, col = cell.row, cell.col
    if row > 0 and not grid[row - 1][col].visited:
        neighbors.append(grid[row - 1][col])
    if row < rows - 1 and not grid[row + 1][col].visited:
        neighbors.append(grid[row + 1][col])
    if col > 0 and not grid[row][col - 1].visited:
        neighbors.append(grid[row][col - 1])
    if col < cols - 1 and not grid[row][col + 1].visited:
        neighbors.append(grid[row][col + 1])
    return neighbors

# Create the grid
grid = [[Cell(row, col) for col in range(cols)] for row in range(rows)]

# Set up the stack and initial cell
stack = []
current_cell = grid[0][0]
current_cell.visited = True

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    # Draw the grid
    for row in grid:
        for cell in row:
            cell.draw()

    # Step through the maze generation
    neighbors = get_unvisited_neighbors(current_cell)
    if neighbors:
        next_cell = random.choice(neighbors)
        next_cell.visited = True
        stack.append(current_cell)
        remove_walls(current_cell, next_cell)
        current_cell = next_cell
    elif stack:
        current_cell = stack.pop()

    pygame.display.flip()

pygame.quit()
