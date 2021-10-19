'''
Initial python file for reading in .bff files for their information.
'''

import numpy as np
import re

P=[]
Grid=[]
bfffile='specific.bff'
copy=False
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
        elif line.startswith('C'):
            C=int(line.partition('C')[2].strip())
        elif line.startswith('L'):
            appending=line.partition('L')[2].strip()
            appending=[int(i) for i in appending.split() if i.isdigit()]
            L=appending
        elif line.startswith('GRID START'):
            copy=True
            continue
        elif line.startswith('GRID STOP'):
            copy=False
            continue
        elif copy:
            Grid.append(line.strip())
