from math import pi
from math import acos
from math import cos
from math import inf

E = 200000
G = 77000
Fy = 210
Fu = 380
n = 1.34

def setSteelProperties(Eset, Gset, Fyset, Fuset, coldFormed):
    global E, G, Fy, Fu, n
    E = Eset
    G = Gset
    Fy = Fyset
    Fu = Fuset

    if coldFormed:
        n = 1.34
    else:
        n = 2.24

def getNumSymmetry(memberType):
    if memberType == "Angle":
        return 0
    elif memberType == "T":
        return 1
    else:
        return 2

def getQubicRoots(a,b,c,d):

    p = c-b^2/3
    q = d-(b*c)/3+(2*b^3)/27
    Delta = -4*p^3-27*q^2

    if Delta == 0:
        r1 = (-4*q)^(1/3)-b/3
        r2 = (q/2)^(1/3)-b/3
        r3 = r2
    elif Delta < 0:
        z1 = (-q/2+((p/3)^3+(q/2)^2)^0.5)^(1/3)
        z2 = (-q/2-((p/3)^3+(q/2)^2)^0.5)^(1/3)
        r1 = z1+z2-b/3
        r2 = inf
        r3 = inf
    else:
        thata = 1/3*acos(-q/2*(3/-p)^(3/2))
        r1 = 2*(-p/3)^0.5*cos(thata)-b/3
        r2 = 2*(-p/3)^0.5*cos(thata+2*pi/3)-b/3
        r3 = 2*(-p/3)^0.5*cos(thata+4*pi/3)-b/3

    return r1, r2, r3

def getFe(numSymmetry, K, L, rx, ry, xo, yo, A, J, Cw):
    ro2 = xo ^ 2 + yo ^ 2 + rx ^ 2 + ry ^ 2

    Fex = ((pi) ^ 2) * E / (K * L.rx)
    Fey = ((pi) ^ 2) * E / (K * L.ry)
    Fez = (((pi) ^ 2 * E * Cw) / (K * L) ^ 2 + G * J) * 1 / A * ro2

    if numSymmetry == 2:
        return min(Fex, Fey, Fez)
    elif numSymmetry == 1:
        ohm = 1 - (xo ^ 2 + yo ^ 2 / ro2)
        Feyz = (Fey + Fez)/(2*ohm)*(1-(1-(4*Fey*Fez*ohm)/(Fey+Fez)^2)^0.5)
        return min(Fex, Feyz)
    else:
        a = 1-xo^2/ro2-yo^2/ro2
        b = Fey*(xo^2/ro2)+Fex*(yo^2/ro2)-Fex-Fey-Fez
        c = Fey*Fez+Fex*Fez+Fex*Fey
        d = -1*Fex*Fey*Fez

        [r1,r2,r3] = getQubicRoots(a,b,c,d)
        Fe = min(r1,r2,r3)
        return Fe


def getCompressionResistance(numSymmetry, K, L, rx, ry, xo, yo, A, J, Cw):
    Fe = getFe(numSymmetry,E,G,K,L,rx,ry,xo,yo,A,J,Cw)
    Lambda = (Fy/Fe)^0.5
    Cr = 0.9*A*Fy/(1+Lambda^(2*n))^(1/n)
    return Cr

# Ag: Gross Area
def getTensionResistance(Ag):
    Tr = 0.9*Ag*Fy
    return Tr

