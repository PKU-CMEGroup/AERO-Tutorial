__author__ = 'Daniel Zhengyu Huang'

import sys
import numpy as np
def read_tet(mshfile):
    '''
    This function reads top file, mshfile, extract the node coordinates in the list nodes,
    and element node numbers in elems(the node number is 0-based index instead of top file'
    1-based index)
    :param mshfile: top file name
    :return: nodes, elems
    '''

    try:
        file = open(mshfile, "r")
    except IOError:
        print("File '%s' not found." % mshfile)
        sys.exit()

    nodes = []
    elems = []
    boundaryNames = []
    boundaries = []

    print('Reading mesh ...')

    # Read nodes
    line = file.readline()  # should be "Nodes FluidNodes"
    while line:
        line = file.readline()
        data = line.split()
        if data[0] == 'Elements':
            break;
        nodes.append(list(map(float, data[1:4])))

    # Read Elements
    line = file.readline()
    while line:
        data = line.split()
        if data[0] == 'Elements':
            break;
        elem = list(map(int, data[2:6]))
        elem = [x - 1 for x in elem]  # fixed top file 1-based index
        elems.append(elem)
        line = file.readline()

    # Read Boundaries
    while line:
        boundary = []
        boundaryName = data[1]
        line = file.readline()
        while line:
            data = line.split()
            if data[0] == 'Elements':
                break;
            tri = list(map(int, data[2:5]))
            tri = [x - 1 for x in tri]  # fixed top file 1-based index
            boundary.append(tri)
            line = file.readline()
        boundaries.append(boundary)
        boundaryNames.append(boundaryName)

    file.close()

    return nodes, elems, boundaryNames, boundaries

def write_tet(nodes,elems, boundaryNames, boundaries, mshfile = 'domain.top', volFunc = lambda x: 0):
    '''
    This function writes top file, mshfile, node coordinates are  in the list nodes,
    and element node numbers are in elems(the node number is 0-based index instead of top file'
    1-based index)
    :param mshfile: top file name
    :param nodes: a list of node coordinates
    :param elems: a list of elems node number
    :param boundaries: a list of several lists, each sublist is a list of boundary triangle node numbers
    :param volFunc: function returns 0, 1, 2, 3... input point, return the point's volume label
    '''

    file = open(mshfile, 'w')
    nNodes,nElems = len(nodes), len(elems)

    file.write('Nodes FluidNodes\n')
    for nN in range(nNodes):
        file.write('%d  %.12f  %.12f  %.12f\n'%(nN + 1, nodes[nN][0],nodes[nN][1],nodes[nN][2]))

    iElems, volLabel = 0,0
    while(iElems < nElems):
        print('Elements FluidMesh_%d using FluidNodes\n'%volLabel)
        file.write('Elements FluidMesh_%d using FluidNodes\n'%volLabel)
        for nE in range(nElems):
            xc = (np.array(nodes[elems[nE][0]]) + np.array(nodes[elems[nE][1]]) + np.array(nodes[elems[nE][2]]) + np.array(nodes[elems[nE][3]]))/4.0
            if volFunc(xc) == volLabel:
                file.write('%d  %d  %d  %d  %d  %d\n'%(nE + 1, 5, elems[nE][0] + 1, elems[nE][1] + 1, elems[nE][2] + 1,elems[nE][3] + 1))
                iElems = iElems + 1
        volLabel = volLabel + 1
    nBounds = len(boundaries)
    for i in range(nBounds):
        if(boundaries == 'None'):
            continue
        file.write('Elements %s using FluidNodes\n' %(boundaryNames[i] + '_' + str(i+volLabel)))
        boundary = boundaries[i]
        nTris = len(boundary)
        for nT in range(nTris):
            nE += 1
            file.write('%d  %d  %d  %d  %d\n' % (nE, 4, boundary[nT][0] + 1, boundary[nT][1] + 1, boundary[nT][2] + 1))

    file.close()
    print('Write to top file, %d nodes and %d elements' %(len(nodes), len(elems)))



