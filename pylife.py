import numpy as np
import sys
import ctypes
import sdl2.ext
import time
from ctypes import *
from sdl2 import *
from copy import deepcopy

PIX_ON = 0xFFFFFF
PIX_OFF = 0x000000
pixel_states = [PIX_ON, PIX_OFF]
grid_size = 200


def seed(size):
    return np.random.choice(pixel_states, size*size, p=[0.15, 0.85]).reshape(size, size)


def conway_update(board, size):

    #create a copy of the game board
    newBoard = deepcopy(board)

    #iterate through each row + col
    for i in range(size):
        for j in range(size):

            #computer number of neighbors with wrapping
            total = int((board[i, (j-1) % size] + 
                         board[i, (j+1) % size] +
                         board[(i-1) % size, j] + 
                         board[(i+1) % size, j] +
                         board[(i-1) % size, (j-1) % size] + 
                         board[(i-1) % size, (j+1) % size] +
                         board[(i+1) % size, (j-1) % size] + 
                         board[(i+1) % size, (j+1) % size])/PIX_ON)

            #default rules
            if board[i, j] == PIX_ON:
                if (total < 2) or (total > 3):
                    newBoard[i, j] = PIX_OFF
            else:
                if total == 3:
                    newBoard[i, j] = PIX_ON

    #set board to new updated state
    board[:] = newBoard[:]


def main():
    print("Game of Life by George Conway.")
    print("(C) 2020 Alex Oberhofer")
    
    #init 
    iterations = 0
    running = True
    scale = 2

    #Setup SDL
    SDL_Init(SDL_INIT_VIDEO)

    #Create Window
    window = SDL_CreateWindow(b"PyLife", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
                              grid_size * scale, grid_size * scale, SDL_WINDOW_SHOWN)

    #create renderer                          
    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED)

    #create our texture
    texture = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_ARGB8888, SDL_TEXTUREACCESS_STREAMING, grid_size, grid_size)

    print("Display Initialized...")
    game_board = np.array([])

    game_board = seed(grid_size)
    print("Board Initalized...")


    while running:

        #event polling
        events = sdl2.ext.get_events()

        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
        
        #iterate board state
        conway_update(game_board, grid_size)
        iterations += 1

        #update title with iterations
        new_title = b"||    PyLife: Conway      ||  Iteration - " + str(iterations).encode('utf-8') + b"    ||"
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
        time.sleep(1/5000)


# call main
if __name__ == '__main__':
    main()
