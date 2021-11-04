from os import X_OK
import unittest
from SolveLAZOR import *
from SolveLAZOR import Block


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
        self.defie_grid = [['o', 'o', 'oB', 'B', 'Bx', 'x', 'xo', 'o', 'oo', 'o', 'o'], ['o', 'o', 'oB', 'B', 'Bx', 'x', 'xo', 'o', 'oo', 'o', 'o'], ['o', 'oo', 'oBoo', 'Bo', 'Bxoo', 'xo', 'xooo', 'oo', 'oooo', 'oo', 'o'], ['o', 'o', 'oo', 'o', 'oo', 'o', 'oo', 'o', 'oo', 'o', 'o'], ['o', 'oo', 'ooox', 'ox', 'ooxo', 'oo', 'oooo', 'oo', 'oooo', 'oo', 'o'], ['o', 'o', 'ox', 'x', 'xo', 'o', 'oo', 'o', 'oo', 'o', 'o'], ['o', 'oo', 'oxox', 'xx', 'xoxo', 'oo', 'oooo', 'oo', 'ooox', 'ox', 'o'], ['o', 'o', 'ox', 'x', 'xo', 'o', 'oo', 'o', 'ox', 'x', 'x'], ['o', 'oo', 'oxoo', 'xo', 'xoox', 'ox', 'ooxx', 'ox', 'oxxo', 'xo', 'x'], ['o', 'o', 'oo', 'o', 'ox', 'x', 'xx', 'x', 'xo', 'o', 'o'], ['o', 'oB', 'ooBo', 'oo', 'oxox', 'xx', 'xxxo', 'xo', 'xooo', 'oo', 'o'], ['B', 'B', 'Bo', 'o', 'ox', 'x', 'xo', 'o', 'oo', 'o', 'o'], ['B', 'B', 'Bo', 'o', 'ox', 'x', 'xo', 'o', 'oo', 'o', 'o']]

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
        Grid = ['o B x o o', 'o o o o o', 'o x o o o', 'o x o o x', 'o o x x o', 'B o x o o']
        self.assertEqual(define_grid(Grid), self.define_grid,
                         'The grid coordinates were not generated correctly.')

    def test_Solve(self):
        '''
        Checks to make sure that the correct solution is outputted
        by the solve function.
        '''
        P, A, B, C, L, Grid = self.parseddata
        self.assertTrue(type(solve_lazor(P, A, B, C, L, Grid)) is list)

    def test_random_grid(self):
        '''
        Checks to makes sure that a random grid is ouputted.
        '''
        P, A, B, C, L, Grid = self.parseddata
        self.assertTrue(type(output_random_grid(Grid, A, B, C, [])) is tuple)


if __name__ == '__main__':
    unittest.main()
