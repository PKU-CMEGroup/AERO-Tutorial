import os
import numpy as np
import sys
sys.path.append("Parachute_Design")

import Parachute_Design.Parachute_Generator as Parachute_Generator
import Parachute_Design.Parachute_Aero_Suite as Parachute_Aero_Suite
#uniform distribution

def generate_paras(parachute_type, ndata=5000, seed=42):
    l = 10.0 
    
    np.random.seed(seed)
    p = np.random.uniform(0, 1, (ndata, 8))


    p[:, 0] = p[:, 0]*4.0 + 5.0                  # Dn in U[5.0, 9.0]
    p[:, 1] = p[:, 1]*0.5 + 0.5                  # Dv in U[0.5, 1.0]

    if parachute_type == "Ribbon":
        p[:, 2] = p[:, 2]*2.0                     # H  in U[0.0, 2.0] for Ribbon 
    else:
        p[:, 2] = p[:, 2] + 1.0                    # H  in U[1.0, 2.0] for DGB or Ringsail

    n_paras = -1
    if parachute_type == "DGB":
        p[:, 3] = p[:, 3]*0.1 + 0.2               # alpha in U[0.2, 0.3]
        n_paras = 4

    elif parachute_type == "Ribbon":
        p[:, 3] = p[:, 3]*0.2 + 0.2               # alpha in U[0.2, 0.4]          
        p[:, 4] = p[:, 4]*0.2 + 0.6               # alpha in U[0.6, 0.8]
        n_paras = 5

    elif parachute_type == "Arc":
        p[:, 3] = p[:, 3]*0.05 + 0.25              # alpha in U[0.25, 0.3]
        p[:, 4] = p[:, 4]*0.05 + 0.35              # alpha in U[0.35,0.4]
        p[:, 5] = p[:, 5]*0.05 + 0.6               # alpha in U[0.6,0.65]
        p[:, 6] = p[:, 6]*0.05 + 0.75              # alpha in U[0.75,0.8]
        n_paras = 7
    

    n_gores = 4 * np.random.randint(4, 10, ndata)         # n_gores = 16, 20, 24, ... , 40
    
    paras = [[parachute_type, n_gores[i], l, *p[i,:n_paras]] for i in range(ndata)]
    return paras

#  source ~/.bashrc_frg  before runing code
def generate_parachute(paras):
    os.system("source ~/.bashrc_frg")
    ndata = len(paras)
    print("ndata = ", ndata)
    compute_npt_method, min_half_nelem = "double", 1
    cl_vertical, cl_horizontal = 1.0e-1, 1.0e-1

    for i in range(ndata):
        
        os.system("cp -r Parachute Parachute_%s_%05d" %(paras[i][0], i))

        os.chdir("./Parachute_%s_%05d/sources" %(paras[i][0], i))
        
        n_gores, points, gap_or_fabric, arcs_infos = Parachute_Generator.Parachute_Generator(paras[i])
        
        nodes, elems, node_info, elem_info = Parachute_Generator.Parachute_Mesh(n_gores, points, gap_or_fabric, arcs_infos, cl_vertical, cl_horizontal, compute_npt_method=compute_npt_method, min_half_nelem=min_half_nelem)
        
        Parachute_Aero_Suite.Write_Structure_File(nodes, elems, node_info, elem_info, node_disp = None, stru_file_name = "StructureFile.include", surf_file_name = "SelfContactSurfaceTopology.include")
        
        os.chdir("..")

        os.system("bash preprocess.sh")

        os.chdir("./simulations")

        os.system("sbatch Sbatch.sh")

        os.chdir("..")

        os.chdir("..")

# In case that the cluster fails
def regenerate_parachute(paras):
    os.system("source ~/.bashrc_frg")
    ndata = len(paras)
    print("ndata = ", ndata)
    compute_npt_method, min_half_nelem = "double", 1
    cl_vertical, cl_horizontal = 1.0e-1, 1.0e-1

    for i in range(ndata):
        # if the data file has been generated, skip
        if os.path.exists("./Parachute_%s_%05d/simulations/results/structure.GDISPLAC.xpost" %(paras[i][0], i)):
            continue


        os.chdir("./Parachute_%s_%05d/sources" %(paras[i][0], i))
        
        n_gores, points, gap_or_fabric, arcs_infos = Parachute_Generator.Parachute_Generator(paras[i])
        
        nodes, elems, node_info, elem_info = Parachute_Generator.Parachute_Mesh(n_gores, points, gap_or_fabric, arcs_infos, cl_vertical, cl_horizontal, compute_npt_method=compute_npt_method, min_half_nelem=min_half_nelem)
        
        Parachute_Aero_Suite.Write_Structure_File(nodes, elems, node_info, elem_info, node_disp = None, stru_file_name = "StructureFile.include", surf_file_name = "SelfContactSurfaceTopology.include")
        
        os.chdir("..")

        os.system("bash preprocess.sh")

        os.chdir("./simulations")

        os.system("sbatch Sbatch.sh")

        os.chdir("..")

        os.chdir("..")


if __name__ == "__main__":
    parachute_types = ["DGB", "Ribbon", "Arc"]
    seeds = [42, 111, 2]
    ndata = 2000
    for i in range(3):
        paras = generate_paras(parachute_types[i], ndata=ndata, seed=seeds[i])
        generate_parachute(paras)
        


    
