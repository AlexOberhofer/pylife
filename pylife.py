import time
import numpy as np
import sys
import ctypes
from sdl2 import *
from copy import deepcopy

PIX_ON = 255
PIX_OFF = 0
pixel_states = [PIX_ON, PIX_OFF]
grid_size = 150
i_update = 60


def randomGrid(N):
    """returns a grid of NxN random values"""
    return np.random.choice(pixel_states, N*N, p=[0.10, 0.90]).reshape(N, N)


def update(grid, N):
    # copy grid since we require 8 neighbors for calculation
    # and we go line by line
    newGrid = deepcopy(grid)
    for i in range(N):
        for j in range(N):
            # compute 8-neghbor sum
            # using toroidal boundary conditions - x and y wrap around
            # so that the simulaton takes place on a toroidal surface.
            total = int((grid[i, (j-1) % N] + grid[i, (j+1) % N] +
                         grid[(i-1) % N, j] + grid[(i+1) % N, j] +
                         grid[(i-1) % N, (j-1) % N] + grid[(i-1) % N, (j+1) % N] +
                         grid[(i+1) % N, (j-1) % N] + grid[(i+1) % N, (j+1) % N])/255)
            # apply Conway's rules
            if grid[i, j] == PIX_ON:
                if (total < 2) or (total > 3):
                    newGrid[i, j] = PIX_OFF
            else:
                if total == 3:
                    newGrid[i, j] = PIX_ON
    # update data
    # img.set_data(newGrid)
    grid[:] = newGrid[:]


def main():
    print("Game of Life by George Conway.")

    SDL_Init(SDL_INIT_VIDEO)

    window = SDL_CreateWindow(b"PyLife",
                              SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
                              grid_size, grid_size, SDL_WINDOW_SHOWN)

    windowsurface = SDL_GetWindowSurface(window)
    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED)
    texture = SDL_CreateTexture(
        renderer, SDL_PIXELFORMAT_ARGB8888, SDL_TEXTUREACCESS_STREAMING, grid_size, grid_size)

    game_board = np.array([])

    game_board = randomGrid(grid_size)
    print("Board Initalized")

    iterations = 0
    while 1:
        update(game_board, grid_size)
        c_array = np.ascontiguousarray(game_board, dtype=int)
        pointer = c_array.ctypes.data_as(ctypes.c_void_p)

        print("Texture converted")
        SDL_UpdateTexture(texture, None, pointer, grid_size)
        print("Texture updated")
        SDL_RenderClear(renderer)
        SDL_RenderCopy(renderer, texture, None, None)
        SDL_RenderPresent(renderer)
        SDL_UpdateWindowSurface(window)
        iterations += 1
        print("Iteration: " + str(iterations))


# call main
if __name__ == '__main__':
    main()
