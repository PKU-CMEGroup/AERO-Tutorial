import numpy as np
import matplotlib.pyplot as plt
import sys



def represent_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def read_nodes(file):
    line = file.readline()  # should be "Nodes FluidNodes"
    print('ReadNodes, the first line is ', line)
    nodes = []
    while line:
        line = file.readline()
        data = line.split()
        if represent_int(data[0]):
            nodes.append(list(map(float, data[1:4])))
        else:
            break
    print("ReadNodes reads ", len(nodes), " nodes")
    return file, line, nodes



def read_elems(file, line):
    print('ReadElems, the first line is ', line)
    elems = []
    while line:
        line = file.readline()
        data = line.split()
        if len(data) > 0 and represent_int(data[0]):
            elems.append(list(map(int, data[2:])))
        else:
            break
    print("ReadElems reads ", len(elems), " elems")
    return file, line, elems

    

def read_top_file(domain_top ='domain.top'):
    '''
    :param domain_geo:
    :return:
    '''
    file = open(domain_top, 'r')
    file, line, nodes = read_nodes(file)

    elems = {}
    
    file, line, elems['FluidMesh'] = read_elems(file, line)

    while line:
        data = line.split()
        file, line, elems[data[1]] = read_elems(file, line)

    file.close()

    return nodes, elems

def filter_elems_helper(elems3, nodes_map):
    elems2 = []
    for e3 in elems3:
        e2 = [nodes_map[i-1]+1 for i in e3 if nodes_map[i-1]>=0]
        if len(e2)>1:
            elems2.append(e2)
    return elems2
    

def filter_3d_to_2d(nodes3, elems3, eps=1e-8):
    # keep only nodes with z = 0.0
    nnodes3 = len(nodes3)
    nodes3 = np.array(nodes3)

    # nodes_map, all nodes are indexed from 0!!!
    nodes_map = np.full(nnodes3, -1, dtype=np.int64)
    ind = 0
    for i in range(nnodes3):
        if nodes3[i,2] < eps:
            nodes_map[i] = ind
            ind += 1

    nodes2 = nodes3[nodes_map>=0,:2]

    elems2 = {}
    elems2['grid'] = np.array(filter_elems_helper(elems3['SymmetryFixedSurface'], nodes_map) ) - 1
    elems2['farfield'] = np.array(filter_elems_helper(elems3['OutletFixedSurface'], nodes_map) ) - 1
    elems2['airfoil'] = np.array(filter_elems_helper(elems3['StickFixedSurface'], nodes_map) ) - 1
    
    return nodes2, elems2, nodes_map


def read_xpost_file(domain_xpost ='domain.xpost', nodes_map = None):
    data = np.loadtxt(domain_xpost, skiprows=1)
    nnodes = int(data[0])
    data = data[1:].reshape((nnodes+1, -1), order="F")
    time = data[0, :]
    field = data[1:, :]

    if nodes_map is not None:
        field = field[nodes_map >= 0, :]
    
    return time, field

def fluid_data(domain_top, domain_xpost):
    # top file and xpost file
    # return:
    # nodes: double[n,2], fluid mesh nodes
    # elems: int[e, 3], triagulation in nodes, index starting from 0
    # field: double[n], field
    # airfoil_ind: int[m, 3], airfoil node index in nodes, starting from 0
    # farfield_ind: int[m', 3], farfield node index in nodes, starting from 0
    # airfoil_nodes: double[m,2], airfoil mesh nodes 
    # airfoil_field: double[m], field on airfoil nodes
    # airfoil_elems: int[e, 2], segment in airfoil nodes, index starting from 0

    nodes3, elems3 = read_top_file(domain_top = domain_top)
    nodes, elems, nodes_map = filter_3d_to_2d(nodes3, elems3)
    # never use nodes3 and elems3
    time, field = read_xpost_file(domain_xpost =  domain_xpost, nodes_map = nodes_map)

    airfoil_ind = np.array(list(set(elems["airfoil"].flatten())), dtype=np.int64)
    farfield_ind = np.array(list(set(elems["farfield"].flatten())), dtype=np.int64)

    airfoil_nodes = nodes[airfoil_ind, :]
    airfoil_field = field[airfoil_ind]
    airfoil_ind_array = np.full(nodes.shape[0], -1)
    for i in range(len(airfoil_ind)):
        airfoil_ind_array[airfoil_ind[i]] = i
    airfoil_elems = airfoil_ind_array[elems["airfoil"]]

    return nodes, elems["grid"], field[:,-1], airfoil_ind, farfield_ind,\
    airfoil_nodes, airfoil_field,  airfoil_elems

    

if __name__ =='__main__':
    nodes, grid, field, airfoil_ind, farfield_ind, \
        airfoil_nodes, airfoil_field,  airfoil_grid \
            = fluid_data(domain_top ='../Airfoil3/sources/fluid.top', domain_xpost ='../Airfoil3/simulations/postpro.Steady/Pressure.xpost')
    
    fig, ax = plt.subplots(1, 1, figsize=(6,6))
    ax.set_aspect('equal')
    tpc = ax.tripcolor(nodes[:,0], nodes[:,1], field, triangles = grid, shading='flat')
    ax.scatter(nodes[airfoil_ind, 0], nodes[airfoil_ind, 1], color="red", linewidths=0.1)
    ax.scatter(nodes[farfield_ind, 0], nodes[farfield_ind, 1], color="black", linewidths=0.1)
    fig.colorbar(tpc, ax=ax)
    plt.tight_layout()
    plt.show()

    
    fig, ax = plt.subplots(1, 1, figsize=(6,6))
    ax.set_aspect('equal')
    airfoil = airfoil_nodes[airfoil_grid, :] 
    # segment k is airfoil[k, 0, :]-[k, 1, :]
    ax.plot(airfoil[:,:,0].T, airfoil[:,:,1].T, "-o", color="C0", markersize=2)
    plt.tight_layout()
    plt.show()
    