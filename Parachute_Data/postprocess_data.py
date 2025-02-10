import os
import numpy as np
import sys
sys.path.append( 'Parachute_Design' )

import Parachute_Design.Parachute_Postprocess as Parachute_Postprocess 


def postprocess_data(input_folder_name, output_folder_name, input_index, output_index):
    nodes, elems, time, fields, line_node_indicator \
            = Parachute_Postprocess.structure_data(domain_top ='./'+input_folder_name+'_%05d/sources/StructureFile.include'%(input_index), \
                                    domain_xposts =['./'+input_folder_name+'_%05d/simulations/results/structure.GDISPLAC.xpost'%(input_index)])
    
    nnodes, nt = nodes.shape[0], len(time)
    if nt != 51 or fields.shape[1] != 3*nt:
        return False
    
    features = np.concatenate((fields, line_node_indicator[:, np.newaxis] ), axis=1)
    
    # if the demo_folder directory is not present  
    # then create it. 
    if not os.path.exists(output_folder_name):
        os.makedirs(output_folder_name)
      
    np.save(output_folder_name + "/nodes_%05d"%(output_index) + ".npy", nodes)
    np.save(output_folder_name + "/elems_%05d"%(output_index) + ".npy", elems)
    np.save(output_folder_name + "/features_%05d"%(output_index) + ".npy", features)

    return True
    

    

if __name__ == "__main__":
    
    for parachute_type in ["DGB", "Arc", "Ribbon"]:
        ndata = 2000
        residuals = np.zeros(ndata)
        index = 0
        for i in range(ndata):
            print("Postprocess data %05d " %(i))
            data_quality = postprocess_data(input_folder_name="Parachute_"+parachute_type, output_folder_name="Parachute_data/"+parachute_type, input_index=i, output_index=index)
            if data_quality:
                residuals[index] = data_quality
                index += 1
            print("Postprocess data %05d -> %05d" %(i, index-1), " data quality ", data_quality)
        np.save("Parachute_"+parachute_type+"_data.npy", residuals[0:index])

