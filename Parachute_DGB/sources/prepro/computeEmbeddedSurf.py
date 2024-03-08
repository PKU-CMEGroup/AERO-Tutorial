'''
This is a file, reading parachute structure file and writing parachute embedded file
'''
import sys
import numpy as np

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

def ReadElems(file, line):
    print('ReadElems, the first line is ', line)
    elems = []
    type = -1
    while line:
        line = file.readline()
        data = line.split()
        if not line or data[0][0] == '*':
            continue
        if RepresentsInt(data[0]):
            type = len(data) - 2
            elem_node = list(map(int, data[2:]))
            if type == 3 or type == 2:
                elems.append(list(map(int, data[2:])))
            elif type == 4:
                elems.append([elem_node[0], elem_node[1], elem_node[2]])
                elems.append([elem_node[2], elem_node[3], elem_node[0]])

        else:
            break
    print("ReadElems reads ", len(elems), " elems")
    return file, line, elems, type


def SplitLines(line_elems):
    '''
    :param line_elems:
    :return:
    '''
    j_old = -1
    line, lines = [], []
    for i,j in line_elems:
        if i != j_old:
            if line:
                lines.append(line)
            line = [i,j]

        else:
            line.append(j)
        j_old = j
    lines.append(line)
    return lines




def LineDressing(line_coord, r, shape, close_or_not = True, A = None, B = None):
    '''
    :param line_coord:
    :param r:
    :param shape:
    :param skip:
    :param close_or_not:  the tube is closed or not
    :param A, B specify the top and bottom center node if the tube is closed
    :return:
    '''
    print("In LineDressing, the line coord shape is ", np.shape(line_coord))
    n = np.shape(line_coord)[0]

    phantom_coord = np.empty(shape=[2*close_or_not + n   * shape, 3], dtype=float)
    phantom_tris =  np.empty(shape=[2*shape*(n + close_or_not - 1), 3], dtype=float)
    if A is None or B is None:
        A = line_coord[0, :]
        B = line_coord[-1 , :]

    nx, ny, nz = dir = (B - A) / np.linalg.norm(B - A)  # direction of AB
    e1 = np.array([1.0, 0.0, 0.0], dtype=float)
    e2 = np.array([0.0, 1.0, 0.0], dtype=float)
    e3 = np.array([0.0, 0.0, 1.0], dtype=float)

    theta = 2 * np.pi / shape

    # Rotation matrix on https://en.wikipedia.org/wiki/Rotation_matrix
    R = np.array([[np.cos(theta) + nx * nx * (1 - np.cos(theta)), nx * ny * (1 - np.cos(theta)) - nz * np.sin(theta),
                   nx * nz * (1 - np.cos(theta)) + ny * np.sin(theta)],
                  [ny * nx * (1 - np.cos(theta)) + nz * np.sin(theta), np.cos(theta) + ny * ny * (1 - np.cos(theta)),
                   ny * nz * (1 - np.cos(theta)) - nx * np.sin(theta)],
                  [nz * nx * (1 - np.cos(theta)) - ny * np.sin(theta),
                   nz * ny * (1 - np.cos(theta)) + nx * np.sin(theta), np.cos(theta) + nz * nz * (1 - np.cos(theta))]],
                 dtype=float)

    phantom_dr = np.empty(shape=[shape, 3], dtype=float)

    if(np.linalg.norm(np.cross(dir, e1)) > 0.5):
        phantom_dr[0, :] = r * np.cross(dir, e1)/np.linalg.norm(np.cross(dir, e1))
    elif(np.linalg.norm(np.cross(dir, e2)) > 0.5):
        phantom_dr[0, :] = r * np.cross(dir, e2)/np.linalg.norm(np.cross(dir, e2))
    elif (np.linalg.norm(np.cross(dir, e3)) > 0.5):
        phantom_dr[0, :] = r * np.cross(dir, e3)/np.linalg.norm(np.cross(dir, e3))
    else:
        print('error in LineDressing')

    if close_or_not:
        phantom_coord[0,:],phantom_coord[-1,:] = A,B


    for j in range(1, shape):
        phantom_dr[j, :] = np.dot(R, phantom_dr[j - 1, :])

    for i in range(n):
        for j in range(shape):
            phantom_coord[i * shape + j + close_or_not, :] = line_coord[i, :] + phantom_dr[j, :]


    #Bottom
    if close_or_not:
        for j in range(shape):
            phantom_tris[j , :] = 0,  (j+1)%shape + 1 , j+1

    for i in range(n - 1):
        for j in range(shape):
            phantom_tris[shape*close_or_not + 2 * i * shape + 2 * j, :]     = shape*i + j + close_or_not , shape*i + (j+1)%shape + close_or_not , shape*i + (j+1) + shape + close_or_not - 1
            phantom_tris[shape*close_or_not + 2 * i * shape + 2 * j + 1, :] = shape*i + (j+1)%shape + close_or_not , shape*i + shape + (j+1)%shape + close_or_not , shape*i + (j+1) + shape + close_or_not - 1



    #Top
    if close_or_not:
        for j in range(shape):
            phantom_tris[-1 - j, :] = shape*n + 1,  shape*n - shape + j + 1, shape*n - shape + (j + 1)%shape + 1

    return phantom_coord, phantom_tris


