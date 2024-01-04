import sys
import numpy as np
sys.path.append('../../AMR')
from Simplex import *


def uniform3D():
    # for sphere

    x = np.linspace(-2.0,      4.0,       31)
    y = np.linspace(-2.0,      2.0,       21)
    z = np.linspace(-2.0,      8.0,       51)



    boundaryNames=['InletFixedSurface','SymmetrySurface','InletFixedSurface',
                   'InletFixedSurface','InletFixedSurface','InletFixedSurface']
    simpleKuhnSimplex = KuhnSimplex(x,y,z,boundaryNames)

    print('Writing to top file')
    simpleKuhnSimplex.write_topfile(outputfile = 'fluid.top')
    
    
if __name__ == '__main__':
    uniform3D()