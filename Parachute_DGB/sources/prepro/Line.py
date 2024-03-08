import sys
import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
'''
solve for a catenary curve pass xm, ym

y(x) = ym + a * (cosh((x - xm) / a) - 1.)

'''
def standard_catenary_prime(a, s, h, v):
    # s, h, v = data
    return - 2 * np.sinh(h / (2 * a)) + h/a*np.cosh(h/(2*a))

def standard_catenary(a, s, h, v):
    #s, h, v = data
    return np.sqrt(s*s - v*v) - 2*a*np.sinh(h/(2*a))

def standard_catenary_b_prime(b, s, h, v):
    # s, h, v = data
    t1 = (1./(2.*b)*np.cosh(1./(2.*b)) - np.sinh(1./(2*b)))
    t2 = (2.*b*np.sinh(1./(2.*b)) - 1.)
    return -t1/((np.sqrt(t2))**3)

def standard_catenary_b(b, s, h, v):
    #s, h, v = data
    t1 = 1. / np.sqrt(np.sqrt(s * s - v * v) / h - 1.)
    t2 = 1./np.sqrt(2*b*np.sinh(1/(2.*b)) - 1)
    return t1 - t2

def shift_catenary_prime(xm, a, x1, y1, x2, y2):
    return np.sinh((x2 - xm)/a) -  np.sinh((x1 - xm)/a)

def shift_catenary(xm, a, x1, y1, x2, y2):
    return (y2 - a*(np.cosh((x2 - xm)/a) - 1.0)) -  (y1 - a*(np.cosh((x1 - xm)/a) - 1.0))

def catenary(x1, y1, x2, y2 , s):
    '''

    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :param s:
    :return:
    '''
    if x1 > x2:
        x1, y1 , x2, y2 = x2, y2, x1, y1
    h, v = x2 - x1, y2 - y1

    succeed = False
    a0 = h
    a, infodict, ler, mesg = fsolve(standard_catenary, a0, (s, h, v), fprime=standard_catenary_prime, full_output=1)
    print(a)
    a = a[0]
    if a < 0:
        a = -a
    res = standard_catenary(a, s, h, v)
    if (ler == 1 and abs(res) < 1.e-10):
        succeed = True
    if not succeed:
        b0 = (2 * np.sqrt(6.) * np.sqrt(np.sqrt(s * s - v * v) / h - 1.))
        b, infodict, ler, mesg = fsolve(standard_catenary_b, b0, (s, h, v), fprime=standard_catenary_b_prime,
                                        full_output=1)
        b = b[0]
        if b < 0:
            b = -b
        res = standard_catenary_b(b, s, h, v)
        if (ler == 1 and abs(res) < 1.e-10):
            succeed = True
            a = b * h

    if not succeed:
        print('****ERROR Catenary solver failed, x1 ', x1, ' y1 ', y1, ' x2 ', x2, ' y2 ', y2, ' s ', s)
    xm, infodict, ler, mesg = fsolve(shift_catenary   , (x1 + x2)/2., (a, x1, y1, x2, y2), fprime=shift_catenary_prime, full_output=1)
    xm = xm[0]
    res = shift_catenary(xm, a, x1, y1, x2, y2)
    if (ler != 1 or abs(res) > 1.e-10):
        print('xm is ', xm, ' res is ', res)
    ym = y1 - a*(np.cosh((x1 - xm)/a) - 1.0)

    return a, xm, ym

def point_on_catenary(x1, y1, x2, y2, a, xm, ym, s, ds):
    '''

    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :param s:
    :param ds: distance from x1
    :return:
    '''


    if x1 < x2:
        # a * np.sinh((xs - xm) / a) - a * np.sinh((x1 - xm) / a) = ds
        xs = a*np.arcsinh(ds/a + np.sinh((x1 - xm) / a)) + xm
        ys = a*(np.cosh((xs - xm)/a) - 1.0) + ym

    else:
        # a * np.sinh((xs - xm) / a) - a * np.sinh((x1 - xm) / a) = ds
        xs = a * np.arcsinh((s - ds)/a + np.sinh((x2 - xm) / a)) + xm
        ys = a * (np.cosh((xs - xm) / a) - 1.0) + ym

    return xs, ys


def _line_to_circle_func(theta, ratio):
    return ratio*theta - 2*np.sin(theta/2.)

def _line_to_circle_func_prime(theta, ratio):
    return ratio - np.cos(theta/2.)

def _line_to_circle_b_func(theta, ratio):
    return ratio - 2*np.sin(theta/2.)/theta

def _line_to_circle_func_b_prime(theta, ratio):
    return -np.cos(theta/2.)/theta + 2*np.sin(theta/2.)/(theta**2)

