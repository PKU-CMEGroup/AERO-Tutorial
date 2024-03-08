#################################
# This file read structure file
# it can refine the canopy
# and fold the canopy
# write down new structure file with IDIPS6
# See main function for more details
#################################
import sys
import numpy as np
from scipy.optimize import fsolve
import Line


def matrix_to_angles(rten, eps=1.e-6):
    # # R = Rz * Ry * Rx
    # # return theta_x, theta_y, theta_z
    # def check(psi, phi, theta, A):
    #     a11 = A[0, 1] - (-np.cos(phi) * np.sin(psi) + np.sin(phi) * np.sin(theta) * np.cos(psi))
    #     a12 = A[0, 2] - (np.sin(phi) * np.sin(psi) + np.cos(phi) * np.sin(theta) * np.cos(psi))
    #     a21 = A[1, 1] - (np.cos(phi)  * np.cos(psi) + np.sin(phi) * np.sin(theta) * np.sin(psi))
    #     a22 = A[1, 2] - (-np.sin(phi) * np.cos(psi) + np.cos(phi) * np.sin(theta) * np.sin(psi))
    #     return (np.abs(a11) < eps and np.abs(a12) < eps and np.abs(a21) < eps and np.abs(a22) < eps)
    #
    # if (R[0,0]**2 + R[1,0]**2 < eps):
    #
    #     if(np.abs(R[0,1] + R[1,2]) < eps and np.abs(R[0,2] - R[1,1]) < eps):
    #         theta = np.pi / 2.0
    #         psi = 0.0
    #         phi = np.arctan2(R[1,1], R[1,2]) + psi
    #     elif(np.abs(R[0,1] - R[1,2]) < eps and np.abs(R[0,2] + R[1,1]) < eps):
    #         theta = -np.pi/2.0
    #         psi = 0.0
    #         phi = - np.arctan2(R[1, 1], R[1, 2]) - psi
    #     else:
    #         print('ERROR in matrix to angles costheta == 0')
    #         exit(1)
    #
    # else:
    #     theta = -np.arcsin(R[2,0])
    #     c_sign = np.sign(np.cos(theta))
    #     psi = np.arctan2(R[1,0] * c_sign, R[0,0] * c_sign)
    #     phi = np.arctan2(R[2,1] * c_sign, R[2,2] * c_sign)
    #
    #     if(not check(psi, phi, theta, R)):
    #         theta = np.pi + np.arcsin(R[2, 0])
    #         c_sign = np.sign(np.cos(theta))
    #         psi = np.arctan2(R[1, 0] * c_sign, R[0, 0] * c_sign)
    #         phi = np.arctan2(R[2, 1] * c_sign, R[2, 2] * c_sign)
    #         if (not check(psi, phi, theta, R)):
    #             print('ERROR in matrix to angles costheta != 0')
    #             print(R, np.linalg.eig(R))
    #             print(np.dot(R, R.T))
    #             exit(1)



    p = np.array([0, 1, 2, 0, 1], dtype= int)
    q = np.zeros(4) #quarternion
    trace = rten[0][0] + rten[1][1] + rten[2][2]

    imax = 0
    if (rten[1][1] > rten[imax][imax]):
        imax = 1
    if (rten[2][2] > rten[imax][imax]):
        imax = 2;

    if (trace > rten[imax][imax]):
        q[0] = np.sqrt(1.0 + trace) / 2.0
        q[1] = (rten[2][1] - rten[1][2]) / (4.0 * q[0])
        q[2] = (rten[0][2] - rten[2][0]) / (4.0 * q[0])
        q[3] = (rten[1][0] - rten[0][1]) / (4.0 * q[0])

    else:
        i = p[imax];
        j = p[imax + 1];
        k = p[imax + 2];
        q[i + 1] = np.sqrt(rten[i][i] / 2.0 + (1.0 - trace) / 4.0);
        q[0] = (rten[k][j] - rten[j][k]) / (4.0 * q[i + 1]);
        q[j + 1] = (rten[j][i] + rten[i][j]) / (4.0 * q[i + 1]);
        q[k + 1] = (rten[k][i] + rten[i][k]) / (4.0 * q[i + 1]);


    if (q[0] < 0):
        print("negative quaternion in mat_to_quat\n")
        for l in range(4):
            q[l] = -q[l]




    sthh = np.sqrt(q[1] * q[1] + q[2] * q[2] + q[3] * q[3])


    cthh = q[0];
    if (sthh < 0.7):
        th = 2.0 * np.arcsin(sthh);
    else:
        th = 2.0 * np.arccos(cthh);

    if (sthh <= eps):
        coef = 2.0;
    else:
        if ( sthh > 1.0 ):
            sthh = 1.0
        coef = th / sthh



    return coef * q[1], coef * q[2], coef * q[3]




class Elem:
    def __init__(self, id, nodes, att = 0, eframe = None):
        self.id = id
        self.nodes = nodes
        self.att = att
        self.eframe = eframe

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def ReadNodes(file):
    line = file.readline()  # should be "Nodes FluidNodes"
    while line:
        data = line.split()
        if data[0] == 'NODES' or data[0] == 'Nodes':
            break
        line = file.readline()
    print('ReadNodes, the first line is ', line)
    nodes = []
    while line:
        line = file.readline()
        data = line.split()
        if data[0][0] == '*' or data[0] == 'NODES' or data[0] == 'Nodes':
            continue
        if RepresentsInt(data[0]):
            nodes.append(list(map(float, data[1:4])))
        else:
            break

    print("ReadNodes reads ", len(nodes), " nodes")
    return file, line, nodes
def pair(a,b):
    return (min(a,b), max(a,b))

def ReadElems(file, line):
    print('\n\n*ReadElems, the first line is ', line)
    elems = []
    type = -1
    print(line)
    name = line.split()[1]
    while line:
        line = file.readline()
        data = line.split()
        if not line or data[0][0] == '*':
            continue
        if RepresentsInt(data[0]):
            type = len(data) - 2
            elems.append(Elem(int(data[0]), list(map(int, data[2:]))))

        else:
            break
    if line.split()[0]  == 'ATTRIBUTES':
        ind = 0
        while line:
            line = file.readline()
            data = line.split()
            if not line or data[0][0] == '*':
                continue
            if RepresentsInt(data[0]):
                if len(data) == 2:
                    elems[ind].att = int(data[1])
                    assert(elems[ind].id == int(data[0]))
                    ind += 1
                elif len(data) == 3:
                    for ele_id in range(int(data[0]), int(data[1]) + 1):
                        elems[ind].att = int(data[2])
                        assert(elems[ind].id == int(ele_id))
                        ind += 1

            else:
                break
    if line.split()[0]  == 'EFRAMES':
        ind = 0
        while line:
            line = file.readline()
            data = line.split()
            if not line or data[0][0] == '*':
                continue
            if RepresentsInt(data[0]):
                elems[ind].eframe = list(map(float, data[1:]))
                assert(elems[ind].id == int(data[0]))
                ind += 1

            else:
                break
    print('ReadElems reads ', len(elems), ' ', name, ' elems')
    return file, line, elems, type, name


def line_to_circle(theta, data):
    a = data[0]
    return a*theta - 2 * np.sin(theta/2.)

def SplitLines(line_elems):
    '''
    :param line_elems:
    :return:
    '''
    j_old = -1
    line, lines = [], []
    for i_e in range(len(line_elems)):
        i,j = line_elems[i_e].nodes
        if i != j_old:
            if line:
                lines.append(line)
            line = [i,j]

        else:
            line.append(j)
        j_old = j
    lines.append(line)
    return lines