def ReadStru(inputStru, beamPars):
    '''
    :param inputStru:
    :param beamPars: parameters to handle phantom surface, skip beamPars[0] beams at all ends of these lines, the shape of
    the cross section beamPars[1], 4 for square, radius of the cross section beamPars[2], beamPars[3] close or not,
    sharp_or_not 1 or 0, adjust A and B for sharp tip or not
    beamPars[4]: sharp_or_not
    :return: nodes: a list of 3 double,
             elems: a list of 3 int
    '''
    try:
        struFile = open(inputStru, "r")
    except IOError:
        print("File '%s' not found." % inputStru)
        sys.exit()

    skip, shape, r, close_or_not, sharp_or_not = beamPars

    sharp_or_not = 0
    nodes = []
    embSurfs = []
    bunchLines = []

    print('Reading Structure mesh ...')
    file, line, nodes = ReadNodes(struFile)
    while line:
        '''
        It should read (0)Band Gores, Disk Gores, (1)Gap Lines, (2)Suspension Lines, (3)Vent Lines
        '''
        data = line.split()
        struFile, line, elems, type = ReadElems(struFile, line)
        print('Elem type is ', type)
        if (type == 3 or type == 4):
            embSurfs.append(elems)
        elif (type == 2):
            bunchLines.append(elems)
    struFile.close()

    print('Processing data ...')
    embNodeSet = set()
    for elems in embSurfs:
        for i, j, k in elems:
            embNodeSet.add(i)
            embNodeSet.add(j)
            embNodeSet.add(k)
    print('Process data ... #Node is ', len(embNodeSet))
    embNodes = list(embNodeSet)
    sorted(embNodes)

    allLines = []
    phantomCoords = [[], [], []]
    phantomTris = [[], [], []]
    for i in range(len(bunchLines)):
        print('line banch ', i)
        lines = SplitLines(bunchLines[i])
        allLines.append(lines)

    for i in range(len(allLines)):
        for line in allLines[i]:
            print('len(line) is ', len(line))
            line_coord = np.empty([len(line) - 2 * skip, 3], dtype=float)
            for j in range(len(line) - 2 * skip):
                line_coord[j, :] = nodes[line[j + skip] - 1]

            A = np.array(nodes[line[skip - sharp_or_not] - 1])
            B = np.array(nodes[line[len(line) - skip + sharp_or_not - 1] - 1])
            phantomCoord, phantomTri = LineDressing(line_coord, r, shape, close_or_not, A, B)

            phantomCoords[i].append(phantomCoord)
            phantomTris[i].append(phantomTri)

    return embNodes, nodes, phantomCoords, embSurfs, phantomTris


def ReadPayload(inputPayload):
    '''
    :param inputPayload:
    :return: nodes: a list of 3 double,
             elems: a list of 3 int
    '''
    try:
        payloadFile = open(inputPayload, "r")
    except IOError:
        print("File '%s' not found." % inputPayload)
        sys.exit()

    print('Reading payload mesh ...')
    file, line, nodes = ReadNodes(payloadFile)


    file, line, elems, type = ReadElems(file, line)
    if type != 3:
        print('unknown elements type: ', type, ' in the payload files')
    payloadFile.close()

    return nodes, elems



