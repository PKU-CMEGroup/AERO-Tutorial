import os
import numpy as np
from Mesh.gmsh_geo_generator import naca_flap_fluid_mesh
#uniform distribution
np.random.seed(42)

ndata = 5000
paras = np.random.uniform(0, 1, (ndata, 7))
# m : (0.0, 0.095) the amount of camber as a fraction of chord length
# p : (0.0, 0.9) the location of maximum camber as a fraction of chord length
# t : (0.01, 0.4) thickness as a fraction of chord length
paras[:, 0] = paras[:, 0]*0.095                  #m in U[0,0.095]
paras[:, 1] = paras[:, 1]*0.4 + 0.2              #p in U[0.2,0.6]
paras[:, 2] = paras[:, 2]*0.39 + 0.01            #t in U[0.01,0.4]
paras[:, 3] = paras[:, 3]*0.095                  #m_f in U[0,0.095]
paras[:, 4] = paras[:, 4]*0.4 + 0.2              #p_f in U[0.2,0.6]
paras[:, 5] = paras[:, 5]*0.39 + 0.01            #t_f in U[0.01,0.4]
paras[:, 6] = paras[:, 3]*35.0 + 5.0             #theta_f (flap angle) in U[5,40]
paras[:, 7] = paras[:, 4]*25.0 - 5.0             #theta (angle of attack) in U[-5,20]


for i in range(ndata):
    os.system("cp -r Airfoil Airfoil_%05d" %(i))
    os.system("cd Airfoil_%05d/sources" %(i))

    naca_flap_fluid_mesh(domain_geo ='fluid.geo', m=paras[i,0], p=paras[i,1], t=paras[i,2], \
                        m_f=paras[i,3], p_f=paras[i,4], t_f=paras[i,5], theta_f=paras[i,6], theta = paras[i,7])

    os.system("gmsh -3 fluid.geo -format msh22")

    os.system("msh2top fluid")

    os.system("cd ..")

    os.system("bash preprocess.sh")

    os.system("cd simulations")

    os.system("sbatch Sbatch.Steady.sh")

