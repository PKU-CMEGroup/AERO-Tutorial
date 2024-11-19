import os
import numpy as np
import sys
sys.path.append( 'Mesh' )

import Mesh.top_reader as top_reader 
#uniform distribution


def postprocess_data(input_folder_name, output_folder_name, input_index, output_index, residual_max = 1e-7):
    nodes, grid, fields, airfoil_ind, farfield_ind, \
        airfoil_nodes, airfoil_grid, airfoil_fields \
            = top_reader.fluid_data(domain_top ='./'+input_folder_name+'_%05d/sources/fluid.top'%(input_index), \
                                    domain_xposts =['./'+input_folder_name+'_%05d/simulations/postpro.Steady/Pressure.xpost'%(input_index), \
                                                    './'+input_folder_name+'_%05d/simulations/postpro.Steady/Mach.xpost'%(input_index)])
    nnodes, nairfoil_nodes = nodes.shape[0], airfoil_nodes.shape[0]
    
    fluid_mask = np.zeros((nnodes, 1))
    fluid_mask[airfoil_ind] = 1 
    fluid_mask[farfield_ind] = 2
    fluid_features = np.concatenate((fields, fluid_mask), axis=1)
    
    # if the demo_folder directory is not present  
    # then create it. 
    if not os.path.exists(output_folder_name+ "/fluid_mesh"):
        os.makedirs(output_folder_name+ "/fluid_mesh")
    if not os.path.exists(output_folder_name+ "/airfoil_mesh"):
        os.makedirs(output_folder_name+ "/airfoil_mesh")   
      
    
    
    residual  = 1.0
    try: 
        with open('./'+input_folder_name+'_%05d/simulations/log.Steady.out'%(input_index), 'r') as log_file:
            lines = log_file.readlines()
        residual = np.float64(lines[-45].split()[4][:-1])
    except ValueError:
        residual  = 1.0
    except IndexError:
        residual  = 1.0
    
    if residual < residual_max:

        np.save(output_folder_name + "/fluid_mesh/nodes_%05d"%(output_index) + ".npy", nodes)
        np.save(output_folder_name + "/fluid_mesh/elems_%05d"%(output_index) + ".npy", grid)
        np.save(output_folder_name + "/fluid_mesh/features_%05d"%(output_index) + ".npy", fluid_features)

        np.save(output_folder_name + "/airfoil_mesh/nodes_%05d"%(output_index) + ".npy", airfoil_nodes)
        np.save(output_folder_name + "/airfoil_mesh/elems_%05d"%(output_index) + ".npy", airfoil_grid)
        np.save(output_folder_name + "/airfoil_mesh/features_%05d"%(output_index) + ".npy", airfoil_fields)

        return True, residual
    
    else: 
        return False, residual
    

if __name__ == "__main__":
    

    POSTPROCESS_AIRFOIL_FLAP_DATA = True
    if POSTPROCESS_AIRFOIL_FLAP_DATA:
        ndata = 2000
        residuals = np.zeros(ndata)
        index = 0
        for i in range(ndata):
            print("Postprocess data %05d " %(i))
            data_quality, residual = postprocess_data(input_folder_name = "Airfoil_flap", output_folder_name="Airfoil_flap_data", input_index=i, output_index=index)
            if data_quality:
                residuals[index] = residual
                index += 1
            print("Postprocess data %05d -> %05d" %(i, index-1), ", data residual ", residual, " data quality ", data_quality)
        np.save("Airfoil_flap_residual.npy", residuals[0:index])


    POSTPROCESS_AIRFOIL_DATA = True
    if POSTPROCESS_AIRFOIL_DATA:
        ndata = 2000
        residuals = np.zeros(ndata)
        index = 0
        for i in range(ndata):
            data_quality, residual = postprocess_data(input_folder_name = "Airfoil", output_folder_name="Airfoil_data", input_index=i, output_index=index)
            if data_quality:
                residuals[index] = residual
                index += 1
            print("Postprocess data %05d -> %05d" %(i, index-1), ", data residual ", residual, "data quality ", data_quality)
            
        np.save("Airfoil_residual.npy", residuals[0:index])
