'''
Initial python file for reading in .bff files for their information.
'''

import random
import time
import collections


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
        P: *list
            Points for laser to intersect
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

        if 'B' in block_type:
            return Block.Opaque(lr, va, vb)
        elif 'A' in block_type:
            return Block.Reflect(lr, va, vb)
        elif 'C' in block_type:
            return Block.Refract(lr, va, vb)
        else:
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
    '''
    Generate list that has correct coordinate values
    for each element (A, B, C, o, x).
    **Parameters**
        Grid: *list
                Initial grid.

    **Returns**
        grid_coords: *list
                Expanded grid that contains the correct
                coordinates x, y for solving maze.
    '''
    y_values = len(Grid) * 2
    grid_elements = []
    # First, we have to split the row strings and instead make them into
    # nested lists. Save into grid_elements.
    for i in Grid:
        grid_elements.append(i.split(' '))
    count = 0
    grid_expanded_y = []
    counter = 0

    # Next, we want to repeat each row to put into coordinates.
    # For example, a row of 'o', 'o', 'o'  will need to be multiplied by three
    # become 'o', 'o', 'o','o', 'o', 'o','o', 'o', 'o' if it is the first row.
    # However, if it is not in the first row,
    # then we will need to multiply by two.
    # It will instead become 'o', 'o', 'o', 'o', 'o', 'o'.
    # This is because there are three rows between y = 0 to y = 2
    # but once y = 2 has been reached, each new block is only another 2 rows,
    # such that y = 3 and y = 4 is the second row,
    # and y = 5 and y = 6 is the third row and so on.
    # This will be saved as grid_expanded_y.
    for element in grid_elements:
        if element == grid_elements[0] and counter == 0:
            # This loop tests whether the element we are at is = to first row.
            # The purpose of the counter is so that if there is another row
            # that is identical to the first row,
            # we don't multiple that one by three as well.
            grid_expanded_y.append(element * 3)
            counter = 1
        else:
            # If we have already done the first row,
            # then we go into this loop & start multiplying by 2 instead of 3.
            grid_expanded_y.append(element * 2)

    # Now that we have completed the row expansion,
    # we need to do the column expansion.
    # We will multiply each element within nested lists by three.
    # We will do times three for all of them because we will
    # eventually need to combine the strings horizontally.
    # This will be saved as grid_expanded, which is a single list.
    grid_expanded = []
    for element in grid_elements:
        count += len(element)
    for element in grid_expanded_y:
        for i in range(len(element)):
            grid_expanded.append(element[i] * 3)

    x_values = int((count / (y_values / 2)) * 2)
    # x_values is the maximum value for the coordinate system that we use,
    # in which each block takes up 3 values in x.
    # For example, the top left block is from x = 0 to x = 2,
    # and the one next to it takes up x = 2 to x = 4.
    x_vals = int(x_values / 2)
    # x_vals is the true number of blocks in each row in initial grid.

    # Now that we have the list, we need to group it again
    # such that it contains nested lists representing each row.
    # This will be saved as grid_grouped_list.
    # Note that we still have multiples within each element in nested lists.
    # Instead of 'o' being an element, it's 'ooo', for example.
    grid_grouped_list = [grid_expanded[n:n + x_vals] for n in
                         range(0, len(grid_expanded), x_vals)]

    # Next, we will need to separate out the multiples
    # into their own elements and put them each as nested lists.
    # For example, 'ooo' will become ['o', 'o', 'o'].
    # This will be save into grid_grouped.
    grid_grouped = []
    for element in grid_grouped_list:
        for i in range(len(element)):
            grid_grouped.append(list(element[i]))
    count = 0

    # Next, we want to get rid of all the nested lists
    # and instead make one long list.
    # This will be saved as grid_grouped_single_list.
    grid_grouped_single_list = []
    for i in range(len(grid_grouped)):
        for j in range(3):
            grid_grouped_single_list.append(grid_grouped[i][j])

    # Next, we want to combine the elements horizontally
    # such that at x = 2, a 'o' block neighboring an 'o' block will be 'oo'.
    # And a 'B' block neighboring a 'o' block will be 'Bo'.
    # We will save these as nested lists, where each list represents a row (x)
    # and the number of the element in each list represents the column (y).
    max_rows = x_vals * 3
    grid_coords = []
    row_cnt = 0
    row = []
    for i, letter in enumerate(grid_grouped_single_list):
        if i > (row_cnt + 1) * max_rows - 1:
            if row != []:
                # Once row is complete, we append entire row to grid_coords.
                grid_coords.append(row)
                row = []
                # We blank the row again to start working on the next row,
                # and we increase row count by 1.
                row_cnt += 1
        if i != (row_cnt * max_rows) and i % 3 == 0:
            # Through trial and error, we see that we need this loop.
            # This loop is crucial because it makes the appending skip over
            # the string that we have already combined.
            # For example, 'o', 'o', 'o', 'B', 'B', 'B', 'x', 'x', 'x'
            # ends up being 'o', 'o', 'oB', 'B', 'B', 'Bx', 'x', 'x'.
            # This is incorrect because it has two B's where
            # it should only have 1 B to represent the middle of the block.
            pass
        elif i in list(range(row_cnt * max_rows + 2,
                             (row_cnt + 1) * max_rows - 1, 3)):
            # If we are at the side of the block,
            # we want to add strings together.
            # For example, we have 'o', 'o', 'o', 'B', 'B', 'B' as first row,
            # representing an 'o' block next to a 'B' block.
            # We want to combine the 2nd element(starting count at 0)
            # with the 3rd element. This results in 'o', 'o', 'oB', 'B', 'B'.
            # We repeat this in increments of 3 until we are 2 counts
            # away from the rightmost edge of the grid.
            # We save the strings to temp and then append temp to the row.
            temp = grid_grouped_single_list[i] \
                + grid_grouped_single_list[i + 1]
            row.append(temp)
        else:
            # If we are not at the sides of the block,
            # then we are in the middle.
            # In this case, we just append the original element
            # because we are not touching another block.
            temp = grid_grouped_single_list[i]
            row.append(temp)
    grid_coords.append(row)

    # Lastly, we want to consider when the blocks are touching
    # ie. (share a side) in the y direction,
    # meaning that one is above the other and they share that y coordinate.
    # We incorporate this into grid_coords, which is our final output.
    try:
        for i in range(len(grid_coords)):
            if i % 2 == 0 and i != 0:
                # If the y value is even and we are not at 0
                # (since Python registers 0 to be even),
                # then we want to add the string in the row above
                # (but at same y value)
                # to the string in the row below.
                for j in range(1, x_values):
                    grid_coords[i][j] = grid_coords[i - 1][j] + \
                        grid_coords[i + 1][j]
    except IndexError:
        # This loop results in an error,
        # but it does not prevent the code from getting the correct answer.
        # print('Grid completed!')
        pass
    # print(grid_coords)
    # Note: the corners, where there are 4 blocks touching,
    # are incorrectly generated by this code.
    # However, the laser will never pass through the corners,
    # so this is not an issue for solving the grid.
    return grid_coords


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