class Mesh:
    '''
    #  nodes set
    #  topology set
    '''
    def __init__(self, fabric_elem_type = 4):
        self.nodes = None
        self.ele_set = []
        self.ele_set_info = []
        self.fabric_elem_type = fabric_elem_type

    def read_stru(self, file_name):
        '''
        :param inputStru:
        :param beamPars: parameters to handle phantom surface, skip beamPars[0] beams at all ends of these lines, the shape of
        the cross section beamPars[1], 4 for square, radius of the cross section beamPars[2]
        :return: nodes: a list of 3 double,
                 elems: a list of 3 int
        '''

        try:
            stru_file = open(file_name, "r")
        except IOError:
            print("File '%s' not found." % file_name)
            sys.exit()


        print('Reading Structure mesh ...')
        file, line, self.nodes = ReadNodes(stru_file)
        while line:
            '''
            It should read (0)Band Gores, Disk Gores, (1)Gap Lines, (2)Suspension Lines, (3)Vent Lines
            '''
            stru_file, line, elems, type, name = ReadElems(stru_file, line)
            self.ele_set.append(elems)
            self.ele_set_info.append([name, type])
        stru_file.close()

    def refine(self, refine_all_beams_or_not = True):
        '''
        add nodes, append to nodes
        change quad
        change beams in quad
        change other beams
        :return:
        '''


        nodes = self.nodes
        ele_set = self.ele_set
        ele_set_info = self.ele_set_info

        n_n = len(nodes) # save number of nodes
        n_es = len(ele_set)

        edge_to_center_node = {}
        new_ele_set = []

        ################   Update canopy
        for i_es in range(n_es): #loop element sets, like Suspension_Lines, Band_Gores ...
            ele = ele_set[i_es]
            ele_info = ele_set_info[i_es]
            new_ele = []
            if ele_info[1] == 2:
                print('beam')
                #beam
            elif ele_info[1] == 4:
                print('quad')
                n_e = len(ele)
                for i_e in range(n_e):
                    id = ele[i_e].id
                    att = ele[i_e].att
                    eframe = ele[i_e].eframe
                    ele_nodes = ele[i_e].nodes
                    new_nodes = [0,0,0,0,0]
                    # step 1: add a new node at the center
                    new_nodes[0] = n_n + 1
                    n_n += 1

                    # update node coordinate
                    # todo
                    new_node_coord = [(nodes[ele_nodes[0] - 1][0] + nodes[ele_nodes[1] - 1][0] + nodes[ele_nodes[2] - 1][0] + nodes[ele_nodes[3] - 1][0]) / 4.0,
                                      (nodes[ele_nodes[0] - 1][1] + nodes[ele_nodes[1] - 1][1] + nodes[ele_nodes[2] - 1][1] + nodes[ele_nodes[3] - 1][1]) / 4.0,
                                      (nodes[ele_nodes[0] - 1][2] + nodes[ele_nodes[1] - 1][2] + nodes[ele_nodes[2] - 1][2] + nodes[ele_nodes[3] - 1][2]) / 4.0]

                    nodes.append(new_node_coord)

                    for i_n in range(ele_info[1]):
                        if pair(ele_nodes[i_n - 1], ele_nodes[i_n]) in edge_to_center_node:
                            #the node is exists
                            new_nodes[i_n + 1] = edge_to_center_node[pair(ele_nodes[i_n - 1], ele_nodes[i_n])]
                        else:
                            new_nodes[i_n + 1] = n_n + 1
                            # update map
                            edge_to_center_node[pair(ele_nodes[i_n - 1], ele_nodes[i_n])] = n_n + 1
                            # update node coordinate
                            #todo
                            new_node_coord = [(nodes[ele_nodes[i_n - 1] - 1][0] + nodes[ele_nodes[i_n] - 1][0]) / 2.0,
                                              (nodes[ele_nodes[i_n - 1] - 1][1] + nodes[ele_nodes[i_n] - 1][1]) / 2.0,
                                              (nodes[ele_nodes[i_n - 1] - 1][2] + nodes[ele_nodes[i_n] - 1][2]) / 2.0]

                            nodes.append(new_node_coord)

                            n_n += 1

                    new_ele.append(Elem(id, [ele_nodes[0], new_nodes[2], new_nodes[0], new_nodes[1]], att, eframe))
                    new_ele.append(Elem(id, [ele_nodes[1], new_nodes[3], new_nodes[0], new_nodes[2]], att, eframe))
                    new_ele.append(Elem(id, [ele_nodes[2], new_nodes[4], new_nodes[0], new_nodes[3]], att, eframe))
                    new_ele.append(Elem(id, [ele_nodes[3], new_nodes[1], new_nodes[0], new_nodes[4]], att, eframe))



            elif ele_info[1] == 3:
                print('tri')
                n_e = len(ele)
                for i_e in range(n_e):
                    id = ele[i_e].id
                    att = ele[i_e].att
                    eframe = ele[i_e].eframe
                    ele_nodes = ele[i_e].nodes
                    new_nodes = [0, 0, 0]

                    for i_n in range(ele_info[1]):
                        if pair(ele_nodes[i_n - 1], ele_nodes[i_n]) in edge_to_center_node:
                            # the node is exists
                            new_nodes[i_n] = edge_to_center_node[pair(ele_nodes[i_n - 1], ele_nodes[i_n])]
                        else:
                            new_nodes[i_n] = n_n + 1
                            # update map
                            edge_to_center_node[pair(ele_nodes[i_n - 1], ele_nodes[i_n])] = n_n + 1
                            # update node coordinate
                            # todo
                            new_node_coord = [(nodes[ele_nodes[i_n - 1] - 1][0] + nodes[ele_nodes[i_n] - 1][0]) / 2.0,
                                              (nodes[ele_nodes[i_n - 1] - 1][1] + nodes[ele_nodes[i_n] - 1][1]) / 2.0,
                                              (nodes[ele_nodes[i_n - 1] - 1][2] + nodes[ele_nodes[i_n] - 1][2]) / 2.0]

                            nodes.append(new_node_coord)

                            n_n += 1

                    new_ele.append(Elem(id, [new_nodes[0], ele_nodes[0], new_nodes[1]], att, eframe))
                    new_ele.append(Elem(id, [new_nodes[1], ele_nodes[1], new_nodes[2]], att, eframe))
                    new_ele.append(Elem(id, [new_nodes[2], ele_nodes[2], new_nodes[0]], att, eframe))
                    new_ele.append(Elem(id, [new_nodes[0], new_nodes[1], new_nodes[2]], att, eframe))


            new_ele_set.append(new_ele)

        ################Update beams on the canopy
        for i_es in range(n_es):
            ele = ele_set[i_es]
            ele_info = ele_set_info[i_es]
            new_ele = new_ele_set[i_es]
            if ele_info[1] == 2:
                # beam
                n_e = len(ele)
                for i_e in range(n_e):
                    id = ele[i_e].id
                    att = ele[i_e].att
                    eframe = ele[i_e].eframe
                    ele_nodes = ele[i_e].nodes

                    if pair(ele_nodes[0], ele_nodes[1]) in edge_to_center_node:
                        # the node is exists
                        new_nodes = edge_to_center_node[pair(ele_nodes[0], ele_nodes[1])]
                        # update element
                        # todo attributes and eframe
                        new_ele.append(Elem(id, [ele_nodes[0], new_nodes], att, eframe))
                        new_ele.append(Elem(id, [new_nodes, ele_nodes[1]], att, eframe))


        ################Update beams not on the canopy

        for i_es in range(n_es):
            ele = ele_set[i_es]
            ele_info = ele_set_info[i_es]
            new_ele = new_ele_set[i_es]
            if ele_info[1] == 2:
                # beam
                n_e = len(ele)
                for i_e in range(n_e):
                    id = ele[i_e].id
                    att = ele[i_e].att
                    eframe = ele[i_e].eframe
                    ele_nodes = ele[i_e].nodes

                    if pair(ele_nodes[0], ele_nodes[1]) in edge_to_center_node:
                        # the node is exists
                        continue
                    else:
                        if refine_all_beams_or_not:
                            new_nodes = n_n + 1
                            # update map
                            edge_to_center_node[pair(ele_nodes[0], ele_nodes[1])] = n_n + 1
                            # update node coordinate
                            # todo
                            new_node_coord = [(nodes[ele_nodes[0] - 1][0] + nodes[ele_nodes[1] - 1][0])/2.0,
                                              (nodes[ele_nodes[0] - 1][1] + nodes[ele_nodes[1] - 1][1])/2.0,
                                              (nodes[ele_nodes[0] - 1][2] + nodes[ele_nodes[1] - 1][2])/2.0]
                            nodes.append(new_node_coord)
                            n_n += 1

                            new_ele.append(Elem(id, [ele_nodes[0], new_nodes], att, eframe))
                            new_ele.append(Elem(id, [new_nodes, ele_nodes[1]], att, eframe))
                        else :# do not refine these beams
                            new_ele.append(Elem(id, [ele_nodes[0], ele_nodes[1]], att, eframe))


        self.ele_set = new_ele_set

    def write_stru(self, stru_file_name, surf_file_name, write_idisp = False,thickness = 2.e-3):
        print('Writing mesh ...')
        stru_file = open(stru_file_name, 'w')
        surf_file = open(surf_file_name, 'w')
        stru_file.write('NODES\n')

        # Step1.1 write nodes
        nodes = self.nodes

        n_n = len(nodes)
        for i in range(n_n):
            stru_file.write('%d  %.16E  %.16E  %.16E\n' % (
            i + 1, nodes[i][0], nodes[i][1], nodes[i][2]))

        # Step1.2 write TOPOLOGY
        ele_set = self.ele_set
        ele_set_info = self.ele_set_info
        n_es = len(ele_set)
        stru_ele_start_id = 1
        surf_ele_start_id = 1
        for i in range(n_es):
            ele_new = ele_set[i]
            ele_info = ele_set_info[i]
            stru_file.write('*  %s\n' % ele_info[0])
            stru_file.write('TOPOLOGY\n')
            n_e = len(ele_new)
            type = fem_type = ele_info[1]
            if type == 2:
                fem_type = 6
            elif type == 3:
                fem_type = 15 #todo membrane 129, shell 15
            elif type == 4:
                fem_type = 16
                
            for j in range(n_e):
                assert(ele_new[j].att == ele_new[0].att)
                if (type == 2):
                    stru_file.write('%d  %d  %d  %d\n' % (stru_ele_start_id + j, fem_type, ele_new[j].nodes[0], ele_new[j].nodes[1]))
                if (type == 3):
                    stru_file.write(
                        '%d  %d  %d  %d  %d\n' % (stru_ele_start_id + j, fem_type, ele_new[j].nodes[0], ele_new[j].nodes[1], ele_new[j].nodes[2]))
                if (type == 4):
                    stru_file.write(
                        '%d  %d  %d  %d  %d  %d\n' % (stru_ele_start_id + j, fem_type, ele_new[j].nodes[0], ele_new[j].nodes[1], ele_new[j].nodes[2], ele_new[j].nodes[3]))
            stru_file.write('ATTRIBUTES\n')
            for j in range(n_e):
                stru_file.write('%d  %d\n' % (stru_ele_start_id + j, ele_new[j].att))

            if(type == 2): #beam elements need EFRAMES
                stru_file.write('EFRAMES\n')
                for j in range(n_e):
                    stru_file.write('%d  %.16E  %.16E  %.16E  %.16E  %.16E  %.16E  %.16E  %.16E  %.16E\n' % (stru_ele_start_id + j,
                                                                                                             ele_new[j].eframe[0], ele_new[j].eframe[1], ele_new[j].eframe[2],
                                                                                                             ele_new[j].eframe[3], ele_new[j].eframe[4], ele_new[j].eframe[5],
                                                                                                             ele_new[j].eframe[6], ele_new[j].eframe[7], ele_new[j].eframe[8]))

            stru_ele_start_id += n_e
            ############Write Sufrace top
            if (type == 4):
                name = ele_info[0]
                surf_id = 1 if name == 'Disk_Gores' else 2
                surf_file.write('*\nSURFACETOPO %d SURFACE_THICKNESS %.16E\n' %(surf_id, thickness))

                for j in range(n_e):
                    surf_file.write(
                        '%d  %d  %d  %d  %d  %d\n' % (
                         j + surf_ele_start_id, 1, ele_new[j].nodes[0], ele_new[j].nodes[1], ele_new[j].nodes[2], ele_new[j].nodes[3]))
                surf_ele_start_id += n_e

            elif (type == 3):
                name = ele_info[0]
                surf_id = 1 if name == 'Disk_Gores' else 2
                surf_file.write('*\nSURFACETOPO %d SURFACE_THICKNESS %.16E\n' %(surf_id, thickness))

                for j in range(n_e):
                    surf_file.write(
                        '%d  %d  %d  %d  %d\n' % (
                         j + surf_ele_start_id, 3, ele_new[j].nodes[0], ele_new[j].nodes[1], ele_new[j].nodes[2]))
                surf_ele_start_id += n_e

        # Step1.3 write IDISP6
        if write_idisp:
            node_disp = self.node_disp
            stru_file.write('IDISP6\n')
            for i_n in range(n_n):
                #todo ignore the initial displacement
                stru_file.write('%d %.16E  %.16E  %.16E  %.16E  %.16E  %.16E\n' %(i_n + 1, node_disp[i_n][0], node_disp[i_n][1], node_disp[i_n][2], 0.0, 0.0, 0.0))



        stru_file.close()
        surf_file.write('*\n')
        surf_file.close()

    def write_stru_split_gores(self, stru_file_name, surf_file_name, write_idisp=False, thickness=2.e-3, with_gap = False):
        print('Writing mesh ...')
        stru_file = open(stru_file_name, 'w')
        surf_file = open(surf_file_name, 'w')
        stru_file.write('NODES\n')

        # Step1.1 write nodes
        nodes = self.nodes

        n_n = len(nodes)
        for i in range(n_n):
            stru_file.write('%d  %.16E  %.16E  %.16E\n' % (
                i + 1, nodes[i][0], nodes[i][1], nodes[i][2]))
        # node_usage = np.zeros(n_n)
        # Step1.2 write TOPOLOGY
        ele_set = self.ele_set
        ele_set_info = self.ele_set_info
        n_es = len(ele_set)
        stru_ele_start_id = 1
        surf_ele_start_id = 1
        for i in range(n_es):
            ele_new = ele_set[i]
            ele_info = ele_set_info[i]
            stru_file.write('*  %s\n' % ele_info[0])
            stru_file.write('TOPOLOGY\n')
            n_e = len(ele_new)
            type = fem_type = ele_info[1]
            if type == 2:
                fem_type = 6
            elif type == 3:
                fem_type = 15  # todo membrane 129, shell 15
            elif type == 4:
                fem_type = 16

            for j in range(n_e):
                assert (ele_new[j].att == ele_new[0].att)
                if (type == 2):
                    stru_file.write('%d  %d  %d  %d\n' % (
                    stru_ele_start_id + j, fem_type, ele_new[j].nodes[0], ele_new[j].nodes[1]))


                if (type == 3):
                    stru_file.write(
                        '%d  %d  %d  %d  %d\n' % (
                        stru_ele_start_id + j, fem_type, ele_new[j].nodes[0], ele_new[j].nodes[1], ele_new[j].nodes[2]))

                if (type == 4):
                    stru_file.write(
                        '%d  %d  %d  %d  %d  %d\n' % (
                        stru_ele_start_id + j, fem_type, ele_new[j].nodes[0], ele_new[j].nodes[1], ele_new[j].nodes[2],
                        ele_new[j].nodes[3]))


            stru_file.write('ATTRIBUTES\n')
            for j in range(n_e):
                stru_file.write('%d  %d\n' % (stru_ele_start_id + j, ele_new[j].att))

            if (type == 2):  # beam elements need EFRAMES
                stru_file.write('EFRAMES\n')
                for j in range(n_e):
                    stru_file.write(
                        '%d  %.16E  %.16E  %.16E  %.16E  %.16E  %.16E  %.16E  %.16E  %.16E\n' % (stru_ele_start_id + j,
                                                                                                 ele_new[j].eframe[0],
                                                                                                 ele_new[j].eframe[1],
                                                                                                 ele_new[j].eframe[2],
                                                                                                 ele_new[j].eframe[3],
                                                                                                 ele_new[j].eframe[4],
                                                                                                 ele_new[j].eframe[5],
                                                                                                 ele_new[j].eframe[6],
                                                                                                 ele_new[j].eframe[7],
                                                                                                 ele_new[j].eframe[8]))

            stru_ele_start_id += n_e
            ############Write Sufrace top
            if (type == 4):
                name = ele_info[0]
                surf_id = 1 if name == 'Disk_Gores' else 2

                GORENUM = 80
                goreTheta = 2 * np.pi / GORENUM
                gores = [[] for x in range(GORENUM)]
                for j in range(n_e):
                    n1, n2, n3, n4 = ele_new[j].nodes[0], ele_new[j].nodes[1], ele_new[j].nodes[2], ele_new[j].nodes[3]
                    x1, y1 = nodes[n1 - 1][0], nodes[n1 - 1][1]
                    x2, y2 = nodes[n2 - 1][0], nodes[n2 - 1][1]
                    x3, y3 = nodes[n3 - 1][0], nodes[n3 - 1][1]
                    x4, y4 = nodes[n4 - 1][0], nodes[n4 - 1][1]
                    l1, l2, l3, l4 = np.sqrt(x1**2 + y1**2), np.sqrt(x2**2 + y2**2), np.sqrt(x3**2 + y3**2), np.sqrt(x4**2 + y4**2)




                    xc, yc = (x1 + x2 + x3 + x4) / 4.0, (y1 + y2 + y3 + y4) / 4.0
                    theta = np.arctan2(yc, xc)
                    if theta < 0:
                        theta = 2 * np.pi + theta
                    goreId = int(theta / goreTheta)
                    eps = 1.e-4

                    if (with_gap and goreId % 2 == 0 and ((abs(y1/l1 - np.sin(goreId*goreTheta)) < eps and abs(x1/l1 - np.cos(goreId*goreTheta)) < eps)
                                          or (abs(y2/l2 - np.sin(goreId*goreTheta)) < eps and abs(x2/l2 - np.cos(goreId*goreTheta)) < eps)
                                          or (abs(y3/l3 - np.sin(goreId*goreTheta)) < eps and abs(x3/l3 - np.cos(goreId*goreTheta)) < eps)
                                          or (abs(y4/l4 - np.sin(goreId*goreTheta)) < eps and abs(x4/l4 - np.cos(goreId*goreTheta)) < eps))):
                        continue


                    gores[goreId].append([n1, n2, n3, n4])

                surf_ele_id = 0
                for goreId in range(GORENUM):  # 80 Gores for each fabric
                    #surf_file.write('SURFACETOPO %d SURFACE_THICKNESS %.16E\n' % ((surf_id - 1) * GORENUM + goreId + 1, thickness))
                    surf_file.write(
                        '*\nSURFACETOPO %d\n' % ((surf_id - 1) * GORENUM + goreId + 1))
                    for n1, n2, n3, n4 in gores[goreId]:
                        surf_file.write('%d  %d  %d  %d  %d  %d\n' % (surf_ele_id + surf_ele_start_id, 1, n1, n2, n3, n4))
                        surf_ele_id += 1

                surf_ele_start_id += n_e

            elif (type == 3):
                name = ele_info[0]
                surf_id = 1 if name == 'Disk_Gores' else 2
                GORENUM = 80
                goreTheta = 2 * np.pi / GORENUM
                gores = [[] for x in range(GORENUM)]
                for j in range(n_e):
                    n1, n2, n3 = ele_new[j].nodes[0], ele_new[j].nodes[1], ele_new[j].nodes[2]
                    x1, y1 = nodes[n1 - 1][0], nodes[n1 - 1][1]
                    x2, y2 = nodes[n2 - 1][0], nodes[n2 - 1][1]
                    x3, y3 = nodes[n3 - 1][0], nodes[n3 - 1][1]
                    l1, l2, l3 = np.sqrt(x1 ** 2 + y1 ** 2), np.sqrt(x2 ** 2 + y2 ** 2), np.sqrt(
                        x3 ** 2 + y3 ** 2)

                    xc, yc = (x1 + x2 + x3) / 3.0, (y1 + y2 + y3) / 3.0
                    theta = np.arctan2(yc, xc)
                    if theta < 0:
                        theta = 2 * np.pi + theta
                    goreId = int(theta / goreTheta)
                    eps = 1.e-4

                    if (with_gap and goreId % 2 == 0 and ((abs(y1 / l1 - np.sin(goreId * goreTheta)) < eps and abs(
                                    x1 / l1 - np.cos(goreId * goreTheta)) < eps)
                                             or (abs(y2 / l2 - np.sin(goreId * goreTheta)) < eps and abs(
                                    x2 / l2 - np.cos(goreId * goreTheta)) < eps)
                                             or (abs(y3 / l3 - np.sin(goreId * goreTheta)) < eps and abs(
                                    x3 / l3 - np.cos(goreId * goreTheta)) < eps))):
                        continue

                    gores[goreId].append([n1, n2, n3])

                surf_ele_id = 0
                for goreId in range(GORENUM):  # 80 Gores for each fabric
                    # surf_file.write(
                    #     'SURFACETOPO %d SURFACE_THICKNESS %.16E\n' % ((surf_id - 1) * GORENUM + goreId + 1, thickness))
                    surf_file.write('*\nSURFACETOPO %d\n' % ((surf_id - 1) * GORENUM + goreId + 1))
                    for n1, n2, n3 in gores[goreId]:
                        surf_file.write(
                            '%d  %d  %d  %d  %d\n' % (surf_ele_id + surf_ele_start_id, 3, n1, n2, n3))
                        surf_ele_id += 1

                surf_ele_start_id += n_e


        if write_idisp:
            node_disp = self.node_disp
            node_rotation = self.compute_rotation()
            stru_file.write('IDISP6\n')
            for i_n in range(n_n):
                # todo ignore the initial displacement
                stru_file.write('%d %.16E  %.16E  %.16E  %.16E  %.16E  %.16E\n' % (
                i_n + 1, node_disp[i_n][0], node_disp[i_n][1], node_disp[i_n][2], node_rotation[i_n][0], node_rotation[i_n][1], node_rotation[i_n][2]))

        stru_file.close()
        surf_file.write('*\n')
        surf_file.close()

    def compute_rotation(self):
        nodes, ele_set, ele_set_info = self.nodes, self.ele_set, self.ele_set_info
        nodes_disp = self.node_disp
        band_rot_matrices = self.band_rot_matrices
        disk_rot_matrices = self.disk_rot_matrices
        n_n = len(nodes)
        n_es = len(ele_set)
        nodes_rotation_2d = np.zeros((n_n, 3))
        nodes_rotation_3d = np.zeros((n_n, 3))
        nodes_rotation = np.zeros((n_n, 3))
        weights = np.zeros((n_n, 2), dtype=int)

        print(len(nodes), nodes_disp.shape, len(ele_set))
        GORENUM = 80 #todo
        goreTheta = 2 * np.pi / GORENUM

        for i in range(len(ele_set)):
            eles = ele_set[i]
            id = len(eles[0].nodes)
            print(ele_set_info[i][0])

            # if(ele_set_info[i][0] == 'Band_Bottom_Edges' or ele_set_info[i][0] == 'Band_Top_Edges'
            #       or ele_set_info[i][0] == 'Disk_Inner_Edges' or ele_set_info[i][0] == 'Disk_Outer_Edges'):
            #     print('skip ', ele_set_info[i][0])
            #     continue

            if id == 2:
                # beam element
                for e in eles:
                    n1, n2 = e.nodes

                    xx1, xx2 = np.array(nodes[n1 - 1]), np.array(nodes[n2 - 1])
                    yy1, yy2 = np.array(nodes[n1 - 1]) + nodes_disp[n1 - 1], np.array(nodes[n2 - 1]) + nodes_disp[n2 - 1]

                    a = xx2 - xx1
                    a = a / np.linalg.norm(a)

                    b = yy2 - yy1
                    b = b / np.linalg.norm(b)


                    v1, v2, v3 = np.cross(a, b)
                    s = np.sqrt(v1**2 + v2**2 + v3**2)
                    c = np.dot(a, b)
                    if s < 1.e-10:
                        theta_x, theta_y, theta_z = 0., 0., 0.
                    else:
                        vx = np.array([[0.,-v3,v2],[v3,0,-v1],[-v2,v1,0.]])

                        R = np.array([[1.,0.,0.],[0.,1.,0.],[0.,0.,1.]]) + vx + np.dot(vx,vx)* (1-c)/s**2

                        theta_x, theta_y, theta_z = matrix_to_angles(R)


                    nodes_rotation_2d[n1 - 1, :] += np.array([theta_x, theta_y, theta_z])
                    nodes_rotation_2d[n2 - 1, :] += np.array([theta_x, theta_y, theta_z])
                    weights[n1 - 1, 1] += 1
                    weights[n2 - 1, 1] += 1





            else:
                # shell element
                for e in eles:
                    n1, n2, n3 = e.nodes

                    x1, y1, z1 = nodes[n1 - 1][0], nodes[n1 - 1][1], nodes[n1 - 1][2]
                    x2, y2, z2 = nodes[n2 - 1][0], nodes[n2 - 1][1], nodes[n2 - 1][2]
                    x3, y3, z3 = nodes[n3 - 1][0], nodes[n3 - 1][1], nodes[n3 - 1][2]

                    xc, yc = (x1 + x2 + x3) / 3.0, (y1 + y2 + y3) / 3.0
                    theta = np.arctan2(yc, xc)
                    if theta < 0:
                        theta = 2 * np.pi + theta



                    goreId = int(theta / goreTheta)

                    R = disk_rot_matrices[goreId] if ele_set_info[i][0] == 'Disk_Gores' else band_rot_matrices[goreId]

                    theta_x, theta_y, theta_z = matrix_to_angles(R)


                    nodes_rotation_3d[n1 - 1, :] += np.array([theta_x, theta_y, theta_z])
                    nodes_rotation_3d[n2 - 1, :] += np.array([theta_x, theta_y, theta_z])
                    nodes_rotation_3d[n3 - 1, :] += np.array([theta_x, theta_y, theta_z])

                    weights[n1 - 1, 0] += 1
                    weights[n2 - 1, 0] += 1
                    weights[n2 - 1, 0] += 1

                    # xx0, xx1, xx2 = np.array(nodes[n1 - 1]), np.array(nodes[n2 - 1]), np.array(nodes[n3 - 1])
                    # aa0, aa1, aa2 = xx0 - xx0, xx1 - xx0, xx2 - xx0
                    #
                    #
                    # yy0, yy1, yy2 = nodes[n1 - 1] + nodes_disp[n1 - 1], nodes[n2 - 1] + nodes_disp[n2 - 1], nodes[n3 - 1] + \
                    #              nodes_disp[n3 - 1]
                    # bb0, bb1, bb2 = yy0 - yy0, yy1 - yy0, yy2 - yy0
                    #
                    #
                    #
                    # e1, e2 = np.dot(R, aa1) - bb1, np.dot(R, aa2) - bb2
                    #
                    # if (np.linalg.norm(e1) > 1.e-10 or np.linalg.norm(e2) > 1.e-10):
                    #     print( n1, n2 , n3, ele_set_info[i][0])
                    #     # print(a1, a2, b1, b2)
                    #     # print(np.linalg.norm(a1), np.linalg.norm(a2), np.linalg.norm(b1), np.linalg.norm(b2))
                    #     print(e1, e2)
                    #     #exit(1)

        # weight = weights[:, 0] + weights[:, 1]
        # nodes_rotation = nodes_rotation_3d + nodes_rotation_2d
        # I = weight > 0
        # nodes_rotation[I, :] = nodes_rotation[I, :] / weight[I, None]
        # I = weights[:, 0] > 0
        # nodes_rotation[I, :] = nodes_rotation_3d[I, :] / weights[I, 0][:,None]

        #shell element use rotation from shell
        I = weights[:, 0] > 0
        nodes_rotation[I, :] = nodes_rotation_3d[I, :] / weights[I, 0][:,None]

        #rewrite beam rotation, use rotaion from beam
        I = weights[:, 1] > 0
        nodes_rotation[I, :] = nodes_rotation_2d[I, :] / weights[I, 1][:, None]




        return nodes_rotation
    def reset_initial(self):
        '''
        update node coordinate to include the displacement
        :return:
        '''
        nodes = self.nodes
        node_disp = self.node_disp
        nn = len(nodes)
        for i_n in range(nn):
            nodes[i_n] = nodes[i_n][0] + node_disp[i_n][0], nodes[i_n][1] + node_disp[i_n][1], nodes[i_n][2] + node_disp[i_n][2]

        # reset eframe
        print('need to rotate the eframe')

    def folding(self, n):
        '''
        First fold the Disk, then the band, and the suspension lines
        n : number of
        :return: disp

        '''
        nodes = self.nodes
        ele_set = self.ele_set
        ele_set_info = self.ele_set_info
        node_disp = np.zeros([len(nodes),3])
        #parachute parameters
        r_d, R_d, h_d =  0.788, 7.7235, 39.2198 #Disk inner radius, outer radius and z
        R_b, ht_b, hb_b = 7.804, 38.3158, 35.7358 #Band radius, band top z and band bottom z
        h0 = 0
        L_s, L_v, L_g = np.sqrt(R_b**2 + hb_b**2), r_d, np.sqrt((R_d - R_b)**2 + (h_d - ht_b)**2) # Suspension_Lines length ,  Vent_Lines length,    Gap_Lines length

        rotaion_matrix = [[],[]] # for the disk and the band

        # todo the second parameter is the z displacement of disk
        disk_b3 = 7.5

        band_deform_method = 'rigid'

        line_relax_method = 'catenary'

        ############ piece map
        theta = np.pi / n

        ################################################ This is for the disk
        # todo the first parameter is cosa in [0, 1], the smaller cosa the more folded
        # cosa = 0.4 # 0.3, 0.2
        # sina = -np.sqrt(1 - cosa * cosa)
        # cosb = (sina * cosa * np.tan(theta) - sina / np.cos(theta)) / (1 + sina * sina * np.tan(theta) * np.tan(theta))
        # sinb = -cosa + cosb * sina * np.tan(theta)
        # print('cosb^2 + sinb^2 = ', cosb * cosb + sinb * sinb)
        #
        # disk_rot0 = np.array([[cosa, -cosb * sina, -sinb * sina],
        #                  [0, cosa - cosb * sina * np.tan(theta), cosb],
        #                  [sina, cosb * cosa, sinb * cosa]])

        cosa = 0.4 # 0.3, 0.2
        sina = np.sqrt(1 - cosa * cosa)
        sinb = (-sina*cosa*np.tan(theta) + sina*np.sqrt(cosa**2*np.tan(theta)**2 + 1 + sina**2*np.tan(theta)**2))/ (1 + sina * sina * np.tan(theta) * np.tan(theta))
        cosb = cosa + sinb * sina * np.tan(theta)
        print('cosb^2 + sinb^2 = ', cosb * cosb + sinb * sinb)

        disk_rot0 = np.array([[cosa,        sinb * sina,                             sina *cosb],
                              [0,               cosb  ,                                             -sinb  ],
                              [-sina,             sinb * cosa,                     cosb * cosa]])

        disk_disp = np.array([0, 0, disk_b3])
        print('orthogonal matrix test ', np.dot(disk_rot0.T, disk_rot0), np.linalg.det(disk_rot0))


        # The rigid motion of the first half gore is rot0*x + disp0
        disk_x1 = np.array([r_d, 0, 0])
        disk_x2 = np.array([R_d, 0, 0])
        disk_x3 = np.array([r_d*np.cos(theta), r_d*np.sin(theta), 0])
        disk_x4 = np.array([R_d*np.cos(theta), R_d*np.sin(theta), 0])

        disk_y1 = np.dot(disk_rot0, disk_x1) + disk_disp + np.array([0.,0., h_d])
        disk_y2 = np.dot(disk_rot0, disk_x2) + disk_disp + np.array([0.,0., h_d])
        disk_y3 = np.dot(disk_rot0, disk_x3) + disk_disp + np.array([0.,0., h_d])
        disk_y4 = np.dot(disk_rot0, disk_x4) + disk_disp + np.array([0.,0., h_d])

        #R < r
        R_d_top_deform = np.sqrt(disk_y1[0] ** 2 + disk_y1[1] ** 2)
        r_d_top_deform = np.sqrt(disk_y3[0] ** 2 + disk_y3[1] ** 2)

        R_d_bottom_deform = np.sqrt(disk_y2[0]**2 + disk_y2[1]**2)
        r_d_bottom_deform = np.sqrt(disk_y4[0]**2 + disk_y4[1]**2)
        disk_rot_matrices = []

        ######################
        for gore_id in range(n):
            #Handle the piece of theta = [2pi/n * gore_id, 2pi/n * (gore_id+1)]
            #The piece will be fold at the center

            ##
            # The the map is
            # rotn = R_z(theta*n) * rot0 * R_z(theta*n)^{-1}
            # bi = b0
            ##
            R_z = np.array([[np.cos(2*gore_id*theta), -np.sin(2*gore_id*theta), 0.],
                            [np.sin(2*gore_id*theta), np.cos(2*gore_id*theta), 0.],
                            [0.,0.,1.]])
            disk_rotn = np.dot(R_z, np.dot(disk_rot0, R_z.T))

            Ref_z = np.array([[np.cos((4*gore_id+2)*theta), np.sin((4*gore_id+2)*theta), 0.],
                              [np.sin((4*gore_id+2)*theta), -np.cos((4*gore_id+2)*theta), 0.],
                              [0., 0., 1.]])
            disk_rotn_2 = np.dot(Ref_z, np.dot(disk_rotn, Ref_z.T))
            disk_rot_matrices.append(disk_rotn)
            disk_rot_matrices.append(disk_rotn_2)

        ################################################ This is for the band, there are two maps,
        # 1) flat
        # 2) rigid


        r_b_deform, l_b_deform, R_b_deform = 0.0, 0.0, 0.0
        if band_deform_method == 'rigid':
            l_b_deform = 2*R_b*np.sin(theta/2.)
        elif band_deform_method == 'flat':
            l_b_deform = theta * R_b

        # todo parameters about the band r_b_deform
        # R < r
        # if you need to enforce R_b_deform = R_d_deform,
        # r_b_deform = (R_d_bottom_deform*np.cos(theta) + np.sqrt(l_b_deform**2 - R_d_bottom_deform**2*np.sin(theta)**2))

        r_b_deform = (
        R_d_bottom_deform * np.cos(theta) + np.sqrt(l_b_deform ** 2 - R_d_bottom_deform ** 2 * np.sin(theta) ** 2))

        R_b_deform = r_b_deform * np.cos(theta) - np.sqrt(l_b_deform * l_b_deform - r_b_deform * r_b_deform * np.sin(theta) * np.sin(theta))

        # todo parameters about the band are z displacement of band
        # make sure no line is stretched
        band_b3 = max(disk_y4[2] - ht_b - np.sqrt(L_g**2  - (disk_y4[0] - r_b_deform*np.cos(theta))**2 - (disk_y4[1] - r_b_deform*np.sin(theta))**2),
                     disk_y2[2] - ht_b - np.sqrt(L_g**2  - (disk_y2[0] - R_b_deform)**2 - disk_y2[1]**2))

        # band_b3 = 0.5*(disk_y4[2] - ht_b - np.sqrt(
        #     L_g ** 2 - (disk_y4[0] - r_b_deform * np.cos(theta)) ** 2 - (disk_y4[1] - r_b_deform * np.sin(theta)) ** 2)+
        #               disk_y2[2] - ht_b - np.sqrt(L_g ** 2 - (disk_y2[0] - R_b_deform) ** 2 - disk_y2[1] ** 2))

        if band_deform_method == 'rigid':
            l_b_deform = 2*R_b*np.sin(theta/2.)
            R_b_deform = r_b_deform * np.cos(theta) - np.sqrt(l_b_deform*l_b_deform - r_b_deform*r_b_deform*np.sin(theta)*np.sin(theta))
            # todo check can also be - np.sqrt
            cosa = (r_b_deform*np.sin(theta)*np.sin(theta) - np.sqrt(r_b_deform**2 * np.sin(theta)**4 - 2.*(1 - np.cos(theta))*(r_b_deform**2 * np.sin(theta)**2 - R_b**2*(1 - np.cos(theta))**2)))\
                   /(2*R_b*(1. - np.cos(theta)))
            sina = -np.sqrt(1 - cosa * cosa)
            print('cosa and sin a : ', cosa, ' ', sina)
            band_rot0 = np.array([[cosa, -sina, 0],
                                  [sina,  cosa, 0],
                                  [   0,     0, 1]])
            band_disp0 = np.array([R_b_deform, 0, 0]) - np.dot(band_rot0, np.array([R_b, 0, 0]))

            band_disp0[2] += band_b3

            ##todo start debug validation
            band_disp0_ = np.array([r_b_deform*np.cos(theta), r_b_deform*np.sin(theta), 0]) - np.dot(band_rot0, np.array([R_b*np.cos(theta), R_b*np.sin(theta), 0]))
            band_disp0_[2] += band_b3
            assert(np.linalg.norm(band_disp0 - band_disp0_) < 1e-10)
            ##todo end debug validation


            band_rot_matrices = []
            band_disp_vectors = []

            ######################
            for gore_id in range(n):
                # Handle the piece of theta = [2pi/n * gore_id, 2pi/n * (gore_id+1)]
                # The piece will be fold at the center

                ##
                # The the map is
                # rotn = R_z(theta*n) * rot0 * R_z(theta*n)^{-1}
                # bi = b0
                ##
                R_z = np.array([[np.cos(2 * gore_id * theta), -np.sin(2 * gore_id * theta), 0.],
                                [np.sin(2 * gore_id * theta), np.cos(2 * gore_id * theta), 0.],
                                [0., 0., 1.]])
                band_rotn = np.dot(R_z, np.dot(band_rot0, R_z.T))
                band_dispn = np.dot(R_z, band_disp0)

                Ref_z = np.array([[np.cos((4 * gore_id + 2) * theta), np.sin((4 * gore_id + 2) * theta), 0.],
                                  [np.sin((4 * gore_id + 2) * theta), -np.cos((4 * gore_id + 2) * theta), 0.],
                                  [0., 0., 1.]])
                band_rotn_2 = np.dot(Ref_z, np.dot(band_rotn, Ref_z.T))
                band_dispn_2 = np.dot(Ref_z, band_dispn)
                band_rot_matrices.append(band_rotn)
                band_rot_matrices.append(band_rotn_2)
                band_disp_vectors.append(band_dispn)
                band_disp_vectors.append(band_dispn_2)


        n_n = len(nodes)  # save number of nodes
        n_es = len(ele_set)



        self.band_rot_matrices = band_rot_matrices
        self.disk_rot_matrices = disk_rot_matrices



        ################   Update canopy
        for i_es in range(n_es):
            ele = ele_set[i_es]
            ele_info = ele_set_info[i_es]
            if (ele_info[1] == 4 or ele_info[1] == 3) and ele_info[0] == 'Disk_Gores':
                n_e = len(ele)
                for i_e in range(n_e):
                    ele_nodes = ele[i_e].nodes
                    for i_n in ele_nodes:
                        xx = nodes[i_n - 1]
                        angle_x = np.arctan2(xx[1], xx[0])   #[-pi, 2pi]
                        gore_id = int((angle_x + 2 * np.pi)/theta)%(2*n)
                        # For the piece  [pi/n * gore_id, pi/n * (gore_id + 1)]
                        # map the point xx -> rot_A * (xx - c) + c + disp_b, here c = [0, 0, xx[2]]


                        disk_rot = disk_rot_matrices[gore_id]
                        xx_shift, disp_shift = np.array([xx[0], xx[1], 0.0]), np.array([0, 0, xx[2]])
                        new_xx = np.dot(disk_rot, xx_shift) + disk_disp + disp_shift

                        node_disp[i_n - 1,:] =  new_xx[0] - xx[0], new_xx[1] - xx[1], new_xx[2] - xx[2]

            if (ele_info[1] == 4 or ele_info[1] == 3) and ele_info[0] == 'Band_Gores':
                n_e = len(ele)
                if band_deform_method == 'rigid':
                    for i_e in range(n_e):
                        ele_nodes = ele[i_e].nodes
                        for i_n in ele_nodes:
                            xx = nodes[i_n - 1]
                            angle_x = np.arctan2(xx[1], xx[0])  # [-pi, pi]
                            gore_id = int((angle_x + 2 * np.pi) / theta) % (2 * n)
                            # For the piece  [pi/n * gore_id, pi/n * (gore_id + 1)]
                            # map the point xx -> rot_A * xx  + disp

                            band_rot = band_rot_matrices[gore_id]
                            band_disp = band_disp_vectors[gore_id]
                            new_xx = np.dot(band_rot, xx) + band_disp

                            node_disp[i_n - 1, :] = new_xx[0] - xx[0], new_xx[1] - xx[1], new_xx[2] - xx[2]
                elif band_deform_method == 'flat':

                    l_b_deform = theta * R_b
                    R_b_deform = r_b_deform * np.cos(theta) - np.sqrt(
                        l_b_deform * l_b_deform - r_b_deform * r_b_deform * np.sin(theta) * np.sin(theta))

                    for i_e in range(n_e):
                        ele_nodes = ele[i_e].nodes
                        for i_n in ele_nodes:
                            xx = nodes[i_n - 1]
                            angle_x = np.arctan2(xx[1], xx[0])   # [-pi, pi]
                            gore_id = int((angle_x + 2 * np.pi)/ theta) % (2 * n)
                            # For the piece  [pi/n * gore_id, pi/n * (gore_id + 1)]
                            # map the point xx -> rot_A * xx  + disp

                            d_theta = angle_x - gore_id*theta if angle_x >= 0 else angle_x + 2*np.pi - gore_id*theta
                            assert(d_theta <=  theta and d_theta >= 0)
                            ds = d_theta * R_b

                            start_deform = np.empty(3)
                            end_deform = np.empty(3)
                            if gore_id % 2 == 0:
                                start_deform[:] = R_b_deform*np.cos(gore_id*theta), R_b_deform*np.sin(gore_id*theta), 0
                                end_deform[:]   = r_b_deform*np.cos((gore_id+1)*theta), r_b_deform*np.sin((gore_id+1)*theta), 0
                            else: #gore_id%2 == 1
                                start_deform[:] = r_b_deform * np.cos(gore_id*theta), r_b_deform * np.sin(gore_id*theta), 0
                                end_deform[:] = R_b_deform * np.cos((gore_id+1)*theta), R_b_deform * np.sin((gore_id+1)*theta), 0


                            new_xx = (1 - ds/l_b_deform)*start_deform + ds/l_b_deform*end_deform
                            new_xx[2] = xx[2] + band_b3

                            node_disp[i_n - 1, :] = new_xx[0] - xx[0], new_xx[1] - xx[1], new_xx[2] - xx[2]

        # n_n = len(nodes)  # save number of nodes
        # n_es = len(ele_set)
        #
        # ################   Update canopy
        # for i_es in range(n_es):
        #     ele = ele_set[i_es]
        #     ele_info = ele_set_info[i_es]
        #     if (ele_info[1] == 4 or ele_info[1] == 3) and ele_info[0] == 'Disk_Gores':
        #         n_e = len(ele)
        #         for i_e in range(n_e):
        #             ele_nodes = ele[i_e].nodes
        #             for i_n in ele_nodes:
        #                 xx = nodes[i_n - 1]
        #                 angle_x = np.arctan2(xx[1], xx[0])  # [-pi, 2pi]
        #                 gore_id = int((angle_x + 2 * np.pi) / theta) % (2 * n)
        #                 # For the piece  [pi/n * gore_id, pi/n * (gore_id + 1)]
        #                 # map the point xx -> rot_A * (xx - c) + c + disp_b, here c = [0, 0, xx[2]]
        #
        #
        #                 disk_rot = disk_rot_matrices[gore_id]
        #                 xx_shift, disp_shift = np.array([xx[0], xx[1], 0.0]), np.array([0, 0, xx[2]])
        #                 new_xx = np.dot(disk_rot, xx_shift) + disk_disp + disp_shift
        #
        #                 node_disp[i_n - 1, :] = new_xx[0] - xx[0], new_xx[1] - xx[1], new_xx[2] - xx[2]
        #
        #     if (ele_info[1] == 4 or ele_info[1] == 3) and ele_info[0] == 'Band_Gores':
        #         n_e = len(ele)
        #         if band_deform_method == 'rigid':
        #             for i_e in range(n_e):
        #                 ele_nodes = ele[i_e].nodes
        #                 for i_n in ele_nodes:
        #                     xx = nodes[i_n - 1]
        #                     angle_x = np.arctan2(xx[1], xx[0])  # [-pi, pi]
        #                     gore_id = int((angle_x + 2 * np.pi) / theta) % (2 * n)
        #                     # For the piece  [pi/n * gore_id, pi/n * (gore_id + 1)]
        #                     # map the point xx -> rot_A * xx  + disp
        #
        #                     band_rot = band_rot_matrices[gore_id]
        #                     band_disp = band_disp_vectors[gore_id]
        #                     new_xx = np.dot(band_rot, xx) + band_disp
        #
        #                     node_disp[i_n - 1, :] = new_xx[0] - xx[0], new_xx[1] - xx[1], new_xx[2] - xx[2]
        #         elif band_deform_method == 'flat':
        #
        #             l_b_deform = theta * R_b
        #             R_b_deform = r_b_deform * np.cos(theta) - np.sqrt(
        #                 l_b_deform * l_b_deform - r_b_deform * r_b_deform * np.sin(theta) * np.sin(theta))
        #
        #             for i_e in range(n_e):
        #                 ele_nodes = ele[i_e].nodes
        #                 for i_n in ele_nodes:
        #                     xx = nodes[i_n - 1]
        #                     angle_x = np.arctan2(xx[1], xx[0])  # [-pi, pi]
        #                     gore_id = int((angle_x + 2 * np.pi) / theta) % (2 * n)
        #                     # For the piece  [pi/n * gore_id, pi/n * (gore_id + 1)]
        #                     # map the point xx -> rot_A * xx  + disp
        #
        #                     d_theta = angle_x - gore_id * theta if angle_x >= 0 else angle_x + 2 * np.pi - gore_id * theta
        #                     assert (d_theta <= theta and d_theta >= 0)
        #                     ds = d_theta * R_b
        #
        #                     start_deform = np.empty(3)
        #                     end_deform = np.empty(3)
        #                     if gore_id % 2 == 0:
        #                         start_deform[:] = R_b_deform * np.cos(gore_id * theta), R_b_deform * np.sin(
        #                             gore_id * theta), 0
        #                         end_deform[:] = r_b_deform * np.cos((gore_id + 1) * theta), r_b_deform * np.sin(
        #                             (gore_id + 1) * theta), 0
        #                     else:  # gore_id%2 == 1
        #                         start_deform[:] = r_b_deform * np.cos(gore_id * theta), r_b_deform * np.sin(
        #                             gore_id * theta), 0
        #                         end_deform[:] = R_b_deform * np.cos((gore_id + 1) * theta), R_b_deform * np.sin(
        #                             (gore_id + 1) * theta), 0
        #
        #                     new_xx = (1 - ds / l_b_deform) * start_deform + ds / l_b_deform * end_deform
        #                     new_xx[2] = xx[2] + band_b3
        #
        #                     node_disp[i_n - 1, :] = new_xx[0] - xx[0], new_xx[1] - xx[1], new_xx[2] - xx[2]

        ##############################################################################################################
        # Update vent_center point
        ##############################################################################################################

        vent_center_node_id = 48842 if self.fabric_elem_type == 4 else 55960

        xx = nodes[vent_center_node_id - 1]
        print(xx[0]**2 + xx[1]**2 + (xx[2] - h_d)**2,  " is smaller than ", 1.e-10)

        vent_b3    = min(np.sqrt(L_v**2 - disk_y1[0]**2 - disk_y1[1]**2) + disk_y1[2] - h_d,
                         np.sqrt(L_v**2 - disk_y3[0]**2 - disk_y3[1]**2) + disk_y3[2] - h_d) - 0.001
        node_disp[vent_center_node_id - 1, :] = 0., 0., vent_b3
        ##############################################################################################################
        # Update suspension lines
        ##############################################################################################################
        for i_es in range(n_es):
            ele = ele_set[i_es]
            ele_info = ele_set_info[i_es]
            if ele_info[1] == 2 and (ele_info[0] == 'Suspension_Lines' or ele_info[0] == 'Vent_Lines' or ele_info[0] == 'Gap_Lines'):
                l_ref = -1.0
                if  ele_info[0] == 'Suspension_Lines':
                    l_ref = L_s
                elif ele_info[0] == 'Vent_Lines':
                    l_ref = L_v
                elif ele_info[0] == 'Gap_Lines':
                    l_ref = L_g


                lines = SplitLines(ele)
                print(ele_info[0], ' the number of lines is ', len(lines))
                for i_line in range(len(lines)):
                    line = lines[i_line]
                    xx_start = np.array(nodes[line[0] - 1])
                    start_deform = np.array(nodes[line[0] - 1]) + node_disp[line[0] - 1,:]
                    end_deform   = np.array(nodes[line[-1] - 1]) + node_disp[line[-1] - 1,:]

                    cur_length = np.linalg.norm(end_deform - start_deform)
                    print('cur_length is ', cur_length, ' l_ref is ', l_ref)

                    if cur_length >= l_ref :
                        #print(ele_info[0], ' current lenght is ', cur_length, ' , which is greater than its undeformed length ', l_ref)

                        for i_n in range(len(line)):
                            xx = nodes[line[i_n] - 1]

                            new_xx = (1. - float(i_n) / float(len(line) - 1)) * start_deform + float(i_n) / float(len(line) - 1) * end_deform

                            node_disp[line[i_n] - 1, :] = new_xx[0] - xx[0], new_xx[1] - xx[1], new_xx[2] - xx[2]
                    else:
                        #print('current lenght is ', cur_length, ' , which is smaller than its undeformed length ', l_ref)

                        # use catenary curve fitting





                        if line_relax_method == 'parabolia':
                            print('have not implemented yet')

                            # a = fsolve(catenary, (cur_length/l_ref), np.sqrt(12 * (1. - cur_length/l_ref)))[0]
                            # line_R = l_ref / line_theta
                            # circle_O =
                            # for i_n in range(len(line)):
                            #     d_theta = float(i_n) / float(len(line)) * line_theta
                            #
                            #
                            #     new_xx = (1. - float(i_n) / float(len(line))) * start_deform + float(i_n) / float(
                            #         len(line)) * end_deform
                            #
                            #     node_disp[line[i_n] - 1, :] = new_xx[0] - xx[0], new_xx[1] - xx[1], new_xx[2] - xx[2]

                        elif line_relax_method == 'catenary':
                            # build 2d coordinate system, which is parallel to the z axis and
                            # contains the start_deform and end_deform, center at start deform

                            dir_r = np.array([end_deform[0] - start_deform[0], end_deform[1] - start_deform[1]])

                            if(np.linalg.norm(dir_r) > 1.e-10):
                                dir_r = dir_r/np.linalg.norm(dir_r)

                                start_deform_2d = np.array([0,0])
                                end_deform_2d = np.array(
                                    [(end_deform[0] - start_deform[0]) * dir_r[0] + (end_deform[1] - start_deform[1]) * dir_r[1], end_deform[2] - start_deform[2]])
                                if not np.linalg.norm(end_deform_2d) < l_ref:
                                    print(np.linalg.norm(end_deform_2d), ' ', l_ref)
                                print(np.linalg.norm(end_deform_2d), " smaller than ",  l_ref)

                                a, xm, ym = Line.catenary(start_deform_2d[0], start_deform_2d[1], end_deform_2d[0], end_deform_2d[1], l_ref)

                                for i_n in range(len(line)):
                                    xx = np.array(nodes[line[i_n] - 1])
                                    ds = np.linalg.norm(xx - xx_start)
                                    new_r, new_z = Line.point_on_catenary(start_deform_2d[0], start_deform_2d[1], end_deform_2d[0], end_deform_2d[1], a, xm, ym, l_ref, ds)

                                    new_xx = np.array([new_r*dir_r[0] + start_deform[0], new_r*dir_r[1] + start_deform[1], new_z + start_deform[2]])

                                    node_disp[line[i_n] - 1, :] = new_xx[0] - xx[0], new_xx[1] - xx[1], new_xx[2] - xx[2]

                            else:
                                # todo the line connecting these two points is parallel to z axis
                                print('the line is parallel to the z axis')

                                dir_r = np.array([start_deform[0], start_deform[1]])
                                dir_r = dir_r/np.linalg.norm(dir_r)
                                circle_theta, circle_r = Line.line_to_circle(l_ref, abs(end_deform[2] - start_deform[2]))
                                #choose the new coordinate center at (0,0,(start_deform[2] + end_deform[2])/2.0)
                                start_deform_2d = np.array([start_deform[0]*dir_r[0] + start_deform[1]*dir_r[1], (start_deform[2] - end_deform[2])/2.0])
                                end_deform_2d = np.array([end_deform[0]*dir_r[0] + end_deform[1]*dir_r[1], (end_deform[2] - start_deform[2])/2.0])

                                for i_n in range(len(line)):
                                    xx = np.array(nodes[line[i_n] - 1])
                                    ds = np.linalg.norm(xx - xx_start)
                                    new_r, new_z = Line.point_on_circle(start_deform_2d[0], start_deform_2d[1], end_deform_2d[0], end_deform_2d[1], circle_theta, circle_r, l_ref, ds)

                                    new_xx = np.array([new_r*dir_r[0], new_r*dir_r[1], new_z + (start_deform[2] + end_deform[2])/2.0])

                                    node_disp[line[i_n] - 1, :] = new_xx[0] - xx[0], new_xx[1] - xx[1], new_xx[2] - xx[2]




        self.node_disp = node_disp






