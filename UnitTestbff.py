import unittest
from ReadInbff import *


class bffTest(unittest.TestCase):
    def setUp(self):
        # Initialize the desired variables here
        self.bfffile='blah'
        # self.parseddata=
        # self.opaque=
    def Check_Parsing(self):
        self.assertEqual(ReadInbff(self.bfffile), self.parseddata,'The file data was not parsed correctly.')

    def Check_Opaque_Physics(self):
        self.assertEqual(self.Block.oqaque(), self.opaque,'The opaque block information is not saved correctly.' )
    
    