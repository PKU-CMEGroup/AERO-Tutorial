import numpy as np
import sys
from naca_four_digit_airfoil import naca_mesh, naca_flap_mesh


def naca_fluid_mesh(domain_geo ='domain.geo'):
    '''
    :param domain_geo:
    :return:
    '''
    ##################################################
    #Generate fluid domain
    #################################################
    #Background
    cl_bg = 5
    cl = 0.005
    ext = 0.1
    L = 50
    
    file = open(domain_geo, 'w')
    file.write("cl_bg = %.15f;\n" % (cl_bg))
    file.write("cl = %.15f;\n" % (cl))
    file.write("L = %.15f;\n" % (L))

    file.write("Point(1000) = {L,  0, 0, cl_bg};\n")
    file.write("Point(2000) = {0,  L, 0, cl_bg};\n")
    file.write("Point(3000) = {-L, 0, 0, cl_bg};\n")
    file.write("Point(4000) = {0, -L, 0, cl_bg};\n")
    file.write("Point(5000) = {0,  0, 0, cl_bg};\n")

    file.write("Circle(1) = {2000, 5000, 1000};\n")
    file.write("Circle(2) = {3000, 5000, 2000};\n")
    file.write("Circle(3) = {4000, 5000, 3000};\n")
    file.write("Circle(4) = {1000, 5000, 4000};\n")


    # compute airfoils 
    c, m, p, t = 1.0, 0.09, 0.4, 0.2
    npt = 80
    airfoil, _, _= naca_mesh(c, m, p, t, npt, True)
    n = airfoil.shape[0]

    for i in range(n):
        file.write("Point(%d) = {%.15f,  %.15f, 0.0, cl};\n" % (i+1, airfoil[i,0], airfoil[i,1]))
    
    file.write("Spline(5) = {")
    for i in range(npt-1):
        file.write("%d," %(i+1))
    file.write("%d};\n" %(npt))

    file.write("Spline(6) = {")
    for i in range(npt-1):
        file.write("%d," %(npt+i))
    file.write("%d};\n" %(1))



    # Refine mesh with Distance and Threshold
    # We then define a `Threshold' field, which uses the return value of the
    # `Distance' field 1 in order to define a simple change in element size
    # depending on the computed distances

    # SizeMax -                     /------------------
    #                              /
    #                             /
    #                            /
    # SizeMin -o----------------/
    #          |                |    |
    #        Point         DistMin  DistMax

    file.write("Field[1] = Distance;\n")
    file.write("Field[1].CurvesList = {5,6};\n")
    file.write("Field[1].Sampling = 100;\n")
    # boundary layer
    file.write("Field[2] = Threshold;\n")
    file.write("Field[2].InField = 1;\n")
    file.write("Field[2].SizeMin = cl;\n")
    file.write("Field[2].SizeMax = cl_bg;\n")
    file.write("Field[2].DistMin = 5*cl;\n")
    file.write("Field[2].DistMax = L;\n")
    # flow features
    file.write("Field[3] = Threshold;\n")
    file.write("Field[3].InField = 1;\n")
    file.write("Field[3].SizeMin = 4*cl;\n")
    file.write("Field[3].SizeMax = cl_bg;\n")
    file.write("Field[3].DistMin = 1.0;\n")
    file.write("Field[3].DistMax = L;\n")

    file.write("Field[4] = Min;\n")
    file.write("Field[4].FieldsList = {2, 3};\n")
    file.write("Background Field = 4;\n")




    file.write("Curve Loop(1) = {1, 4, 3, 2};\n" )
    file.write("Curve Loop(2) = {5, 6};\n" )
    file.write("Plane Surface(1) = {1, 2};\n" )

    file.write("Extrude {0, 0, %.15f} {Surface{1}; Layers{1};}\n" %(ext))
    file.write("Physical Surface(\"SymmetryFixedSurface\") = {1, 38};\n")
    file.write("Physical Surface(\"OutletFixedSurface\") = {29, 17, 21, 25};\n")
    file.write("Physical Surface(\"StickFixedSurface\") = {37, 33};\n")
    file.write("Physical Volume(\"FluidMesh\") = {1};\n")

    file.close()




