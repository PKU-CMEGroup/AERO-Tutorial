import os
import numpy as np
import sys
sys.path.append( 'Mesh' )

import Mesh.gmsh_geo_generator as gmsh_geo_generator 
#uniform distribution

def generate_paras(ndata=5000, seed=42):
    np.random.seed(seed)
    paras = np.random.uniform(0, 1, (ndata, 8))
    # m : the amount of camber as a fraction of chord length
    # p : the location of maximum camber as a fraction of chord length
    # t : thickness as a fraction of chord length
    paras[:, 0] = paras[:, 0]*0.09                   # m in U[0,0.09]
    paras[:, 1] = paras[:, 1]*0.4  + 0.2             # p in U[0.2,0.6]
    paras[:, 2] = paras[:, 2]*0.25 + 0.05            # t in U[0.05,0.3]
    paras[:, 3] = paras[:, 3]*0.09                   # m_f in U[0,0.09]
    paras[:, 4] = paras[:, 4]*0.4  + 0.2             # p_f in U[0.2,0.6]
    paras[:, 5] = paras[:, 5]*0.1  + 0.1             # t_f in U[0.1,0.2]
    paras[:, 6] = paras[:, 3]*35.0 + 5.0             # theta_f (flap angle) in U[5,40]
    paras[:, 7] = paras[:, 4]*25.0 - 5.0             # theta (angle of attack) in U[-5,20]

    return paras

#  source ~/.bashrc_frg  before runing code
def generate_airfoil(paras, flap_or_not):
    os.system("source ~/.bashrc_frg")
    ndata, _ = paras.shape

    for i in range(ndata):

        if flap_or_not:
            os.system("cp -r Airfoil Airfoil_flap_%05d" %(i))
            os.chdir("./Airfoil_flap_%05d/sources" %(i))
            gmsh_geo_generator.naca_flap_fluid_mesh(domain_geo ='fluid.geo', m=paras[i,0], p=paras[i,1], t=paras[i,2], \
                                m_f=paras[i,3], p_f=paras[i,4], t_f=paras[i,5], theta_f=paras[i,6], theta = paras[i,7])
        else:
            os.system("cp -r Airfoil Airfoil_%05d" %(i))
            os.chdir("./Airfoil_%05d/sources" %(i))
            gmsh_geo_generator.naca_fluid_mesh(domain_geo ='fluid.geo', m=paras[i,0], p=paras[i,1], t=paras[i,2], theta=paras[i,7])


        os.system("gmsh -3 fluid.geo -format msh22")

        os.system("gmsh2top fluid")

        os.chdir("..")

        os.system("bash preprocess.sh")

        os.chdir("./simulations")

        os.system("sbatch Sbatch.Steady.sh")
        os.chdir("..")
        os.chdir("..")

if __name__ == "__main__":
    # paras = np.zeros((4, 8))
    # paras[:, 0] = 0.09                                   # m in U[0,0.09]
    # paras[:, 1] = 0.6                                    # p in U[0.2,0.6]
    # paras[:, 2] = 0.05, 0.05, 0.3, 0.3                   # t in U[0.05,0.3]
    # paras[:, 3] = 0.09                                   # m_f in U[0,0.09]
    # paras[:, 4] = 0.2                                    # p_f in U[0.2,0.6]
    # paras[:, 5] = 0.1,  0.2,  0.1, 0.2                   # t_f in U[0.1,0.2]
    # paras[:, 6] = 5.0                                    # theta_f (flap angle) in U[5,40]
    # paras[:, 7] = 0.0                                    # theta (angle of attack) in U[-5,20]

    # generate_airfoil(paras, True)

    GENERATE_AIRFOIL_FLAP_DATA = False
    if GENERATE_AIRFOIL_FLAP_DATA:
        paras = generate_paras(ndata=2000, seed=42)
        generate_airfoil(paras, True)

    GENERATE_AIRFOIL_DATA = True
    if GENERATE_AIRFOIL_DATA:
        paras = generate_paras(ndata=2000, seed=24)
        generate_airfoil(paras, False)
