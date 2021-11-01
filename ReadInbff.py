'''
Initial python file for reading in .bff files for their information.
'''

import numpy as np
import random


def ReadInbff(bfffile):
    '''
    Read in the inputted bff file and return all the necessary
    variables used for LAZOR puzzle solving.

    **Parameters**
        bfffile: *string
            The absolute directory path to the desired bff file.

    **Returns**
        Grid: *list
            Initial Grid
        L: *list
            Lazor position and velocity. First two numbers are where the
            the laser starts, and the last two numbers are the
            x and y velocities.
        A: *int
            Number of Reflect Blocks
        B: *int
            Number of Opaque Blocks
        C: *int
            Number of Refract Blocks
    '''
    P = []
    Grid = []
    L = []
    copy = False
    A = 0
    B = 0
    C = 0
    with open(bfffile, 'r') as f:
        for line in f:
            if '#' in line:
                continue
            elif line.startswith('P'):
                appending = line.partition('P')[2].strip()
                appending = [int(i) for i in appending.split() if i.isdigit()]
                P.append(appending)
            elif line.startswith('A'):
                A = int(line.partition('A')[2].strip())
            elif (line.startswith('B') and
                  line.partition('B')[2].strip().isdigit()):
                B = int(line.partition('B')[2].strip())
            elif line.startswith('C'):
                C = int(line.partition('C')[2].strip())
            elif line.startswith('L'):
                appending = line.partition('L')[2].strip()
                appending = [int(i) for i in appending.split()]
                L.append(appending)
            elif line.startswith('GRID START'):
                copy = True
                continue
            elif line.startswith('GRID STOP'):
                copy = False
                continue
            elif copy:
                Grid.append(line.strip().replace("  ", ""))
    return P, A, B, C, L, Grid

# Make class to define the blocks. Save the properties of each block in
# the block class.


class Block:
    '''
    Here we store all the attributes of each block type and allow
    for the Block class to be called to descrive the attributes
    of each block type.
    '''
    def __init__(self, block_type, lr, va, vb):
        self.block_type = block_type
        self.lr = lr
        self.va = va
        self.vb = vb

    def Reflect(lr, va, vb):
        '''
        Returns the vx and vy after impacting the reflect block. vx and vy
        are dependent on what side of the reflect block is impacted.

        **Parameters**

            lr: *int
                0 if the top or bottom is impacted, 1 if the left or right is
                impacted.
            va: *int
                The x velocity of the laser just before impact.
            vb: *int
                The y velocity of the laser just before impact.

        **Returns**

            vx: *int
                The x velocity of the laser after impact.
            vy: *int
                The y velocity of the laser after impact.
        '''

        if lr == 1:
            vx = -va
            vy = vb
        else:
            vx = va
            vy = -vb
        return vx, vy

    def Opaque(lr, va, vb):
        '''
        Returns the vx and vy after impacting the opaque block. vx and vy
        are both 0 after hitting this block.

        **Parameters**

            lr: *int
                0 if the top or bottom is impacted, 1 if the left or right is
                impacted.
            va: *int
                The x velocity of the laser just before impact.
            vb: *int
                The y velocity of the laser just before impact.

        **Returns**

            vx: *int
                The x velocity of the laser after impact.
            vy: *int
                The y velocity of the laser after impact.
        '''
        vx = 0
        vy = 0
        return vx, vy

    def Refract(lr, va, vb):
        '''
        Returns the vx and vy, and the same va and vb as inputted,
        after impacting the reflect block. vx and vy are
        dependent on what side of the reflect block is impacted.

        **Parameters**

            lr: *int
                0 if the top or bottom is impacted, 1 if the left or right is
                impacted.
            va: *int
                The x velocity of the laser just before impact.
            vb: *int
                The y velocity of the laser just before impact.

        **Returns**

            vx: *int
                The x velocity of the laser after impact.
            vy: *int
                The y velocity of the laser after impact.
            va: *int
                The x velocity of the second laser after impact.
            vb: *int
                The y velocity of the second laser after impact.
        '''
        if lr == 1:
            vx = -va
            vy = vb
        else:
            vx = va
            vy = -vb
        return vx, vy, va, vb

    def __call__(self, block_type, lr, va, vb):

        if block_type == 'A':
            return Block.Reflect(lr, va, vb)
        elif block_type == 'B' or block_type == 'Bo':
            return Block.Opaque(lr, va, vb)
        elif block_type == 'C':
            return Block.Refract(lr, va, vb)
        elif block_type == 'o' or block_type == 'oo' or block_type == 'x':
            return va, vb


