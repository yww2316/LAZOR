from os import X_OK
import unittest
from ReadInbff import *
from ReadInbff import Block


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
