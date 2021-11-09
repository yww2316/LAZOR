import unittest
from SolveLAZOR import *


class bffTest(unittest.TestCase):
    def setUp(self):
        '''
        Initialize the known answers here for unittesting
        '''
        self.bfffile = 'bff_files\\showstopper_4.bff'
        self.parseddata = [[2, 3]], 3, 3, 0,\
            [[3, 6, -1, -1]], ['B o o', 'o o o', 'o o o']
        self.reflect = (-1, 1)
        self.opaque = (0, 0)
        self.refract = (-1, 1, 1, 1)
        self.block = (-1, 1)
        self.define_grid =\
            [['o', 'o', 'oB', 'B', 'Bx', 'x', 'xo', 'o', 'oo', 'o', 'o'],
                ['o', 'o', 'oB', 'B', 'Bx', 'x', 'xo', 'o', 'oo', 'o', 'o'],
                ['o', 'oo', 'oBoo', 'Bo', 'Bxoo', 'xo', 'xooo', 'oo', 'oooo',
                 'oo', 'o'],
                ['o', 'o', 'oo', 'o', 'oo', 'o', 'oo', 'o', 'oo', 'o', 'o'],
                ['o', 'oo', 'ooox', 'ox', 'ooxo', 'oo', 'oooo', 'oo', 'oooo',
                 'oo', 'o'],
                ['o', 'o', 'ox', 'x', 'xo', 'o', 'oo', 'o', 'oo', 'o', 'o'],
                ['o', 'oo', 'oxox', 'xx', 'xoxo', 'oo', 'oooo', 'oo', 'ooox',
                 'ox', 'o'],
                ['o', 'o', 'ox', 'x', 'xo', 'o', 'oo', 'o', 'ox', 'x', 'x'],
                ['o', 'oo', 'oxoo', 'xo', 'xoox', 'ox', 'ooxx', 'ox', 'oxxo',
                 'xo', 'x'],
                ['o', 'o', 'oo', 'o', 'ox', 'x', 'xx', 'x', 'xo', 'o', 'o'],
                ['o', 'oB', 'ooBo', 'oo', 'oxox', 'xx', 'xxxo', 'xo', 'xooo',
                 'oo', 'o'],
                ['B', 'B', 'Bo', 'o', 'ox', 'x', 'xo', 'o', 'oo', 'o', 'o'],
                ['B', 'B', 'Bo', 'o', 'ox', 'x', 'xo', 'o', 'oo', 'o', 'o']]
        self.Grid = ['o B x o o', 'o o o o o', 'o x o o o', 'o x o o x',
                     'o o x x o', 'B o x o o']
        self.possible_grid =\
            [['o', 'o', 'oB', 'B', 'Bx', 'x', 'xA', 'A', 'Ao', 'o', 'o'],
                ['o', 'o', 'oB', 'B', 'Bx', 'x', 'xA', 'A', 'Ao', 'o', 'o'],
                ['o', 'oo', 'oBoA', 'BA', 'BxAo', 'xo', 'xAoA', 'AA', 'AoAA',
                    'oA', 'o'],
                ['o', 'o', 'oA', 'A', 'Ao', 'o', 'oA', 'A', 'AA', 'A', 'A'],
                ['o', 'oo', 'oAox', 'Ax', 'AoxA', 'oA', 'oAAo', 'Ao', 'AAoo',
                    'Ao', 'A'],
                ['o', 'o', 'ox', 'x', 'xA', 'A', 'Ao', 'o', 'oo', 'o', 'o'],
                ['o', 'oA', 'oxAx', 'xx', 'xAxo', 'Ao', 'AooA', 'oA', 'ooAx',
                    'ox', 'o'],
                ['A', 'A', 'Ax', 'x', 'xo', 'o', 'oA', 'A', 'Ax', 'x', 'x'],
                ['A', 'Ao', 'Axoo', 'xo', 'xoox', 'ox', 'oAxx', 'Ax', 'Axxo',
                    'xo', 'x'],
                ['o', 'o', 'oo', 'o', 'ox', 'x', 'xx', 'x', 'xo', 'o', 'o'],
                ['o', 'oB', 'ooBo', 'oo', 'oxox', 'xx', 'xxxA', 'xA', 'xoAo',
                    'oo', 'o'],
                ['B', 'B', 'Bo', 'o', 'ox', 'x', 'xA', 'A', 'Ao', 'o', 'o'],
                ['B', 'B', 'Bo', 'o', 'ox', 'x', 'xA', 'A', 'Ao', 'o', 'o']]
        self.laser_pos =\
            [(4, -1), (4, 1), (4, 3), (5, 0), (5, 2), (5, 4), (6, 1), (6, 3)]
        self.refract_list = []
        self.result_sort =\
            [(4, 1), (4, 3), (5, 0), (5, 2), (5, 4), (6, 1), (6, 3)]

        self.Solution_Grid = ['o B x o o', 'o A o o o', 'A x o o A',
                              'o x A o x', 'A o x x A', 'B A x A o']
        self.P = [[6, 9], [9, 2]]
        self.L = [[4, 1, 1, 1]]
        self.sol_grid = ['o B x o o', 'o A o o o', 'A x o o A', 'o x A o x',
                         'A o x x A', 'B A x A o']

    def test_Check_Parsing(self):
        '''
        Checks to make sure that the desired data is parsed correctly.
        '''
        self.assertEqual(ReadInbff(self.bfffile), self.parseddata,
                         'The file data was not parsed correctly.')

    def test_Check_Reflect(self):
        '''
        Checks to make sure that the reflect block outputs the
        correct velocities.
        '''
        self.assertEqual(Block.Reflect(1, 1, 1), self.reflect,
                         'The reflect block information\
                         is not saved correctly.')

    def test_Check_Opaque(self):
        '''
        Checks to make sure that the opaque block outputs the 0 velocity.
        '''
        self.assertEqual(Block.Opaque(1, 1, 1), self.opaque,
                         'The opaque block information\
                         is not saved correctly.')

    def test_Check_Refract(self):
        '''
        Checks to make sure that the refract block outputs the 0 velocity.
        '''
        self.assertEqual(Block.Refract(1, 1, 1), self.refract,
                         'The refract block information\
                         is not saved correctly.')

    def test_Block_call(self):
        '''
        Checks to ensure that the correct velocities are
        outputted when a specific block is called.
        '''
        bah = Block('B', 1, 2, 1)
        self.assertEqual(bah('A', 1, 1, 1), self.block,
                         'The block information is not saved correctly.')

    def test_define_grid(self):
        '''
        Checks to make sure that the grid coordinates are outputted
        correctly by the define_grid function.
        '''
        self.assertEqual(define_grid(self.Grid), self.define_grid,
                         'The grid coordinates were not generated correctly.')

    def test_Solve_LAZOR(self):
        '''
        Checks to makes sure that a random grid is ouputted.
        '''
        P, A, B, C, L, Grid = self.parseddata
        self.assertTrue(Solve_LAZOR('bff_files\\yarn_5.bff') ==
                        self.sol_grid, 'The incorrect grid was outputted')

    def test_grid_outcome(self):
        '''
        Checks to make sure that grid_outcome identifies a correct solution.
        '''
        self.assertTrue(grid_outcome(self.P, self.L,
                                     define_grid(self.sol_grid)),
                        'The incorrect grid outcome was outputted')

    def test_get_all_paths_taken(self):
        '''Checks to make sure that get_all_paths_taken returns all
        of the correct paths taken by the laser'''
        self.assertEqual(get_all_paths_taken(self.L, self.possible_grid),
                         self.result_sort)

    def test_path_loop(self):
        '''Checks to make sure that path_loop returns the correct laser
        positions and the correct unused refract list that arises from
        hitting a C block'''
        a, b = path_loop(self.L, self.possible_grid)
        self.assertEqual(a, self.laser_pos)
        self.assertEqual(b, self.refract_list)


if __name__ == '__main__':
    unittest.main()