def pos_chk(x, y, width, height):
    '''
    Validate if the coordinates specified (x and y) are within the maze.

    **Parameters**

        x: *int*
            An x coordinate to check if it resides within the maze.
        y: *int*
            A y coordinate to check if it resides within the maze.
        nBlocks: *int*
            How many blocks wide the maze is.  Should be equivalent to
            the length of the maze (ie. len(maze)).

    **Returns**

        valid: *bool*
            Whether the coordiantes are valid (True) or not (False).
    '''
    return x >= 0 and x <= width and y >= 0 and y <= height


def define_grid(Grid):
    y_values = len(Grid)*2
    x_values = []
    for i in Grid:
        x_values.append(i.split(' ')[0])
    x_values = len(x_values)*2
    grid_list = []
    for i in Grid:
        for j in range(int((y_values / 2))):
            grid_list.append(i.split(' ')[j])
    x_vals = int(x_values/2)
    y_vals = int(y_values/2)
    grid_expanded = []
    for i in range(len(grid_list)):
        grid_expanded.append(grid_list[i] * 9)
    grid_separated = []
    for i in range(x_vals):
        for j in range(y_vals):
            grid_grouped_list = [grid_expanded[n:n+x_vals] for n in
                                 range(0, len(grid_expanded), x_vals)]
            grid_grouped = grid_grouped_list[i][j]
            grid_separated = grid_separated + list(grid_grouped[:9])
    # for i in range(x_vals):
    #     for j in range(y_vals):
    #         grid_elements = [grid_separated[n:n+x_vals] for n in
    #         range(0, len(grid_separated),x_vals)]
    x_count = 2
    y_count = x_values + 3
    while x_count < x_values*9:
        grid_separated[x_count] =\
            grid_separated[x_count] + grid_separated[x_count + 9]
        x_count = x_count + 3
    # while y_count < x_values + y_values:
    #     grid_separated[y_count] =\
    #        grid_separated[y_count] + grid_separated[y_count + 1]
    #     y_count = y_count + 2
    for i in range(1, x_values+2):
        grid_grouped_list = [grid_separated[n:n+i] for n in
                             range(0, len(grid_separated), i)]
    print(grid_grouped_list)
    print(grid_grouped_list[0][6])
    return grid_grouped_list


def as_string(seq_of_rows):
    '''
    Function for visualizing the new_grid more easily.

    **Parameters**
        seq_of_rows: *list
            A list of lists that has the elements of the new coordinate system.

    **Returns**
        Visual: *string
            A string that has all the elements in a more visually
            understandable format.
    '''
    return '\n'.join(''.join(str(i).center(5) for i in row)
                     for row in seq_of_rows)

 def laser_path(start):
    laser_pos = [start] # list of all the positions the laser passed
    vx = 1
    vy = 1
    grid_h = len(new_grid)
    grid_w = len(new_grid[0])
    laser_dir = [
        (1, 1),
        (-1, -1),
        (1, -1),
        (-1, 1)
    ]

    change = Block('A',1,1,1) # location, velocity x, y
    # the velocity wouldn't be any different though? always (1,1)?


    while pos_chk(laser_pos[-1][0], laser_pos[-1][1], grid_w - 1, grid_h - 1):  # if position within block
        # get current laser position
        lz_cur = laser_pos[-1] 
        old_x = lz_cur[0]
        old_y = lz_cur[1]

        # check hit top/bottom (0) or left/right (1) - how
        hit = 1

        # get the change and update new position
        ch = change(new_grid[old_y][old_x], hit, vx, vy)
        print('type:', new_grid[old_y][old_x])
        print("ch:", ch)
        new_x = old_x + laser_dir[2][0]*ch[0] + 1  # the new x position after stepping
        new_y = old_y + laser_dir[2][0]*ch[1] + 1
        print('new x:',new_x,'new y:',new_y)
        
        # append into the position list for laser
        laser_pos.append((new_x, new_y))
    return laser_pos

