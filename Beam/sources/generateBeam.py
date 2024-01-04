import numpy as np




class Beam_Cable:


    def __init__(self,A,B,n,k,r, E,rho, v):
        self.A = A
        self.B = B
        self.E = E
        self.rho = rho
        self.v = v
        self.n = n
        self.k = k
        self.cable_r = r
        self.matcher_coord = self.compute_matcher_node_coordinates()
        self.phantom_coord = self.compute_phantom_node_coordinates()
        self.surface_coord = self.compute_surface_node()


    @staticmethod
    def write_nodes(coord, file_name, first_line):

        # NodeId, x coordinate, y coordinate, z coordinate
        file_name.write(first_line)
        # First part for the canopy
        id = 1
        for x, y, z in coord:
            file_name.write('%d   %.20E  %.20E  %.20E \n' % (id, x, y, z))
            id += 1




    def compute_matcher_node_coordinates(self):
        A = self.A
        B = self.B
        n = self.n
        coord = np.empty(shape=(n,3),dtype=float)
        for i in range(3):
            coord[:,i] = np.linspace(A[i],B[i],n)
        return coord

    def compute_phantom_node_coordinates(self):
        # cable AB
        # A = np.array([0.0,0.0,0.0],dtype=float)
        # B = np.array([0.0,0.0,1.0],dtype=float)

        # n = 20 # number of nodes on the cable AB
        # k = 6  # number of nodes on the phantom skeleton
        # cable_r = 0.1 # radius of cable
        # choose A cross e_1(1,0,0) as the first rigid phantom edge
        A = self.A
        B = self.B
        n = self.n
        k = self.k
        cable_r = self.cable_r

        X = np.empty(shape=[n, 3], dtype=float)
        for i in range(3):
            X[:, i] = np.linspace(A[i], B[i], num=n)

        nx, ny, nz = dir = (B - A) / np.linalg.norm(B - A)  # direction of AB
        e1 = np.array([1.0, 0.0, 0.0], dtype=float)

        theta = 2 * np.pi / k

        # Rotation matrix on https://en.wikipedia.org/wiki/Rotation_matrix
        R = np.array([[np.cos(theta) + nx * nx * (1 - np.cos(theta)),
                       nx * ny * (1 - np.cos(theta)) - nz * np.sin(theta),
                       nx * nz * (1 - np.cos(theta)) + ny * np.sin(theta)],
                      [ny * nx * (1 - np.cos(theta)) + nz * np.sin(theta),
                       np.cos(theta) + ny * ny * (1 - np.cos(theta)),
                       ny * nz * (1 - np.cos(theta)) - nx * np.sin(theta)],
                      [nz * nx * (1 - np.cos(theta)) - ny * np.sin(theta),
                       nz * ny * (1 - np.cos(theta)) + nx * np.sin(theta),
                       np.cos(theta) + nz * nz * (1 - np.cos(theta))]], dtype=float)

        phontom_dr = np.empty(shape=[k, 3], dtype=float)
        phontom_dr[0, :] = cable_r * np.cross(dir, e1)

        for i in range(1, k):
            phontom_dr[i, :] = np.dot(R, phontom_dr[i - 1, :])

        coord = np.empty(shape=[n * (k + 1), 3], dtype=float)
        for i in range(n):
            coord[i * (k + 1), :] = X[i, :]
            for j in range(1, k + 1):
                coord[i * (k + 1) + j, :] = X[i, :] + phontom_dr[j - 1, :]
        return coord



    def compute_surface_node(self):
        n = self.n
        A = self.A
        B = self.B
        cable_r = self.cable_r
        k = self.k
        # cable AB
        # A = np.array([0.0,0.0,0.0],dtype=float)
        # B = np.array([0.0,0.0,1.0],dtype=float)

        # n = 20 # number of nodes on the cable AB
        # k = 6  # number of nodes on the phantom skeleton
        # cable_r = 0.1 # radius of cable
        # choose A cross e_1(1,0,0) as the first rigid phantom edge


        X = np.empty(shape=[n, 3], dtype=float)
        for i in range(3):
            X[:, i] = np.linspace(A[i], B[i], num=n)

        nx, ny, nz = dir = (B - A) / np.linalg.norm(B - A)  # direction of AB
        e1 = np.array([1.0, 0.0, 0.0], dtype=float)

        theta = -2 * np.pi / k

        # Rotation matrix on https://en.wikipedia.org/wiki/Rotation_matrix
        R = np.array([[np.cos(theta) + nx * nx * (1 - np.cos(theta)),
                       nx * ny * (1 - np.cos(theta)) - nz * np.sin(theta),
                       nx * nz * (1 - np.cos(theta)) + ny * np.sin(theta)],
                      [ny * nx * (1 - np.cos(theta)) + nz * np.sin(theta),
                       np.cos(theta) + ny * ny * (1 - np.cos(theta)),
                       ny * nz * (1 - np.cos(theta)) - nx * np.sin(theta)],
                      [nz * nx * (1 - np.cos(theta)) - ny * np.sin(theta),
                       nz * ny * (1 - np.cos(theta)) + nx * np.sin(theta),
                       np.cos(theta) + nz * nz * (1 - np.cos(theta))]], dtype=float)

        phontom_dr = np.empty(shape=[k, 3], dtype=float)
        phontom_dr[0, :] = cable_r * np.cross(dir, e1)

        for i in range(1, k):
            phontom_dr[i, :] = np.dot(R, phontom_dr[i - 1, :])

        surface_coord = np.empty(shape=[n * k + 2, 3], dtype=float)
        surface_coord[0,:], surface_coord[-1,:] = A, B
        for i in range(n):
            for j in range(k):
                surface_coord[i * k + j + 1, :] = X[i, :] + phontom_dr[j - 1, :]

        return surface_coord

    def write_embedded_surface(self, outputfile = 'embeddedSurface.top'):
        n = self.n
        k = self.k
        surface_coord = self.surface_coord

        file_name = open(outputfile, 'w')
        first_line = 'Nodes nodeset\n'
        Beam_Cable.write_nodes(surface_coord, file_name, first_line)

        ##############################################################################################################

        file_name.write('Elements StickMovingSurface using nodeset\n')
        id = 1
        topo = 4
        
        temp = range(k)
        
        #triangle at the top
        temp = range(1,k+1)
        i = 1
        for j in range(k):
            file_name.write('%d   %d  %d  %d  %d\n' %(id, topo,  i, i + temp[j-1], i+temp[j]))
            id += 1


        for i in range(n - 1):
            for j in range(k):
                file_name.write('%d   %d  %d  %d  %d\n' % (id, topo, i * k + temp[j] + 1, i * k + temp[j - 1] + 1, (i + 1) * k + temp[j - 1] + 1))
                id += 1
                file_name.write('%d   %d  %d  %d  %d\n' % (id, topo, i * k + temp[j] + 1, (i + 1) * k + temp[j - 1] + 1, (i + 1) * k + temp[j] + 1))
                id += 1


        

        #triangles at bottom
        i = n*k + 2
        for j in range(k):
            file_name.write('%d   %d  %d  %d  %d\n' %(id, topo,  i, i - temp[j-1], i-temp[j]))
            id +=1



        file_name.close()



    def write_matcher_top_file(self, outputfile = 'structureFile.include'):

        n = self.n
        B = self.B
        A = self.A


        ################################################################################################################################
        ################################################################################################################################
        file_name = open(outputfile,'w')
        first_line = 'NODES\n'

        Beam_Cable.write_nodes(self.matcher_coord,file_name,first_line)
        file_name.write('*\n')
        file_name.write('TOPOLOGY\n')

        ##############################################################################################
        id=1
        #beam element 6
        topo = 6
        for i in range(1,n):
            file_name.write('%d   %d  %d  %d\n' %(id, topo,  i, i+1))
            id +=1

        attributes = 1
        file_name.write('ATTRIBUTS\n')
        file_name.write('%d   %d  %d\n' %(1, n-1, 1))
        file_name.write('*\n')


        file_name.write('EFRAMES\n')

        Sx = (B-A)/np.linalg.norm(B-A) # direction of AB
        e1 = np.array([1.0,0.0,0.0],dtype=float)

        Sy = np.cross(Sx,e1)
        Sz = np.cross(Sx,Sy)
       
        for id in range(1,n):
            file_name.write('%d  %.20E %.20E %.20E    %.20E %.20E %.20E    %.20E %.20E %.20E\n' %(id,  Sx[0],Sx[1],Sx[2],  Sy[0],Sy[1],Sy[2],  Sz[0],Sz[1],Sz[2]))
        file_name.write('*\n')

        file_name.write('DISP\n')
        for freedom in range(1,7):
            file_name.write('%d %d 0.0\n' %(n, freedom))
        file_name.write('*\n')
        file_name.close()



    
if __name__ == "__main__":
    '''
    The beam starts from A and ends at B
    Young's modulus : E
    Poisson ratio : v
    density : rho
    number of nodes : n
    shape of the cross-section of the cable : k
    cable radius : r
    '''
    A = np.array([0.0,0.0,0.0],dtype=float)
    B = np.array([0.0,0.0,8.0],dtype=float)
    E = 17e+6
    v = 0.42
    rho = 5200.0

    n = 100 # number of nodes on the cable AB
    k = 6  # number of nodes on the phantom skeleton
    cable_r = 0.0335 # radius of cable = 1.0e-3
    beam_cable = Beam_Cable(A,B,n,k,cable_r, E, rho, v)
    beam_cable.write_embedded_surface(outputfile = 'embeddedSurface.top')
    beam_cable.write_matcher_top_file(outputfile = 'StructureFile.include')

    
