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
    # We will use P, A, B, C, L, Grid
    # Grid: *list
    #   Initial Grid
    # L: *list
    #   Lazor position and velocity. First two numbers are where the the laser
    #   starts, and the last two numbers are the x and y velocities.
    # A: *int
    #   Number of Reflect Blocks
    # B: *int 
    #   Number of Opaque Blocks
    # C: *int
    #   Number of Refract Blocks
    # First step is to read in the information from the .bff file.
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
class Block(object):
    '''
    Here we store all the attributes 
    '''
    def Reflect(self, lr, va, vb):
        if lr==1:
            vx=-va
            vy=vb
        else:
            vx=va
            vy=-vb
        return vx, vy
    
    def Opaque(self, va, vb):
        vx=0
        vy=0
        return vx, vy
    
    def Refract(self, lr, va, vb):
        if lr==1:
            vx=-va
            vy=vb
        else:
            vx=va
            vy=-vb
        return va, vb, vx, vy


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

if __name__=='__main__':
    bfffile='bff_files\showstopper_4.bff'
    P, A, B, C, L, Grid = ReadInbff(bfffile)
    print("\n".join(map(" ".join, Grid)))