def path_loop(L, new_grid):

    '''
    Returns a list of one path taken by the laser. Goes hand-in-hand with
    the function get_all_paths_taken as this function
    does not contain the additional paths taken from a C block split.

    **Parameters**
        L: *list
            Lazor position and velocity. First two numbers are where the
            the laser starts, and the last two numbers are the
            x and y velocities.

        new_grid: *list
            modified intital grid

    **Returns**
        laser_pos: *list
            A list of all the positions taken
        refract_list: *list
            A list of the laser position and velocity after hitting the C block
    '''

    # starting position (user input)
    position = tuple(L[0][:2])
    # starting velocity (user input)
    vx = L[0][2]
    vy = L[0][3]

    # list of all the positions the laser passed
    laser_pos = [position]
    # list of the block types the laser passed
    blk_type = ['o', 'o', 'o']

    grid_h = len(new_grid)
    grid_w = len(new_grid[0])

    # additional list for refract block
    refract_list = []

    change = Block('A', 1, 1, 1)  # block type, hit, vx, vy

    # if position within block
    in_grid = True

    # velocity positive?
    vel_chk = True

    # get current laser position
    lz_cur = laser_pos[-1]
    old_x = lz_cur[0]
    old_y = lz_cur[1]

    # check ahead for first step
    # because laser reflects if its on an A block at the beginning
    # (we don't want that)
    in_grid = pos_chk(old_x + vx, old_y + vy, grid_w - 2, grid_h - 2)

    vx1 = old_x + vx
    vy1 = old_y + vy

    if in_grid:
        if new_grid[vy1][vx1] == 'oo' or new_grid[vy1][vx1] == 'o' or\
             new_grid[vy1][vx1] == 'xo' or new_grid[vy1][vx1] == 'ox':
            new_x = vx1
            new_y = vy1
            laser_pos.append((new_x, new_y))
            blk_type.append(new_grid[new_y][new_x])
    check_start = time.time()
    while in_grid and vel_chk:
        check_end = time.time()
        if check_end-check_start > .003:
            break
        # get current laser position
        lz_cur = laser_pos[-1]
        old_x = lz_cur[0]
        old_y = lz_cur[1]
        blk_type.append(new_grid[old_y][old_x])

        # check hit top/bottom (0) or left/right (1) - x odd or even
        if old_x % 2 == 0:   # if even, left/right
            hit = 1
        else:
            hit = 0

        # if laser is stuck between 2 A blocks
        # if hit == 1:
        #     if new_grid[old_y][old_x-1] == 'A'\
        #          and new_grid[old_y][old_x] == 'A':
        #         break
        # if hit == 0:
        #     if new_grid[old_y-1][old_x] == 'A'\
        #          and new_grid[old_y][old_x] == 'A':
        #         break

        # get the change and update new position
        ch = change(new_grid[old_y][old_x], hit, vx, vy)
        blk_type.append(new_grid[old_y][old_x])

        if len(ch) == 2:  # A or B block
            # update velocity
            vx = ch[0]
            vy = ch[1]
            new_x = old_x + vx
            new_y = old_y + vy

            # need to check this with B block
            if vx == 0 and vy == 0:
                vel_chk = False

        # will have two velocity pairs for C
        # doesn't perform the refract action if prev. was also a C
        elif len(ch) == 4 and 'C' not in blk_type[-3]:
            vx = ch[0]
            vy = ch[1]
            extra_vx = ch[2]
            extra_vy = ch[3]

            new_x = old_x + vx
            new_y = old_y + vy
            extra_x = old_x + extra_vx
            extra_y = old_y + extra_vy
            # append into the extra refract list
            refract_list.append([extra_x, extra_y, extra_vx, extra_vy])

        else:  # perform the len(ch) == 2 code
            vx = ch[2]  # this is the extra vx value
            vy = ch[3]
            new_x = old_x + vx
            new_y = old_y + vy

            # need to check this with B block
            if vx == 0 and vy == 0:
                vel_chk = False

        # append into the position list for laser
        laser_pos.append((new_x, new_y))
        in_grid = pos_chk(
            laser_pos[-1][0], laser_pos[-1][1], grid_w - 2, grid_h - 2)

    return laser_pos, refract_list