class KuhnSimplex:
    def __init__(self,x,y,z, boundaryNames):
        '''
        :param x: float array
        :param y: float array
        :param z: float array
        :param boundaryNames:  [bottom z = zmin, top  z = zmax, left x = xmin,
                                      right x = xmax, front y = ymin, back y = ymax]
        '''
        self.x,  self.y,  self.z = x,y,z
        self.nx, self.ny, self.nz = len(x), len(y), len(z)
        self.nodes = self.create_nodes()
        self.eles = self.create_tet()
        self.boundaries = self.create_boundaries()
        self.boundaryNames = boundaryNames


    def _node_id(self,ix,iy,iz):
        nx, ny, nz = self.nx, self.ny, self.nz
        return ix + iy*nx + iz*nx*ny

    def create_nodes(self):
        x,y,z = self.x, self.y, self.z
        nx, ny, nz = self.nx, self.ny, self.nz


        nodes = np.empty((nx*ny*nz, 3))

        xx,yy,zz = np.meshgrid(x,y,z)

        nodes[:, 0] = np.reshape(np.reshape(xx, (-1, nz)), (1, -1), order='F')
        nodes[:, 1] = np.reshape(np.reshape(yy, (-1, nz)), (1, -1), order='F')
        nodes[:, 2] = np.reshape(np.reshape(zz, (-1, nz)), (1, -1), order='F')

        return nodes





    def create_tet(self):
        '''
        :param xx:
        :param yy:
        :param zz:
        cut each small cube into 6 tetrahedrons

        nodes = [n0,n1,n2,n3,n4,n5,n6,n7]

        n0: (0,0,0)
        n1: (1,0,0)
        n2: (0,1,0)
        n3: (1,1,0)
        n4: (0,0,1)
        n5: (1,0,1)
        n6: (0,1,1)
        n7: (1,1,1)

        T(1 2 3) n0(0, 0, 0), n1(1, 0, 0), n3(1, 1, 0), n7(1, 1, 1)
        T(1 3 2) n0(0, 0, 0), n1(1, 0, 0), n5(1, 0, 1), n7(1, 1, 1)
        T(2 1 3) n0(0, 0, 0), n2(0, 1, 0), n3(1, 1, 0), n7(1, 1, 1)
        T(3 1 2) n0(0, 0, 0), n2(0, 1, 0), n6(0, 1, 1), n7(1, 1, 1)
        T(3 2 1) n0(0, 0, 0), n4(0, 0, 1), n6(0, 1, 1), n7(1, 1, 1)
        T(2 3 1) n0(0, 0, 0), n4(0, 0, 1), n5(1, 0, 1), n7(1, 1, 1)

        :return:
        '''
        nx, ny, nz = self.nx, self.ny, self.nz

        eles = np.empty((6*(nx - 1) * (ny - 1) * (nz - 1), 4), dtype=int)
        for k in range(nz - 1):
            for j in range(ny - 1):
                for i in range(nx - 1):
                    cubeId = i + j*(nx-1) + k*(nx-1)*(ny-1)
                    nn = [self._node_id(i, j, k), self._node_id(i + 1, j, k), self._node_id(i, j + 1, k), self._node_id(i + 1, j + 1, k),
                          self._node_id(i, j, k + 1), self._node_id(i + 1, j, k + 1), self._node_id(i, j + 1, k + 1), self._node_id(i + 1, j + 1, k + 1)]
                    eles[6 * cubeId:6 * (cubeId + 1), :] = [[nn[0], nn[1], nn[3], nn[7]],
                                                  [nn[0], nn[1], nn[5], nn[7]],
                                                  [nn[0], nn[2], nn[3], nn[7]],
                                                  [nn[0], nn[2], nn[6], nn[7]],
                                                  [nn[0], nn[4], nn[6], nn[7]],
                                                  [nn[0], nn[4], nn[5], nn[7]]]

        return eles

    def create_boundaries(self):
        nx, ny, nz = self.nx, self.ny, self.nz
        tri = [[],[],[],[],[],[]]
        # bottom z = zmin
        for j in range(ny - 1):
            for i in range(nx - 1):
                k = 0
                tri[0].append([self._node_id(i, j, k), self._node_id(i + 1, j, k), self._node_id(i + 1, j + 1, k)])
                tri[0].append([self._node_id(i, j, k), self._node_id(i + 1, j + 1, k), self._node_id(i, j + 1, k)])


        # top  z = zmax
        for j in range(ny - 1):
            for i in range(nx - 1):
                k = nz - 1
                tri[1].append([self._node_id(i, j, k), self._node_id(i + 1, j, k), self._node_id(i + 1, j + 1, k)])
                tri[1].append([self._node_id(i, j, k), self._node_id(i + 1, j + 1, k), self._node_id(i, j + 1, k)])

        # left x = xmin
        for k in range(nz - 1):
            for j in range(ny - 1):
                i = 0
                tri[2].append([self._node_id(i, j, k), self._node_id(i , j + 1, k),     self._node_id(i, j + 1, k + 1)])
                tri[2].append([self._node_id(i, j, k), self._node_id(i , j + 1, k + 1), self._node_id(i, j , k + 1)])
        # right x = xmax
        for k in range(nz - 1):
            for j in range(ny - 1):
                i = nx - 1
                tri[3].append([self._node_id(i, j, k), self._node_id(i, j + 1, k), self._node_id(i, j + 1, k + 1)])
                tri[3].append([self._node_id(i, j, k), self._node_id(i, j + 1, k + 1), self._node_id(i, j, k + 1)])
        # front y = ymin
        for k in range(nz - 1):
            for i in range(nx - 1):
                j = 0
                tri[4].append([self._node_id(i, j, k), self._node_id(i, j , k + 1), self._node_id(i + 1, j, k + 1)])
                tri[4].append([self._node_id(i, j, k), self._node_id(i + 1, j, k + 1), self._node_id(i + 1, j, k)])
        # back y = ymax
        for k in range(nz - 1):
            for i in range(nx - 1):
                j = ny - 1
                tri[5].append([self._node_id(i, j, k), self._node_id(i, j, k + 1), self._node_id(i + 1, j, k + 1)])
                tri[5].append([self._node_id(i, j, k), self._node_id(i + 1, j, k + 1), self._node_id(i + 1, j, k)])


        return tri

    def write_topfile(self, outputfile = 'domain.top', volFunc = lambda x: 0):
        nodes = self.nodes
        eles = self.eles
        boundaries = self.boundaries
        boundaryNames = self.boundaryNames
        write_tet(nodes, eles, boundaryNames, boundaries, outputfile, volFunc)


    def plot_mesh(self):
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        eles  = self.eles
        nodes = self.nodes
        for e in eles:
            for i in range(4):
                for j in range(i+1,4):
                    x = [nodes[e[i],0],nodes[e[j],0]]
                    y = [nodes[e[i],1],nodes[e[j],1]]
                    z = [nodes[e[i],2],nodes[e[j],2]]
                    ax.plot(x,y,z)
        plt.show()