def line_to_circle(arc_len, chord_len):
    #solve for r and theta
    #arc_len = r theta
    #chord_len = 2 sin(theta/2) r
    ratio = chord_len/arc_len
    succeed = False
    theta, infodict, ler, mesg = fsolve(_line_to_circle_func, np.pi , (ratio), fprime=_line_to_circle_func_prime, full_output=1)
    res = _line_to_circle_func(theta, ratio)
    if (ler == 1 and res < 1.e-10 and abs(theta) > 1.e-10):
        succeed = True
    else:
        theta, infodict, ler, mesg = fsolve(_line_to_circle_b_func, np.pi , (ratio), fprime=_line_to_circle_func_b_prime, full_output=1)
        res = _line_to_circle_b_func(theta, ratio)
        if (ler == 1 and res < 1.e-10 and abs(theta) > 1.e-10):
            succeed = True

    if not succeed:
        print('****ERROR line_to_cirle failed, ratio is ', ratio, ' theta is ', theta)
    theta = theta[0]
    if theta < 0:
        theta = -theta

    r = arc_len/theta
    return theta , r

def point_on_circle(x1, y1, x2, y2, theta, r, s, ds):
    '''

    :param x1: start
    :param y1:
    :param x2: end
    :param y2:
    :param s:
    :param ds: distance from x1
    :return:
    '''
    assert (abs(x1 - x2) < 1.e-10)
    assert (abs(y1 + y2) < 1.e-10)
    if theta < 1.e-10:
        xs = (1. - ds/s)*x1 + ds/s*x2
        ys = (1. - ds/s)*y1 + ds/s*y2
    else:
        circle_x = (x1 + x2)/2. - r*np.cos(theta/2.)

        if y1 < y2:
            d_theta = ds/r
        else:
            d_theta = theta - ds/r
        xs = circle_x + r*np.cos(-theta/2. + d_theta)
        ys = r*np.sin(-theta/2. + d_theta)

    return xs, ys


if __name__ == '__main__':
    test_catenary = True
    if test_catenary:
        r1, z1 = 0., 0.
        r2, z2 = 0.575303360777  ,  0.538488665692

        P1, P2 = np.array([r1, z1]), np.array([r2, z2])
        s = 0.788


        h, v = abs(r2 - r1), z2 -z1

        eps = 1.e-3
        a = h/2.0
        b = a/h
        print('standard_catenary ', ((standard_catenary(b + eps, s, h, v) - standard_catenary(b - eps, s, h, v))/(2*eps) - standard_catenary_prime(b, s, h, v)))
        xm = -0.5
        print('shift_catenary ', ((shift_catenary(xm + eps, a, r1, z1, r2, z2) - shift_catenary(xm - eps, a, r1, z1, r2, z2)) / (2 * eps) - shift_catenary_prime(xm, a, r1, z1, r2, z2)))
        a, xm, ym = catenary(r1, z1, r2, z2, s)


        xx = np.linspace(min(r1, r2), max(r1,r2), 100)
        yy = a*(np.cosh((xx - xm)/a) - 1.0) + ym

        print(point_on_catenary(r1, z1, r2, z2, a, xm, ym, s, s))

        plt.plot([r1, r2], [z1, z2])
        plt.plot(xx, yy)
        plt.show()
    test_circle = False
    if test_circle:
        eps = 1.e-3
        arc, chord = 1., 1.0
        ratio = chord/arc
        theta = 0.3
        print('line_to_circle_func ', (
        (_line_to_circle_func(theta + eps, ratio) - _line_to_circle_func(theta - eps, ratio)) / (2 * eps) - _line_to_circle_func_prime(theta, ratio)))

        print('line_to_circle_b_func ', (
            (_line_to_circle_b_func(theta + eps, ratio) - _line_to_circle_b_func(theta - eps, ratio)) / (
            2 * eps) - _line_to_circle_func_b_prime(theta, ratio)))

        h = 1.0
        x1, y1 = h + 1.0, -1.0
        x2, y2 = h + 1.0, 1.0
        arc = np.pi/np.sqrt(2.0)
        chord = abs(y1 - y2)
        theta, r = line_to_circle(arc, chord)
        print(theta, ' ', r)
        ds = arc

        print(point_on_circle(x1, y1, x2, y2, theta, r, arc, ds))

        h = 0.0
        x1, y1 = h + 1.0, -1.0
        x2, y2 = h + 1.0, 1.0
        arc = 2.0
        chord = abs(y1 - y2)
        theta, r = line_to_circle(arc, chord)
        print(theta, ' ', r)
        ds = arc/4.0

        print(point_on_circle(x1, y1, x2, y2, theta, r, arc, ds))

