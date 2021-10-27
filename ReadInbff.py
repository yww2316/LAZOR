'''
Initial python file for reading in .bff files for their information.
'''

import numpy as np
import re

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
            Lazor position and velocity. First two numbers are where the the laser
            starts, and the last two numbers are the x and y velocities.
        A: *int
            Number of Reflect Blocks
        B: *int 
            Number of Opaque Blocks
        C: *int
            Number of Refract Blocks
    '''
    P=[]
    Grid=[]
    L=[]
    copy=False
    A = 0
    B = 0
    C = 0
    with open(bfffile, 'r') as f:
        for line in f:
            if '#' in line:
                continue
            elif line.startswith('P'):
                appending=line.partition('P')[2].strip()
                appending=[int(i) for i in appending.split() if i.isdigit()]
                P.append(appending)
            elif line.startswith('A'):
                A=int(line.partition('A')[2].strip())
            elif line.startswith('B') and line.partition('B')[2].strip().isdigit():
                B=int(line.partition('B')[2].strip())
            elif line.startswith('C'):
                C=int(line.partition('C')[2].strip())
            elif line.startswith('L'):
                appending=line.partition('L')[2].strip()
                appending=[int(i) for i in appending.split()]
                L.append(appending)
            elif line.startswith('GRID START'):
                copy=True
                continue
            elif line.startswith('GRID STOP'):
                copy=False
                continue
            elif copy:
                Grid.append(line.strip())
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

            if lr==1:
                vx=-va
                vy=vb
            else:
                vx=va
                vy=-vb
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
        vx=0
        vy=0
        return vx, vy

        
    def Refract(lr, va, vb):
        '''
        Returns the vx and vy, and the same va and vb as inputted, after impacting the reflect block. 
        vx and vy are dependent on what side of the reflect block is impacted.

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
        if lr==1:
            vx=-va
            vy=vb
        else:
            vx=va
            vy=-vb
        return vx, vy, va, vb

    def __call__(self, block_type, lr, va, vb):

        if block_type == 'A':
            return Block.Reflect(lr, va, vb)
        elif block_type == 'B':
            return Block.Opaque(lr, va, vb)
        elif block_type == 'C':
            return Block.Refract(lr, va, vb)
        elif block_type == 'o':
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
    Solved_Grid = Grid

    return Solved_Grid
if __name__=='__main__':

    bfffile='bff_files\showstopper_4.bff'
    # bfffile=input('Please Enter the name of the .bff file to be solved: ')
    # bfffile='bff_files/' + bfffile
    P, A, B, C, L, Grid = ReadInbff(bfffile)
    #print(P, A, B, C, L, Grid)
    print('')
    print('Initial Grid:')
    print('')
    print("\n".join(map(" ".join, Grid)))
    #bah = Block('B', 1, 1, 1)
    #print(bah('A', 1, 2, 1))
    solved=solve_lazor(P, A, B, C, L, Grid)
    print('')
    print('Solution:')
    print('')
    print("\n".join(map(" ".join, solved)))
    #Number of laser grid points is 2N*2N