def ParachuteEmbSurf(type, beamPars = [1, 4, 0.01, True], inputStru = './mesh_emb_raw.top', inputPayload = './capsule.top', output = 'embeddedSurface.top'):
    # beamPars[2] is the radius

    print("REMINDER: NO EMPTY LINES AT THE END")
    fabricNodes, fabricNodeCoord, phantomCoords, fabricEmbSurfs, phantomTris  = ReadStru(inputStru, beamPars)
    if(type == 1):
        payloadNodes, payloadElems = ReadPayload(inputPayload)


    print('Writing mesh ...')
    embFile = open(output, 'w')
    embFile.write('Nodes nodeset\n')

    nodeId = [0, 0, 0]
    #Step1.1 write fabric nodes
    fabricNodeNum = len(fabricNodes)
    nodeId[0] = fabricNodeNum
    for i in range(fabricNodeNum):
        embFile.write('%d  %.16E %.16E  %.16E\n' % (i + 1, fabricNodeCoord[fabricNodes[i]-1][0], fabricNodeCoord[fabricNodes[i]-1][1], fabricNodeCoord[fabricNodes[i]-1][2]))

    # Step1.2 write phantom suspension line surface nodes
    nId = fabricNodeNum
    # write nodes
    for i in range(len(phantomCoords)):
        for j in range(len(phantomCoords[i])):
            phantomCoord = phantomCoords[i][j]
            for k in range(len(phantomCoord)):
                nId += 1
                embFile.write(
                    '%d  %.12f  %.12f  %.12f\n' % (nId, phantomCoord[k, 0], phantomCoord[k, 1], phantomCoord[k, 2]))
    nodeId[1] = nId
    # Step1.3 write payload surface nodes
    if (type == 1):
        # write nodes
        for i in range(len(payloadNodes)):
            embFile.write('%d  %.12f  %.12f  %.12f\n' % (i + nId + 1, payloadNodes[i][0], payloadNodes[i][1], payloadNodes[i][2]))
        nodeId[2] = len(payloadNodes) + nId + 1

    print('fabric nodes:[', 1, ' , ', nodeId[0],
          '] phantom suspension line nodes: [', nodeId[0]+1, ' , ', nodeId[1],
          '] payload nodes: [', nodeId[1]+1, ' , ', nodeId[2], ']')

    # Step2.1 write fabric surface elems
    elemId = [0,0,0]
    fabricNodesMap = {}
    for i in range(len(fabricNodes)):
        fabricNodesMap[fabricNodes[i]] = i + 1
    nS = 0;
    for nType in range(len(fabricEmbSurfs)):
        print('nType is ', nType)
        embFile.write('Elements StickMovingSurface_%d using nodeset\n' % (nType + 1))
        for i in range(len(fabricEmbSurfs[nType])):
            nS += 1
            embFile.write('%d  4  %d  %d  %d\n' % (
            nS, fabricNodesMap[fabricEmbSurfs[nType][i][0]], fabricNodesMap[fabricEmbSurfs[nType][i][1]],
            fabricNodesMap[fabricEmbSurfs[nType][i][2]]))
    elemId[0] = nS
    # Step2.2 write suspension line phantom surface elems
    firstNode = nodeId[0] + 1
    for i in range(len(phantomCoords)):
        nType += 1
        embFile.write('Elements StickMovingSurface_%d using nodeset\n' % (nType + 1))
        for j in range(len(phantomTris[i])):

            phantomCoord = phantomCoords[i][j]
            phantomTri = phantomTris[i][j]
            for k in range(len(phantomTri)):
                nS += 1
                embFile.write('%d  4 %d  %d  %d\n' % (
                nS, firstNode + phantomTri[k, 0], firstNode + phantomTri[k, 1], firstNode + phantomTri[k, 2]))
            firstNode += len(phantomCoord)
    elemId[1] = nS
    # Step2.3 write payload surface elems
    if(type == 1):
        firstNode = nodeId[1]
        nType += 1
        embFile.write('Elements StickFixedSurface_%d using nodeset\n' % (nType + 1))
        for i in range(len(payloadElems)):
            nS += 1
            embFile.write('%d  4 %d  %d  %d\n' % (
                        nS, firstNode + payloadElems[i][0], firstNode + payloadElems[i][1], firstNode + payloadElems[i][2]))
            elemId[2] = nS

    print('fabric elems:[', 1, ' , ', elemId[0],
          '] phantom suspension line elems: [', elemId[0] + 1, ' , ', elemId[1],
          '] payload elems: [', elemId[1] + 1, ' , ', elemId[2], ']')
    embFile.close()




if __name__ == '__main__':
    # suspension line diameter and radius
    d = 3.175e-3
    r = d/2.0
    
    '''
    type: 1: including capsule, 2: not including capsule
    
    beamPars: parameters to handle phantom surface, skip beamPars[0] beams at all ends of these lines, the shape of
    the cross section beamPars[1], 4 for square, radius of the cross section beamPars[2], beamPars[3] close or not,
    sharp_or_not 1 or 0, adjust A and B for sharp tip or not

    inputStru: structure file 
    And you need to clean it to have only nodes, canopy and suspension lines(do not need Disk outer/inner edges, seams....)
    If you do not want suspension line dressing, remove suspension lines from the mesh_Structural.top.tria
    '''
    # whether or not consider capsule
    considerCapsule = True
    # whether or not consider fluid suspension line interaction
    considerSuspensionLine = False

    embType = 1 if considerCapsule else 2
    inputStru = 'parachute_susp_line_emb_mesh.top' if considerSuspensionLine else 'parachute_emb_mesh.top'
    ParachuteEmbSurf(type=embType, beamPars=[6, 6, r, True, 0], inputStru=inputStru,
                     inputPayload='./capsule.top',
                     output='embeddedSurface.top')

    