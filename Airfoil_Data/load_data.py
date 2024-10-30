import os
import numpy as np
import sys
import matplotlib.pyplot as plt
sys.path.append( 'Mesh' )


def load_data(input_folder_name="Airfoil_data", index=0):
    
    

    nodes = np.load(input_folder_name + "/fluid_mesh/nodes_%05d"%(index) + ".npy")
    elems = np.load(input_folder_name + "/fluid_mesh/elems_%05d"%(index) + ".npy")
    fluid_features = np.load(input_folder_name + "/fluid_mesh/features_%05d"%(index) + ".npy")

    airfoil_nodes = np.load(input_folder_name + "/airfoil_mesh/nodes_%05d"%(index) + ".npy")
    airfoil_elems = np.load(input_folder_name + "/airfoil_mesh/elems_%05d"%(index) + ".npy")
    airfoil_features = np.load(input_folder_name + "/airfoil_mesh/features_%05d"%(index) + ".npy")
    

    return nodes, elems, fluid_features, airfoil_nodes, airfoil_elems, airfoil_features

if __name__ == "__main__":
    
    nodes, elems, fluid_features, airfoil_nodes, airfoil_elems, airfoil_features = load_data(input_folder_name="Airfoil_data", index=3)

    pressure, mach, airfoil_ind, farfield_ind = fluid_features[:,0], fluid_features[:,1], fluid_features[:,2], fluid_features[:,3]
    fig, ax = plt.subplots(1, 1, figsize=(6,6))
    ax.set_aspect('equal')
    tpc= ax.tripcolor(nodes[:,0], nodes[:,1], pressure, triangles = elems, shading='flat')
    ax.set_title("Pressure")
    ax.scatter(nodes[airfoil_ind == 1.0, 0], nodes[airfoil_ind == 1.0, 1], color="red", s=0.1)
    ax.scatter(nodes[farfield_ind == 1.0, 0], nodes[farfield_ind == 1.0, 1], color="black", s=0.1)
    fig.colorbar(tpc, ax=ax)
    plt.tight_layout()
    plt.show()
    fig, ax = plt.subplots(1, 1, figsize=(6,6))
    ax.set_aspect('equal')
    tpc= ax.tripcolor(nodes[:,0], nodes[:,1], mach, triangles = elems, shading='flat')
    ax.set_title("Mach")
    ax.scatter(nodes[airfoil_ind == 1.0, 0], nodes[airfoil_ind == 1.0, 1], color="red", s=0.1)
    ax.scatter(nodes[farfield_ind == 1.0, 0], nodes[farfield_ind == 1.0, 1], color="black", s=0.1)
    fig.colorbar(tpc, ax=ax)
    plt.tight_layout()
    plt.show()

    
    
    fig, ax = plt.subplots(1, 1, figsize=(6,6))
    ax.set_aspect('equal')
    airfoil = airfoil_nodes[airfoil_elems, :] 
    # segment k is airfoil[k, 0, :]-[k, 1, :]
    ax.plot(airfoil[:,:,0].T, airfoil[:,:,1].T, "-o", color="C0", markersize=2)
    plt.tight_layout()
    plt.show()
    
    airfoil_pressure, airfoil_mach, = airfoil_features[:,0], airfoil_features[:,1]
    # airfoil_pressure, airfoil_mach, = airfoil_features[airfoil_elems,0], airfoil_features[airfoil_elems,1]
    fig, axs = plt.subplots(2, 1, figsize=(12,6))
    # segment k is airfoil[k, 0, :]-[k, 1, :]
    axs[0].scatter(airfoil_nodes[:,0], airfoil_pressure, color="C0", s=1)
    axs[0].plot(airfoil[:,:,0].T, airfoil_pressure[airfoil_elems].T, color="C0")
    axs[0].set_title("Pressure")
    axs[1].scatter(airfoil_nodes[:,0], airfoil_mach, color="C0", s=1)
    axs[1].plot(airfoil[:,:,0].T, airfoil_mach[airfoil_elems].T, color="C0")
    axs[1].set_title("Mach")
    plt.tight_layout()
    plt.show()

   