def naca_flap_fluid_mesh(domain_geo ='domain.geo'):
    '''
    :param birdWing: a node list, n[0],n[1] ....n[m-1] n[0] is a close curve
    :param domain_geo:
    :return:
    '''
    ##################################################
    #Generate fluid domain
    #################################################
    #Background
    cl_bg = 5
    cl = 0.005
    ext = 0.1
    L = 50

    file = open(domain_geo, 'w')
    file.write("cl_bg = %.15f;\n" % (cl_bg))
    file.write("cl = %.15f;\n" % (cl))
    file.write("L = %.15f;\n" % (L))

    file.write("Point(1000) = {L,  0, 0, cl_bg};\n")
    file.write("Point(2000) = {0,  L, 0, cl_bg};\n")
    file.write("Point(3000) = {-L, 0, 0, cl_bg};\n")
    file.write("Point(4000) = {0, -L, 0, cl_bg};\n")
    file.write("Point(5000) = {0,  0, 0, cl_bg};\n")

    file.write("Circle(1) = {2000, 5000, 1000};\n")
    file.write("Circle(2) = {3000, 5000, 2000};\n")
    file.write("Circle(3) = {4000, 5000, 3000};\n")
    file.write("Circle(4) = {1000, 5000, 4000};\n")


    # compute airfoils 
    c, m, p, t = 1.0, 0.09, 0.4, 0.2
    npt = 80
    c_f, m_f, p_f, t_f = 0.2, 0.09, 0.4, 0.2
    npt_f = 20
    x_f, y_f, theta_f = 0.985*c, -0.05*c, 0.0
    airfoil, flap = naca_flap_mesh(c, m, p, t, npt, True, c_f, m_f, p_f, t_f, npt_f, True, x_f, y_f, theta_f)
    n, n_f = airfoil.shape[0], flap.shape[0]

    for i in range(n):
        file.write("Point(%d) = {%.15f,  %.15f, 0.0, cl};\n" % (i+1, airfoil[i,0], airfoil[i,1]))
    for i in range(n_f):
        file.write("Point(%d) = {%.15f,  %.15f, 0.0, cl/2};\n" % (n+1+i, flap[i,0], flap[i,1]))
    
    file.write("Spline(5) = {")
    for i in range(npt-1):
        file.write("%d," %(i+1))
    file.write("%d};\n" %(npt))

    file.write("Spline(6) = {")
    for i in range(npt-1):
        file.write("%d," %(npt+i))
    file.write("%d};\n" %(1))


    file.write("Spline(7) = {")
    for i in range(npt_f-1):
        file.write("%d," %(n+i+1))
    file.write("%d};\n" %(n+npt_f))

    file.write("Spline(8) = {")
    for i in range(npt_f-1):
        file.write("%d," %(n+npt_f+i))
    file.write("%d};\n" %(n+1))


    # Refine mesh with Distance and Threshold
    # We then define a `Threshold' field, which uses the return value of the
    # `Distance' field 1 in order to define a simple change in element size
    # depending on the computed distances

    # SizeMax -                     /------------------
    #                              /
    #                             /
    #                            /
    # SizeMin -o----------------/
    #          |                |    |
    #        Point         DistMin  DistMax

    file.write("Field[1] = Distance;\n")
    file.write("Field[1].CurvesList = {5,6,7,8};\n")
    file.write("Field[1].Sampling = 100;\n")
    # boundary layer
    file.write("Field[2] = Threshold;\n")
    file.write("Field[2].InField = 1;\n")
    file.write("Field[2].SizeMin = cl;\n")
    file.write("Field[2].SizeMax = cl_bg;\n")
    file.write("Field[2].DistMin = 5*cl;\n")
    file.write("Field[2].DistMax = L;\n")
    # flow features
    file.write("Field[3] = Threshold;\n")
    file.write("Field[3].InField = 1;\n")
    file.write("Field[3].SizeMin = 4*cl;\n")
    file.write("Field[3].SizeMax = cl_bg;\n")
    file.write("Field[3].DistMin = 1.0;\n")
    file.write("Field[3].DistMax = L;\n")

    file.write("Field[4] = Min;\n")
    file.write("Field[4].FieldsList = {2, 3};\n")
    file.write("Background Field = 4;\n")




    file.write("Curve Loop(1) = {1, 4, 3, 2};\n" )
    file.write("Curve Loop(2) = {5, 6};\n" )
    file.write("Curve Loop(3) = {7, 8};\n" )
    file.write("Plane Surface(1) = {1, 2, 3};\n" )

    file.write("Extrude {0, 0, %.15f} {Surface{1}; Layers{1};}\n" %(ext))
    file.write("Physical Surface(\"SymmetryFixedSurface\") = {1, 50};\n")
    file.write("Physical Surface(\"OutletFixedSurface\") = {33, 21, 25, 29};\n")
    file.write("Physical Surface(\"StickFixedSurface\") = {41, 37, 49, 45};\n")
    file.write("Physical Volume(\"FluidMesh\") = {1};\n")





if __name__ =='__main__':
    naca_fluid_mesh(domain_geo ='naca_fluid_mesh.geo')
    naca_flap_fluid_mesh(domain_geo ='naca_flap_fluid_mesh.geo')