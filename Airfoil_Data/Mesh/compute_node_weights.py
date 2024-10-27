import numpy as np
import matplotlib.pyplot as plt

def compute_triangle_area(points):
    ab = points[1, :] - points[0,:]
    ac = points[2, :] - points[0,:]
    cross_product = np.cross(ab, ac)
    return 0.5 * np.linalg.norm(cross_product)


def compute_tetrahedron_volume(points):
    ab = points[1, :] - points[0,:]
    ac = points[2, :] - points[0,:]
    ad = points[3, :] - points[0,:]
    
    # Calculate the scalar triple product
    volume = abs(np.dot(np.cross(ab, ac), ad)) / 6
    return volume

def compute_weight_per_elem(points, type):
    # compute elem area
    # type: length, area, volume
    n, ndim = points.shape
    if type == "length":
        assert(n == 2)
        s = np.linalg.norm(points[0, :] - points[1, :])
    elif type == "area":
        assert(n == 3 or n == 4)
        if n == 3:
            s = compute_triangle_area(points)
        else:
            s = compute_triangle_area(points[:3,:]) + compute_triangle_area(points[1:,:])
    elif type == "volume":
        assert(n == 4)
        s = compute_tetrahedron_volume(points)
    else:
        raise ValueError("type ", type,  "is not recognized")
    
    return s


def compute_weights(nodes, elems, type):
    nnodes = nodes.shape[0]
    weights = np.zeros(nnodes)
    for e in elems:
        ne = len(e)
        s = compute_weight_per_elem(nodes[e, :], type)
        weights[e] += s/ne 
    return weights

if __name__ == "__main__":
    elems = np.array([[0,1,2],[0,2,3]])
    type = "area"
    nodes = np.array([[0.0,0.0],[1.0,0.0],[1.0,1.0],[0.0,1.0]]) 
    assert(np.linalg.norm(compute_weights(nodes, elems, type) - np.array([1.0/3, 1.0/6, 1.0/3, 1.0/6])) < 1e-15)

    elems = np.array([[0,1,2],[0,2,3]])
    type = "area"
    nodes = np.array([[0.0,0.0,1.0],[1.0,0.0,1.0],[1.0,1.0,1.0],[0.0,1.0,1.0]]) 
    assert(np.linalg.norm(compute_weights(nodes, elems, type) - np.array([1.0/3, 1.0/6, 1.0/3, 1.0/6])) < 1e-15)
    

    elems = np.array([[0,1],[1,2],[2,3]])
    type = "length"
    nodes = np.array([[0.0,0.0,1.0],[1.0,0.0,1.0],[1.0,1.0,1.0],[0.0,1.0,1.0]]) 
    assert(np.linalg.norm(compute_weights(nodes, elems, type) - np.array([0.5, 1.0, 1.0, 0.5])) < 1e-15)
    

    elems = np.array([[0,1,2,4],[0,2,3,4]])
    type = "volume"
    nodes = np.array([[0.0,0.0,0.0],[1.0,0.0,0.0],[1.0,1.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]]) 
    assert(np.linalg.norm(compute_weights(nodes, elems, type) - np.array([1.0/12.0, 1.0/24.0, 1.0/12.0, 1.0/24.0, 1.0/12.0])) < 1e-15)
    