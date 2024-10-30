import os
import numpy as np
import sys
import open3d as o3d
sys.path.append( 'Mesh' )

import Mesh.top_reader as top_reader 
#uniform distribution


def postprocess_data(input_folder_name = "Airfoil_flap", output_folder_name="Airfoil_data", index=0):
    nodes, grid, fields, airfoil_ind, farfield_ind, \
        airfoil_nodes, airfoil_grid, airfoil_fields \
            = top_reader.fluid_data(domain_top ='./'+input_folder_name+'_%05d/sources/fluid.top'%(index), \
                                    domain_xposts =['./'+input_folder_name+'_%05d/simulations/postpro.Steady/Pressure.xpost' %(index), \
                                                    './'+input_folder_name+'_%05d/simulations/postpro.Steady/Mach.xpost' %(index)])
    nnodes, nairfoil_nodes = nodes.shape[0], airfoil_nodes.shape[0]
    
    fluid_mask = np.zeros((nnodes, 2))
    fluid_mask[airfoil_ind,  0] = 1 
    fluid_mask[farfield_ind, 1] = 1
    fluid_features = np.concatenate((fields, fluid_mask), axis=1)
    
    if not os.path.exists(output_folder_name+ "/fluid_mesh"):
        os.makedirs(output_folder_name+ "/fluid_mesh")
    if not os.path.exists(output_folder_name+ "/airfoil_mesh"):
        os.makedirs(output_folder_name+ "/airfoil_mesh")   
      
    # if the demo_folder directory is not present  
    # then create it. 
    

    np.save(output_folder_name + "/fluid_mesh/nodes_%05d"%(index) + ".npy", nodes)
    np.save(output_folder_name + "/fluid_mesh/elems_%05d"%(index) + ".npy", grid)
    np.save(output_folder_name + "/fluid_mesh/features_%05d"%(index) + ".npy", fluid_features)

    np.save(output_folder_name + "/airfoil_mesh/nodes_%05d"%(index) + ".npy", airfoil_nodes)
    np.save(output_folder_name + "/airfoil_mesh/elems_%05d"%(index) + ".npy", airfoil_grid)
    np.save(output_folder_name + "/airfoil_mesh/features_%05d"%(index) + ".npy", airfoil_fields)
    

if __name__ == "__main__":
    for i in range(4):
        postprocess_data(input_folder_name = "Airfoil_flap", output_folder_name="Airfoil_data", index=i)