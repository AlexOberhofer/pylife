import time
import numpy as np
import sys
import ctypes
import sdl2.ext
from ctypes import *
from sdl2 import *
from copy import deepcopy

PIX_ON = 0xFFFFFF
PIX_OFF = 0x000000
pixel_states = [PIX_ON, PIX_OFF]
grid_size = 200


def randomGrid(N):
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
                         grid[(i+1) % N, (j-1) % N] + grid[(i+1) % N, (j+1) % N])/PIX_ON)
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

    scale = 2

    window = SDL_CreateWindow(b"PyLife",
                              SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
                              grid_size * scale, grid_size * scale, SDL_WINDOW_SHOWN)

    windowsurface = SDL_GetWindowSurface(window)
    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED)
    texture = SDL_CreateTexture(
        renderer, SDL_PIXELFORMAT_ARGB8888, SDL_TEXTUREACCESS_STREAMING, grid_size, grid_size)

    game_board = np.array([])

    game_board = randomGrid(grid_size)
    print("Board Initalized")

    iterations = 0
    running = True
    while running:
        events = sdl2.ext.get_events()

        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
        
        #iterate board state
        update(game_board, grid_size)
        iterations += 1

        new_title = b"PyLife                      Iteration - " + str(iterations).encode('utf-8')
        SDL_SetWindowTitle(window, new_title)

        #convert to 2d to contiguous array
        c_array = np.ascontiguousarray(game_board, dtype=int)

        #change to c type sdl expects
        pointer = c_array.ctypes.data_as(ctypes.c_void_p)

        #update our texture
        SDL_UpdateTexture(texture, None, pointer, grid_size * 4)
        SDL_RenderClear(renderer)
        SDL_RenderCopy(renderer, texture, None, None)
        SDL_RenderPresent(renderer)
        SDL_UpdateWindowSurface(window)
        
        print("Iteration: " + str(iterations))


# call main
if __name__ == '__main__':
    main()
