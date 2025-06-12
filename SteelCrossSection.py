
def getA(memberType, d, b, t, w):
    A = 0
    if memberType == "I":
        A = 2*b*t+(d-2*t)*w
    return A

def getI(memberType, axis, d, b, t, w):
    I = 0
    if memberType == "I":
        if axis == "x":
            I = 1/12*(b*d**3-(b-w)*(d-2*t)**3)
        else:
            I = 1/12*(2*t*b**3+(d-2*t)*w**3)
    return I

def getS(memberType, Axis, d, b, t, w):
    S = 0
    if memberType == "I":
        if Axis == "x":
            S = 1/(6*d)*(b*d**3-(b-w)*(d-2*t)**3)
        else:
            S = 1/(6*d)*(2*t*b**3+(d-2*t)*w**3)
    return S

def getZ(memberType, Axis, d, b, t, w):
    Z = 0
    if memberType == "I":
        if Axis == "x":
            Z = 1/4*(b*d**3-(b-w)*(d-2*t)**3)
        else:
            Z  = 1/4*(2*t*(b**2-w**2)+d*w**2)
    return Z

def getJ(memberType, d, b, t, w):
    J = 0
    if memberType == "I":
        J = 1/3*(2*b*t**3+(d-t)*w**3)
    return J

def getCw(memberType, d, b, t, w):
    Cw = 0
    if memberType == "I":
        Cw = 1/24*(d-t)**2*b**3*t
    return Cw

def getr(memberType, Axis, I, A):
    r = 0
    if memberType == "I":
        if Axis == "x":
            r=(I/A)**0.5
        else:
            r=(I/A)
    return r

def getAxisO(memberType, Axis):
    AxisO = 0
    if memberType == "I":
        AxisO = 0
    return AxisO

def getCrossSectionProperties(memberType, d, b, t, w):
    A = getA(memberType, d, b, t, w)
    Ix = getI(memberType, "x", d, b, t, w)
    Iy = getI(memberType, "y", d, b, t, w)
    Sx = getS(memberType, "x", d, b, t, w)
    Sy = getS(memberType, "y", d, b, t, w)
    Zx = getZ(memberType, "x", d, b, t, w)
    Zy = getZ(memberType, "y", d, b, t, w)
    J = getJ(memberType, d, b, t, w)
    Cw = getCw(memberType, d, b, t, w)
    rx = getr(memberType, "x", Ix, A)
    ry = getr(memberType, "y", Iy, A)
    xo = getAxisO(memberType, "x")
    yo = getAxisO(memberType, "y")

    return A, Ix, Iy, Sx, Sy, Zx, Zy, J, Cw, rx, ry, xo, yo