def uniform_exponential_stretch(xa, xb, nab, Xa, Xb, ra, rb):
    xx_in = np.linspace(xa, xb, nab)
    dx_ab = xx_in[1] - xx_in[0]

    xx_a = []
    if ra > 0:
        xa_p = xa
        dxa_p = dx_ab
        while xa_p > Xa:
            xa_p -= dxa_p
            dxa_p *= ra
            xx_a.insert(0, xa_p)

    xx_b = []
    if rb > 0:
        xb_p = xb
        dxb_p = dx_ab
        while xb_p < Xb:
            xb_p += dxb_p
            dxb_p *= rb
            xx_b.append(xb_p)
    
    return np.concatenate((np.array(xx_a), xx_in, np.array(xx_b)))


def geomspace(x0, xn, dx0, includeX0, type, ratio):
    '''
    :param x0: float, start point
    :param xn: float, end point (end point is beyond xn)
    :param dx0: float, increment at x0
    :param includeX0, bool, should the array include x0 or not
    :param type: string 'num' or 'dist'
    :param ratio: list of float
           [float, int; float, int, float ...]
           [float float; float, float; , float ...]
    :return: xx
           ratio has n pairs(ci, yi), y of the last pair is optional
           xx array has n segments, in each segment the increment dx
           is a geometric sequence of ratio ci
           if type = 'num', each segment has yi points,
           the ratio is interpreted as c1, n1, c2, n2 ...
           the incremental array is dx, dx*c1, dx*c1^2 ... dx*c1^(n1-1),
           dx*c1^(n1-1)*c2, dx*c1^(n1-1)*c2^2 ...dx*c1^(n1-1)*c2^(n2-1)...
           if type = 'dist', each segment has length > yi - yi-1
           the ratio is interpreted as c1, n1, c2, n2 ...
           the incremental array is dx, dx*c1, dx*c1^2 ... dx*c1^(n1-1),
           dx*c1^(n1-1)*c2, dx*c1^(n1-1)*c2^2 ...dx*c1^(n1-1)*c2^(n2-1)...
           ni in this case is computed based on yi
    '''

    n = (len(ratio) + 1)//2
    xx = [x0] if includeX0 else []

    if(type == 'num'):
        x, dx = x0, dx0
        if len(ratio) % 2:
            ratio.append(int(1e12))#append any large number
        for i in range(n):
            for j in range(ratio[2*i + 1]):
                x = x + dx
                xx.append(x)
                dx *= ratio[2 * i]
                if(x0 < xn and x > xn) or (x0 > xn and x < xn):
                    break

    if(type == 'dist'):
        x, dx = x0, dx0
        if len(ratio) % 2:
            ratio.append(xn)
        for i in range(n):
            xc = x0 + ratio[2*i + 1]
            while (x0 < xc and x < xc) or (x0 > xc and x > xc):
                x = x + dx
                xx.append(x)
                dx *= ratio[2 * i]



    return xx

def symmetry(xx, type):
    '''
    :param xx: array {x0, x1, x2}
    :param type: string, 'left' or 'right'
    :return: mirror the array to left or right
             if type = 'left' xx = {2x0 - x2, 2x0 - x1, x0, x1, x2}
             if type = 'right' xx = {x0, x1, x2, 2x2 - x1, 2x2 - x0}
    '''

    n = len(xx)

    if(type == 'left'):
        xx_temp = []
        xc = xx[0]
        for i in range(n - 1, 0, -1):
            xx_temp.append(2*xc - xx[n - 1 - i])
        xx = xx_temp + xx
    if(type == 'right'):
        xc = xx[-1]
        for i in range(n - 1):
            xx.append(2*xc - xx[n - 1 - i - 1])
    return xx
