import pygame
import random
import time

# Define maze parameters
MAZE_WIDTH = 20
MAZE_HEIGHT = 20
CELL_SIZE = 30
MAZE = [[0] * MAZE_WIDTH for _ in range(MAZE_HEIGHT)]

# Pygame setup
pygame.init()
WINDOW_SIZE = (MAZE_WIDTH * CELL_SIZE, MAZE_HEIGHT * CELL_SIZE)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("AI Maze Learning")

# Define AI parameters
POPULATION_SIZE = 5
MUTATION_RATE = 0.1
GENERATIONS = 100

# Initialize population
population = [{'x': 0, 'y': 0, 'fitness': 0} for _ in range(POPULATION_SIZE)]


def generate_maze():
    # Create a random path from start to finish
    for x in range(MAZE_WIDTH):
        MAZE[0][x] = 0  # Start
        MAZE[MAZE_HEIGHT - 1][x] = 0  # Finish

    current_y = 0
    while current_y < MAZE_HEIGHT - 1:
        move_direction = random.choice([-1, 1])  # Move either left or right
        current_y += 1
        MAZE[current_y][max(0, min(MAZE_WIDTH - 1, current_y + move_direction))] = 0

    # Randomize the rest of the maze
    for y in range(1, MAZE_HEIGHT - 1):
        for x in range(MAZE_WIDTH):
            if MAZE[y][x] != 0:
                MAZE[y][x] = random.choice([0, 1])

def draw_maze():
    # Draw the maze
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            color = (0, 0, 0) if MAZE[y][x] == 1 else (255, 255, 255)
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def draw_population():
    # Draw the population
    for individual in population:
        pygame.draw.circle(screen, (255, 0, 0), (individual['x'] * CELL_SIZE + CELL_SIZE // 2,
                                                individual['y'] * CELL_SIZE + CELL_SIZE // 2), 10)


def move_individual(individual, action):
    # Move individual based on action (0: up, 1: down, 2: left, 3: right)
    if action == 0 and individual['y'] > 0 and MAZE[individual['y'] - 1][individual['x']] == 0:
        individual['y'] -= 1
    elif action == 1 and individual['y'] < MAZE_HEIGHT - 1 and MAZE[individual['y'] + 1][individual['x']] == 0:
        individual['y'] += 1
    elif action == 2 and individual['x'] > 0 and MAZE[individual['y']][individual['x'] - 1] == 0:
        individual['x'] -= 1
    elif action == 3 and individual['x'] < MAZE_WIDTH - 1 and MAZE[individual['y']][individual['x'] + 1] == 0:
        individual['x'] += 1


def evaluate_fitness(individual):
    # Evaluate fitness based on positive and negative rewards
    end_time = 60  # 1 minute
    elapsed_time = time.time() - start_time
    max_fitness = MAZE_WIDTH * MAZE_HEIGHT

    if individual['x'] == MAZE_WIDTH - 1 and individual['y'] == MAZE_HEIGHT - 1:
        # Reached the end
        individual['fitness'] = max_fitness + (end_time - elapsed_time) * 10
    else:
        # Negative rewards
        individual['fitness'] = -10  # Base negative reward

        if MAZE[individual['y']][individual['x']] == 1:
            individual['fitness'] -= 5  # Touching walls

        if individual['x'] == 0 or individual['y'] == 0 or individual['x'] == MAZE_WIDTH - 1 or individual[
            'y'] == MAZE_HEIGHT - 1:
            individual['fitness'] -= 3  # Hitting maze boundaries

    return individual['fitness']


def crossover(parent1, parent2):
    # Crossover two individuals to create a new one
    crossover_point = random.randint(0, len(parent1) - 1)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child


def mutate(child):
    # Mutate an individual
    for i in range(len(child)):
        if random.random() < MUTATION_RATE:
            child[i] = random.randint(0, 3)  # Randomly change action
    return child


# Main loop
generate_maze()
start_time = time.time()

for generation in range(GENERATIONS):
    max_fitness = float('-inf')
    for individual in population:
        # Reset individual's position
        individual['x'] = 0
        individual['y'] = 0

        for _ in range(MAZE_WIDTH * MAZE_HEIGHT):
            # Simulate individual's moves
            action = random.randint(0, 3)
            move_individual(individual, action)

            # Evaluate fitness
            fitness = evaluate_fitness(individual)

            if fitness > max_fitness:
                max_fitness = fitness

            # Draw the maze and population
            screen.fill((255, 255, 255))
            draw_maze()
            draw_population()
            pygame.display.flip()

            # Pause for a short time to visualize the simulation
            pygame.time.wait(50)

    # Select the top-performing individuals
    population.sort(key=lambda x: x['fitness'], reverse=True)
    selected_parents = population[:int(POPULATION_SIZE * 0.2)]

    # Crossover and mutate to create a new generation
    new_population = selected_parents.copy()
    while len(new_population) < POPULATION_SIZE:
        parent1 = random.choice(selected_parents)
        parent2 = random.choice(selected_parents)
        child = mutate(crossover(parent1, parent2))
        new_population.append({'x': 0, 'y': 0, 'fitness': 0, 'actions': child})

    population = new_population

pygame.quit()
