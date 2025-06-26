from math import pi
#http://www.labciv.eng.uerj.br/pgeciv/files/Torsion%20Properties.pdf
def getA(memberType, d, b, t, w):
    A = 0
    if memberType == "I":
        A = 2*b*t+(d-2*t)*w
    elif memberType == "HSS":
        b1 = b-2*t
        d1 = d-2*t
        A = 2*b*d-b1*d1
    elif memberType == "Pipe":
        d1 = d-2*t
        A = pi*(d**2-d1**2)/4
    elif memberType == "T":
        A = b*t+w*(d-t)
    return A

def getI(memberType, axis, A, d, b, t, w):
    I = 0
    if memberType == "I":
        if axis == "x":
            I = 1/12*(b*d**3-(b-w)*(d-2*t)**3)
        else:
            I = 1/12*(2*t*b**3+(d-2*t)*w**3)
    elif memberType == "HSS":
        b1 = b - 2 * t
        d1 = d - 2 * t
        if axis == "x":
            I = 1/12*(b*d**3-b1*d1**3)
        else:
            I = 1/12*(d*b**3-d1*b1**3)
    elif memberType == "Pipe":
        d1 = d - 2 * t
        I = pi*(d**4-d1**4)/64
    elif memberType == "T":
        if axis == "x":
            I = 1/12*(b*t**3+w*(d-t)**3+(3*b*w*t*d**2*(d-t))/A)
        else:
            I = 1/12*(t*b**3+(d-t)*w**3)
    return I

def getS(memberType, axis, A, I, d, b, t, w):
    S = 0
    if memberType == "I":
        if axis == "x":
            S = 1/(6*d)*(b*d**3-(b-w)*(d-2*t)**3)
        else:
            S = 1/(6*d)*(2*t*b**3+(d-2*t)*w**3)
    elif memberType == "HSS":
        b1 = b - 2 * t
        d1 = d - 2 * t
        if axis == "x":
            S = 1/(6*d)*(b*d**3-b1*d1**3)
        else:
            S = 1/(6*b) * (d * b ** 3 - d1 * b1 ** 3)
    elif memberType == "Pipe":
        d1 = d - 2 * t
        S = pi*(d**4-d1**4)/(32*d)
    elif memberType == "T":
        if axis == "x":
            y = 1/2*(b*d*t/A+d-t)
            S = min(I/y, I/(d-y))
        else:
            S = 2*I/b
    return S

def getZ(memberType, axis, A, d, b, t, w):
    Z = 0
    if memberType == "I":
        if axis == "x":
            Z = 1/4*(b*d**3-(b-w)*(d-2*t)**3)
        else:
            Z  = 1/4*(2*t*(b**2-w**2)+d*w**2)
    elif memberType == "HSS":
        b1 = b - 2 * t
        d1 = d - 2 * t
        if axis == "x":
            Z = 1/4*(b*d**2-b1*d1**2)
        else:
            Z = 1/4*(d*b**2-d1*b1**2)
    elif memberType == "Pipe":
        d1 = d - 2 * t
        Z = 1/6*(d**3-d1**3)
    elif memberType == "T":
        if axis == "x":
            if t<=A/(2*b):
                Z = w*(d-t)**2/4+b*d*t/2-b**2*t**2/(4*w)
            else:
                Z = w*d**2/2+b*t**2/4-d*t*w/2-(d-t)**2*w**2/(4*b)
        else:
            Z = t*b**2/4+(d-t)*w**2/4
    return Z

def getJ(memberType, I,  d, b, t, w):
    J = 0
    if memberType == "I":
        J = 1/3*(2*b*t**3+(d-t)*w**3)
    elif memberType == "HSS":
        Rc = 1.5*t
        Ap = (d-t)*(b-t)-Rc**2*(4-pi)
        p = 2*((d-t)+(b-t))-2*Rc*(4-pi)
        J = 4*Ap**2*t/p
    elif memberType == "Pipe":
        J = 2*I
    elif memberType == "T":
        J = 1/3*(b*t**3+(d-t/2)*w**3)
    return J

def getCw(memberType, d, b, t, w):
    Cw = 0
    if memberType == "I":
        Cw = 1/24*(d-t)**2*b**3*t
    elif memberType == "HSS" or memberType == "Pipe":
        Cw = 0
    elif memberType == "T":
        Cw = (b**3*t**3)/144+((d-t/2)**3*w**3)/36
    return Cw

def getr(memberType, axis, I, A, b, d, t, w):
    r = 0
    if memberType == "I":
        r=(I/A)**0.5
    elif memberType == "HSS":
        b1 = b - 2 * t
        d1 = d - 2 * t
        if axis == "x":
            r = ((b*d**3-b1*d1**3)/(12*A))**0.5
        else:
            r = ((d*b**3-d1*b1**3)/(12*A))**0.5
    elif memberType == "Pipe":
        d1 = d - 2 * t
        r = (d**2+d1**2)**0.5/4
    elif memberType == "T":
        r = (I/A)**0.5
    return r

def getAxisO(memberType, Axis):
    AxisO = 0
    if memberType == "I" or memberType == "HSS" or memberType == "Pipe" or memberType == "T":
        AxisO = 0
    return AxisO

def getCrossSectionProperties(memberType, d, b, t, w):
    A = getA(memberType, d, b, t, w)
    Ix = getI(memberType, "x", A, d, b, t, w)
    Iy = getI(memberType, "y", A, d, b, t, w)
    Sx = getS(memberType, "x", A, Ix, d, b, t, w)
    Sy = getS(memberType, "y", A, Iy, d, b, t, w)
    Zx = getZ(memberType, "x", A, d, b, t, w)
    Zy = getZ(memberType, "y", A, d, b, t, w)
    J = getJ(memberType, Ix, d, b, t, w)
    Cw = getCw(memberType, d, b, t, w)
    rx = getr(memberType, "x", Ix, A, d, b, t, w)
    ry = getr(memberType, "y", Iy, A, d, b, t, w)
    xo = getAxisO(memberType, "x")
    yo = getAxisO(memberType, "y")
    NumSymetry = 0
    if memberType == "I" or memberType == "HSS" or memberType == "Pipe":
        NumSymetry = 2
    elif memberType == "T":
        NumSymetry = 1

    return NumSymetry, A, Ix, Iy, Sx, Sy, Zx, Zy, J, Cw, rx, ry, xo, yo