if __name__ == '__main__':
    # element type can be 3 or 4
    # 3: triangular structure element 
    # 4: quad element structure mesh
    element_type = 3

    # contact surface topology thickness for 2 side contact
    # since we use one side contact, this is no longer used
    thickness = 2.0e-3

    # leave gap in the surface topology for 2 side contact
    # since we use one side contact, this is false
    with_gap = False
    if element_type == 3:
        mesh = Mesh(3)
        suffix = '.tria'
        mesh.read_stru('parachute_coarse' + suffix)

        # calling the function, you can refine the mesh by cuting each edge into 2
        mesh.refine()
        # mesh.refine()

        # Apply the accordion folding with 40 /\/\/\/\ .....
        # The most important parameters in this function (hard-coded)
        # the 1st parameter is cosa = 0.4 in [0, 1], the smaller cosa the more folded is the parachute 
        # the 2nd parameter is disk_b3 = 7.5, the z displacement of disk   
        mesh.folding(40)

        # This function put initial displacements as intial condition, this is no longer used
        #mesh.reset_initial()

        # Write down the new structure file
        mesh.write_stru_split_gores('mesh_Structural.top' + suffix, 'mesh_Structural.surfacetop' + suffix, True, thickness, with_gap)
    elif element_type == 4:
        mesh = Mesh(4)
        suffix = '.quad'
        mesh.read_stru('parachute_coarse' + suffix)

        # calling the function, you can refine the mesh by cuting each edge into 2 
        mesh.refine()
        # mesh.refine()

        # Apply the accordion folding with 40 /\/\/\/\ .....
        # The most important parameters in this function (hard-coded)
        # the 1st parameter is cosa = 0.4 in [0, 1], the smaller cosa the more folded is the parachute 
        # the 2nd parameter is disk_b3 = 7.5, the z displacement of disk   
        mesh.folding(40)

        #mesh.reset_initial()

        mesh.write_stru_split_gores('mesh_Structural.top' + suffix, 'mesh_Structural.surfacetop' + suffix, True)