#Aw: Shear Area (dw for rolled shapes and hw for girders, 2ht for rectangular HSS
#h:web depth
#w:
#stiffenedWeb: is there stiffeners
#a: (distance between stiffeners)
def getShearResistance(Aw, h, w, stiffenedWeb, a):
    if stiffenedWeb:

        if a/h<1:
            kv = 4+5.34/(a/h)^2
        else:
            kv = 5.34 + 4/(a/h)^2

        Fcri = 290*(Fy*kv)^0.5/(h/w)
        Fcre = (180000*kv)/(h/w)^2
        ka = 1/(1+(a/h)^2)^0.5

        if h/w <= 439*(kv/Fy)^0.5:
            Fs = 0.66*Fy
        elif 439*(kv/Fy)^0.5 < h/w & h/w <= 502*(kv/Fy)^0.5:
            Fs = Fcri
        elif 502*(kv/Fy)^0.5 < h/w & h/w <= 621*(kv/Fy)^0.5:
            Fs = Fcri + ka*(0.5*Fy-0.866*Fcri)
        else:
            Fs = Fcre + ka*(0.5*Fy-0.866*Fcre)
    else:
        if h/w <= 1014/Fy^0.5:
            Fs = 0.66*Fy
        elif 1014/Fy^0.5 < h/w & h/w <= 1435/Fy^0.5:
            Fs = (670*Fy^0.5)/(h/w)
        else:
            Fs = 961200/(h/w)^2

    Vr = 0.9*Aw*Fs
    return Vr

def getBendingResistanceLaterallySupported(bClass, Z, S):

    if bClass == 1 | bClass == 2:
        Mr = 0.9*Z*Fy
    else:
        Mr = 0.9*S*Fy

def getBendingResistanceLaterallyUnSupported(bClass, axisBending, memberType, numSymmetry, L, Z, S, Iy, Ix, J, Cw, b, t, h, w, d, Mmax, Ma, Mb, Mc):
    w2 = (4*Mmax)/(Mmax^2+4*Ma^2+7*Mb^2+4*Mc^2)^0.5
    if w2>2.5:
       w2 = 2.5

    Mu = w2*pi/L*(E*Iy*G*J+(pi*E/L)^2*Iy*Cw)^0.5

    if numSymmetry == 2:
        if bClass == 1 | bClass == 2:
            if memberType == "ClosedSquare" or memberType == "CircularSection":
                Mr = 0.9*Z*Fy
            else:
                if Mu > 0.67*Z*Fy:
                    Mr = 1.15*0.9*Z*Fy*(1-0.28*Z*Fy/Mu)
                    if Mr > 0.9*Z*Fy:
                        Mr = 0.9*Z*Fy
                else:
                    Mr = 0.9*Mu
        else:
            if memberType == "ClosedSquare" or memberType == "CircularSection":
                Mr = 0.9 * S * Fy
            else:
                if Mu > 0.67 * S * Fy:
                    Mr = 1.15 * 0.9 * S * Fy * (1 - 0.28 * S * Fy / Mu)
                    if Mr > 0.9 * S * Fy:
                        Mr = 0.9 * S * Fy
                else:
                    Mr = 0.9 * Mu
    elif numSymmetry == 1:
        Myr = 0.7*S*Fy
        if Mu > Myr:
            Lyr = 0
            rt = b/(12*(1+h*w/(3*b*t)))
            Lu = 1.1*rt*(E/Fy)^0.5

            if bClass == 1 | bClass == 2:
                if memberType == "T":
                    Mr = 0.9 * (S * Fy - (S * Fy - Myr) * ((L - Lu) / (Lyr - Lu)))
                    if Mr > 0.9 * S * Fy:
                        Mr = 0.9 * S * Fy
                else:
                    Mr = 0.9*(Z*Fy-(Z*Fy-Myr)*((L-Lu)/(Lyr-Lu)))
                    if Mr > 0.9*Z*Fy:
                        Mr = 0.9*Z*Fy
            else:
                Mr = 0.9 * (S * Fy - (S * Fy - Myr) * ((L - Lu) / (Lyr - Lu)))
                if Mr > 0.9 * S * Fy:
                    Mr = 0.9 * S * Fy
        else:
            Bx = 0.9*(d-t)*(1-(Iy/Ix)^2)
            Mu = w2*pi^2*E*Iy/(2*L^2)*(Bx+(Bx^2+4*(G*J*L^2/(pi^2*E*Iy)+Cw/Iy))^0.5)
            Mr = 0.9*Mu