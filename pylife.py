import time
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

PIX_ON = 255
PIX_OFF = 0
pixel_states = [PIX_ON, PIX_OFF]
grid_size = 150
i_update = 60

def randomGrid(N):
    """returns a grid of NxN random values"""
    return np.random.choice(pixel_states, N*N, p=[0.10, 0.90]).reshape(N, N)

def update(frameNum, img, grid, N):
    # copy grid since we require 8 neighbors for calculation
    # and we go line by line 
    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):
            # compute 8-neghbor sum
            # using toroidal boundary conditions - x and y wrap around 
            # so that the simulaton takes place on a toroidal surface.
            total = int((grid[i, (j-1)%N] + grid[i, (j+1)%N] + 
                         grid[(i-1)%N, j] + grid[(i+1)%N, j] + 
                         grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] + 
                         grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])/255)
            # apply Conway's rules
            if grid[i, j]  == PIX_ON:
                if (total < 2) or (total > 3):
                    newGrid[i, j] = PIX_OFF
            else:
                if total == 3:
                    newGrid[i, j] = PIX_ON
    # update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

  

def main():
    print("Game of Life by George Conway.")

    game_board = np.array([])

    game_board = randomGrid(grid_size)
    print("Board Initalized")

    plt.rcParams['toolbar'] = 'None'

    fig, ax = plt.subplots() 
    ax.set_axis_off()
            
    ax.spines['left'].set_position(('outward', 0))
    ax.spines['bottom'].set_position(('outward', 0))
       
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
      
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

    fig.subplots_adjust(0,0,1,1)

    img = ax.imshow(game_board, cmap=plt.cm.gray, interpolation='nearest') 

    ani = animation.FuncAnimation(fig, update, fargs=(img, game_board, grid_size, ),
                                frames = 60,
                                interval=i_update,
                                save_count=100)

    plt.show()

    
    
# call main
if __name__ == '__main__':
    main()
