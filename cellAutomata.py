# by jvpcms
# setup cells then run simulation by closing window

from time import sleep
import pygame
from numpy import zeros

grid_size, cell_size, border_px = 150, 5, 1
dt = 0.1
running = True
clicked = False

resolution = (grid_size*cell_size, grid_size*cell_size)
black, white = (20, 20, 20), (200, 200, 200)

grid = zeros((grid_size, grid_size))
aux_grid = zeros((grid_size, grid_size))

# init screen
pygame.display.init()
screen = pygame.display.set_mode(resolution)

# setup cells
while running:

    # print board
    for i in range(grid_size):
        for j in range(grid_size):
            cell_position = (i*cell_size, j*cell_size, cell_size, cell_size)
            if grid[i][j]:
                pygame.draw.rect(screen, white, cell_position)
            else:
                pygame.draw.rect(screen, black, cell_position)

    # invert cell when clicked
    if pygame.mouse.get_pressed()[0]:
        if not clicked:
            x, y = pygame.mouse.get_pos()
            x = x // cell_size
            y = y // cell_size
            grid[x][y] = not grid[x][y]
            clicked = True
    else:
        clicked = False

    # update screen
    pygame.display.flip()

    # detect quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

running = True

# run cell automata
while running:
    # clear
    pygame.draw.rect(screen, black, (0, 0, grid_size*cell_size, grid_size*cell_size))

    # print board
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j]:
                cell_position = (i*cell_size, j*cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, white, cell_position)

    # generate new aux board
    for i in range(grid_size):
        for j in range(grid_size):
            neighbors = 0

            for col in range(i - 1, i + 2):
                for lin in range(j - 1, j + 2):
                    if 0 <= col < grid_size and 0 <= lin < grid_size and (col != i or lin != j):
                        neighbors += grid[col][lin]

            if grid[i][j] == 1 and (neighbors == 2 or neighbors == 3):
                aux_grid[i][j] = 1
            elif grid[i][j] == 0 and neighbors == 3:
                aux_grid[i][j] = 1
            else:
                aux_grid[i][j] = 0

    # board <- aux board
    grid = list(map(list, aux_grid))

    # update screen
    pygame.display.flip()

    # wait
    sleep(dt)

    # detect quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