def output_random_grid(Grid, A, B, C, Repeat_Grid):
    '''
    Function for adding all possible block elements to a random grid.

    **Parameters**
        Grid: *list
            The grid read in from the .bff file.
        A: *int
            The number of A blocks to be added.
        B: *int
            The number of B blocks to be added.
        C: *int
            The number of C blocks to be added.
        Repeat_Grid: *list
            The grids that have already been tried
            are saved here in a list.

    **Returns**
        Output_Grid: *list
            The randomized grid with A, B, and C placed at random positions
            where o used to be.
        Repeat_Grid: *list
            The grids that have already been tried
            are saved here in a list.
    '''

    Random_Grid = []
    Output_Grid = []
    for i in Grid:
        Random_Grid.append(i.split(" "))
    print(Random_Grid)
    while A > 0 or B > 0 or C > 0:
        list1 = random.randrange(len(Random_Grid))
        list2 = random.randrange(len(Random_Grid[0]))
        if Random_Grid[list1][list2] == 'o':
            if A > 0:
                Random_Grid[list1][list2] = 'A'
                A -= 1
            elif B > 0:
                Random_Grid[list1][list2] = 'B'
                B -= 1
            elif C > 0:
                Random_Grid[list1][list2] = 'C'
                C -= 1
    for i in Random_Grid:
        Output_Grid.append(" ".join(i))
    Repeat_Grid.append(Output_Grid)
    return Output_Grid, Repeat_Grid

def solve_lazor(P, A, B, C, L, Grid):
    '''
     **Parameters**

    Grid: *list
      Initial grid read from the inputted .bff file.
    L: *list
      Lazor position and velocity. First two numbers are where the the laser
      starts, and the last two numbers are the x and y velocities.
    A: *int
      Number of Reflect Blocks
    B: *int
      Number of Opaque Blocks
    C: *int
      Number of Refract Blocks

    **Returns**
        Solved_Grid: *list

    '''
    Solution_Flag = 0
    Repeat_Grid = []
    while Solution_Flag == 0:
        Output_Grid, Repeat_Grid = output_random_grid(Grid, A, B, C,
                                                      Repeat_Grid)
        for i in Repeat_Grid:
            if Output_Grid in i:
                continue
        Solution_Flag = 1

    Solved_Grid = Output_Grid

    return Solved_Grid


if __name__ == '__main__':

    bfffile = 'bff_files\\yarn_5.bff'
    # bfffile=input('Please Enter the name of the .bff file to be solved: ')
    # bfffile='bff_files/' + bfffile
    P, A, B, C, L, Grid = ReadInbff(bfffile)
    print(A, B, C, Grid)
    ans = Block('o', 1, 1, 1)
    a = ans('o', 1, 0, 1)
    print(a)
    print('')
    print('Initial Grid:')
    print('')
    print("\n".join(map(" ".join, Grid)))
    solved = solve_lazor(P, A, B, C, L, Grid)
    # new_grid = define_grid(Grid)
    # print(as_string(new_grid))
    print('')
    print('Solution:')
    print('')
    print("\n".join(map(" ".join, solved)))
    # Number of laser grid points is 2N*2N