def get_all_paths_taken(L, new_grid):

    '''
    contain the additional path from a C block split.
    **Parameters**
        L: *list
            Lazor position and velocity. First two numbers are where the
            the laser starts, and the last two numbers are the
            x and y velocities.

        new_grid: *list
            modified intital grid

    **Returns**
        result: *list
            A list of all the positions taken
    '''

    total_pos = []
    a, b = path_loop(L, new_grid)
    old_a = a
    old_b = b
    total_pos.append(old_a)

    # while there are new paths from refract (C) blocks
    while len(old_b) != 0:
        new_a, new_b = path_loop(old_b, new_grid)
        total_pos.append(new_a)
        old_b = new_b

    # join the refract nested list
    joined_final = [j for i in total_pos for j in i]
    # take out the negatives
    result = [i for i in joined_final if i[0] >= 0 and i[1] >= 0]

    return result


def grid_outcome(P, L, new_grid):

    '''
    Returns whether all the points have been hit by the laser
    **Parameters**
        P: *list
            Points for laser to intersect

        L: *list
            Lazor position and velocity. First two numbers are where the
            the laser starts, and the last two numbers are the
            x and y velocities.

        new_grid: *list
            modified intital grid

    **Returns**
        all_touched: *bool
            whether all points were touched
    '''
    # include all lasers (some files have multiple starting lasers)
    joined_all = []
    for i in L:
        join = get_all_paths_taken([i], new_grid)
        joined_all.append(join)

    # make the intersection points into a list of tuples
    intersect_pts = []
    for pt in P:
        intersect_pts.append(tuple(pt))

    # flatten lists
    joined_final = [j for i in joined_all for j in i]
    # delete duplicates
    no_repeat = list(set([x for x in joined_final]))
    # laser touched all intersect pts
    all_touched = all(elem in no_repeat for elem in intersect_pts)
    return all_touched


def output_random_grid(Grid, A, B, C):
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
    '''
    Random_Grid = []
    Output_Grid = []
    for i in Grid:
        Random_Grid.append(i.split(" "))
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
    return Output_Grid


def allUnique(x):
    seen = list()
    return not any(i in seen or seen.append(i) for i in x)


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
    Repeat_Grid = collections.deque([])
    while Solution_Flag == 0:
        Output_Grid = output_random_grid(Grid, A, B, C)
        if Output_Grid in Repeat_Grid:
            continue
        else:
            Repeat_Grid.append(Output_Grid)
            # print(len(Repeat_Grid))
        new_grid = define_grid(Output_Grid)
        # print(new_grid)
        # print(as_string(new_grid))
        # time_wow = time.time()
        Solution_Flag = grid_outcome(P, L, new_grid)
        # print('wow')
        time_end = time.time()
        # print(time_end-time_wow)
        if time_end-start > 120:
            print('This puzzle cannot be solved in two minutes.')
            break
    return Output_Grid


if __name__ == '__main__':
    start = time.time()
    bfffile = 'bff_files\\tiny_5.bff'
    # bfffile=input('Please Enter the name of the .bff file to be solved: ')
    # bfffile='bff_files/' + bfffile
    P, A, B, C, L, Grid = ReadInbff(bfffile)
    solution_grid = ['o B x o o', 'o A o o o', 'A x o o A', 'o x A o x',
                     'A o x x A', 'B A x A o']
    solution_grid_num = ['B o o', 'A x x', 'B o A', 'A x o', 'B o o']
    solution_grid_mad = ['o o A o o', 'o o o A o', 'A o A o x', 'o o o A o',
                         'o o A o o']
    new_grid_sol = define_grid(solution_grid_mad)
    print(grid_outcome(P, L, new_grid_sol))
    ans = Block('o', 1, 1, 1)
    a = ans('o', 1, 0, 1)
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
    end = time.time()
    print('Time Elapsed: '+str(end-start)+' seconds')
    # Number of laser grid points is 2N*2N
