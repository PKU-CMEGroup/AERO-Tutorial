import math 
import numpy as np
import matplotlib.pyplot as plt
# http://airfoiltools.com/airfoil/naca4digit
# https://en.wikipedia.org/wiki/NACA_airfoil
# c : chord length (default 1)
# m : (0.0, 0.095) the amount of camber as a fraction of chord length
# p : (0.0, 0.9) the location of maximum camber as a fraction of chord length
# t : (0.01, 0.4) thickness as a fraction of chord length
####################### Example: 4 digital NACA_2412 ################
# The leading '2' indicates maximum camber is 2% of chord length
# The '4' indicates maximum camber is at 40% of the chord length
# The '12' indicates maximum thickness is 12% of the chord length
#####################################################################

def rotate(points, theta, x=0.0, y=0.0):
    # rotate the flap around the leading point (0,0), then move the flap
    points[:,0], points[:,1] =  points[:,0]*np.cos(theta*np.pi/180) + points[:,1]*np.sin(theta*np.pi/180) + x, \
        -points[:,0]*np.sin(theta*np.pi/180) + points[:,1]*np.cos(theta*np.pi/180) + y
    return points

def camberLine(x, c, m, p):
    # x : location
    # return : y
    # the camber line is (x, y), connecting (0, 0) and (c, 0)
    # the maxium camber line is at (pc, mc)
    if (x < p * c):
        return m * x / (p * p) * (2 * p - x / c)
    else:
        p1 = 1 - p
        return m * (c - x) / (p1 * p1) * (1 + x / c - 2 * p)



def camberLineSlope(x, c, m, p):
    if (x < p * c):
        return 2 * m / (p * p) * (p - x / c)
    else:
        p1 = 1 - p
        return 2 * m / (p1 * p1) * (p - x / c)




def thickness(x, c, t, closed_trailing_edge):
    # thickness needs to be applied perpendicular to the camber line
    # this is half thickness of the airfoil at location x
    u = x / c
    a0, a1, a2, a3, a4 = 0.2969, -0.1260, -0.3516, 0.2843, -0.1015
    if closed_trailing_edge: 
        a4 = -0.1036
    return 5.0*t*c*(a0*math.sqrt(u) + a1*u + a2*u**2 + a3*u**3 + a4*u**4)



def leadingEdgeRadius(t, c):
    return 1.1019 * t * t * c



def evaluate(x, c, m, p, t, closed_trailing_edge):
    yc = camberLine(x, c, m, p)
    yt = thickness(x, c, t, closed_trailing_edge)
    dycdx = camberLineSlope(x, c, m, p)
    dscdx = math.sqrt(1 + dycdx * dycdx)
    ctheta = 1 / dscdx
    stheta = dycdx / dscdx

    return [
    x - yt * stheta,   #  upper surface xU
    yc + yt * ctheta,  #  upper surface yU
    x + yt * stheta,   #  lower surface xL
    yc - yt * ctheta   #  lower surface yL
    ]




def naca_mesh(c, m, p, t, npt, closed_trailing_edge):
    # from the leading edge to trailing edge along the upper surface 
    # then back to the leading edge along the lower surface (not include leading edge)
    x = c/2.0 * (1.0 - np.cos(np.linspace(0, np.pi, npt)))
    yc, shape = np.zeros(npt), np.zeros((npt, 4))
    
     # xU, yU, xL, yL
    for i in range(npt):
        yc[i] = camberLine(x[i], c, m, p)
        shape[i,:] = evaluate(x[i], c, m, p, t, closed_trailing_edge)

    if closed_trailing_edge:
        return np.vstack((shape[:,0:2], shape[-2:0:-1,2:4])), x, yc
    else:
        return np.vstack((shape[:,0:2], shape[-1:0:-1,2:4])), x, yc
    
def naca_flap_mesh(c, m, p, t, npt, closed_trailing_edge, 
                   c_f, m_f, p_f, t_f, npt_f, closed_trailing_edge_f,
                   x_f, y_f, theta_f):
    # from the leading edge to trailing edge along the upper surface 
    # then back to the leading edge along the lower surface (not include leading edge)
    # theta_f is the rotation angle in clockwise
    shape, _, _ = naca_mesh(c, m, p, t, npt, closed_trailing_edge)
    shape_f, _, _ = naca_mesh(c_f, m_f, p_f, t_f, npt_f, closed_trailing_edge_f)

    # rotate the flap around the leading point (0,0), then move the flap
    shape_f =  rotate(shape_f, theta_f, x_f, y_f)
    
    
    return shape, shape_f
    



if __name__ == "__main__":
    c, m, p, t = 1.0, 0.09, 0.4, 0.2
    npt = 20
    
    fig, axs = plt.subplots(2, 1, figsize=(15, 5), sharex=True, sharey=True)
    shape, x, yc = naca_mesh(c, m, p, t, npt, False)
    axs[0].plot(x, yc, color="red")
    axs[0].plot(shape[:,0], shape[:,1], "-o", color="grey",  markersize=3)
    axs[0].set_ylabel("open trailing edge")
    shape, x, yc = naca_mesh(c, m, p, t, npt, True)
    axs[1].plot(x, yc, color="red")
    axs[1].plot(shape[:,0], shape[:,1], "-o", color="grey",  markersize=3)
    axs[1].set_ylabel("closed trailing edge")
    fig.savefig("NACA_4digit.pdf")
    plt.show()



    c, m, p, t = 1.0, 0.09, 0.6, 0.3
    npt = 80
    c_f, m_f, p_f, t_f = 0.25, 0.09, 0.2, 0.2
    npt_f = 20

    fig, axs = plt.subplots(2, 1, sharex=True)
    
    x_f, y_f, theta_f = 0.99*c, -0.05*c, 5.0
    shape, shape_f = naca_flap_mesh(c, m, p, t, npt, True, c_f, m_f, p_f, t_f, npt_f, True, x_f, y_f, theta_f)
    
    axs[0].plot(shape[:,0], shape[:,1], "-o", color="grey",  markersize=3)
    axs[0].plot(shape_f[:,0], shape_f[:,1], "-o", color="grey",  markersize=3)
    axs[0].set_ylabel(f"angle={theta_f}")
    axs[0].set_aspect('equal')
    

    theta_f = 40.0
    shape, shape_f = naca_flap_mesh(c, m, p, t, npt, True, c_f, m_f, p_f, t_f, npt_f, True, x_f, y_f, theta_f)
    axs[1].plot(shape[:,0], shape[:,1], "-o", color="grey",  markersize=3)
    axs[1].plot(shape_f[:,0], shape_f[:,1], "-o", color="grey",  markersize=3)
    axs[1].set_ylabel(f"angle={theta_f}")
    axs[1].set_aspect('equal')
    
    fig.tight_layout()
    fig.savefig("NACA_flap.pdf")
    plt.show()


    