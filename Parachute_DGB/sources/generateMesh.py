import sys
import numpy as np
sys.path.append('../../AMR')
from Simplex import *

    
def parachute3D(type=0):
    '''
    To generate initial mesh for 3D parachute
    :param type: 0: just for canopy, 1: for both the whole parachute
    :return:
    '''
    # x direction, the parachute is in [-7.7235, 7.7235]
    # the fluid domain is [-150 150]
    xcl, xcr, nx = -15.0, 15.0, 61
    xc = np.linspace(xcl, xcr, nx)
    dxc = (xcr - xcl) / (nx - 1)
    xRatio = 1.1
    xl = geomspace(xcl, -80, -dxc, False, 'num', [xRatio])
    xr = geomspace(xcr, 80, dxc, False, 'num', [xRatio])


    x = [*reversed(xl),*xc,*xr]


    y = x
    # z direction, the parachute is in [35.7358, 39.2198]
    # the fluid domain is [-20 200]

    if(type == 0):
        zcl, zcr, nz = 25.0, 50.0, 51

    elif(type == 1):
        # zcl, zcr, nz = -10.0, 60.0, 141
        zcl, zcr, nz = -15.0, 65.0, 161
    zc = np.linspace(zcl, zcr, nz)
    dzc = (zcr - zcl)/(nz - 1)
    zRatio = 1.1
    zl = geomspace(zcl, -20, -dzc, False, 'num', [zRatio])
    zr = geomspace(zcr, 180, dzc, False, 'num', [zRatio])
    z = [*reversed(zl), *zc, *zr]

    boundaryNames = ['InletFixedSurface' for i in range(6)]
    print('len(x) ', len(x), ' len(y) ', len(y), ' len(z) ', len(z))
    simpleKuhnSimplex = KuhnSimplex(x,y,z, boundaryNames)

    print('Writing to top file')
    simpleKuhnSimplex.write_topfile(outputfile = 'fluid.top')
    
    
if __name__ == '__main__':
    parachute3D(type=1)