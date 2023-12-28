import sys
import numpy as np
sys.path.append('../../../AMR')
from Simplex import *

def agard3D():

    ratio = 1.3
    
    eps = 0.0
    x = uniform_exponential_stretch(-1.0 - 1.0/3.0, 23.0 - 1.0/3.0,  33,  -100,  150, ratio, ratio)
    y = uniform_exponential_stretch(0.0 + eps,   33.0 + eps,   45,     0,  150, -1,    ratio)
    z = uniform_exponential_stretch(-1.0 -1.0/3.0 , 11.0 - 1.0/3.0,  25,  -100,  100, ratio, ratio)

    print("len(x), len(y), len(z) = ", len(x), len(y), len(z), " total node number: ", len(x)*len(y)*len(z))

    boundaryNames=['InletFixedSurface', 'InletFixedSurface',    'InletFixedSurface',
                   'InletFixedSurface', 'SymmetryFixedSurface', 'InletFixedSurface']
    simpleKuhnSimplex = KuhnSimplex(x,y,z,boundaryNames)

    # map x, y, z to x+y, y, z
    nodes = simpleKuhnSimplex.nodes
    n = nodes.shape[0]
    print(nodes.shape)
    for i in range(n):
        nodes[i, 0] = nodes[i, 0] + nodes[i, 1]


    print('Writing to top file')
    simpleKuhnSimplex.write_topfile(outputfile = 'fluid.top')


if __name__ == '__main__':
    agard3D()
