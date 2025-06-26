from math import sin
from math import cos
from math import inf
from math import radians

# works
def getUnitLateralYieldResistance(f1,f2,dF,t1,t2,fy):
    # (a)
    nuA = f1*dF*t1
    # (b)
    nuB = f2*dF*t2
    # (c)
    nuC = 0.5*f2*dF*t2
    # (d)
    nuD = f1*dF**2*(((1*f2*fy)/(6*(f1+f2)*f1)) ** 0.5 + t1 / (5 * dF))
    # (e)
    nuE = f1*dF**2*(((1*f2*fy)/(6*(f1+f2)*f1)) ** 0.5 + t2 / (5 * dF))
    # (f)
    nuF = f1*dF**2*0.2*(t1/dF+(f2*t2)/(f1*dF))
    # (g)
    nuG = f1*dF**2*((2*f2*fy)/(3*(f1+f2)*f1))**0.5
    nu = min(nuA, nuB, nuC, nuD, nuE, nuF, nuG)
    return nu

# works
def getEmbedmentStrength(material, G, thata, dF, KD, KSF, KT, fu):
    if material == "Wood":
        fiP = 50*G*(1-0.01*dF)
        fiQ = 22*G*(1-0.01*dF)
        fi = (fiP*fiQ)/((fiP*(sin(radians(thata)))**2)+(fiQ*(cos(radians(thata)))**2))*KD*KSF*KT
        return fi
    elif material == "Steel":
        return 3*fu*(0.67/0.8)
    elif material == "Concrete":
        return 125
    else:
        return "ERROR: Material Not Found"

#works
def getYieldingResistance(material, G, thata, dF, KD, KSF, KT, fu, t, fy, ns, nf):
    f = []
    for i in range(len(material)):
        f.append(getEmbedmentStrength(material[i], G[i], thata, dF, KD[i], KSF[i], KT[i], fu[i]))

    nu = inf
    for i in range(len(material)-1):
        i2 = i+1
        nu = min(nu,getUnitLateralYieldResistance(f[i], f[(i2)], dF, t[i], t[(i2)], fy))

    Nr = 0.8 * nu * ns * nf

    return Nr

def getParallelToGrainRowShearResistance(material, nR, fv, Kls, t, nc, acri, KD, KSF, KT):
    PRri = []
    for i in range(len(material)):
        if material[i] == "Wood":
            PRij = []
            for j in range(nR):
                PRij.append(1.2*fv[i]*Kls[i]*t[i]*nc*acri[j])
            PRijmin = min(PRij)
            PRri.append(0.7*PRijmin*nR*KD[i]*KSF[i]*KT[i])
        else:
            PRri.append(0)
    PRrT = sum(PRri)
    print("Parallel To Grain Row Shear Resistance = ", PRrT)
    return PRrT

def getParallelToGrainGroupTearOutResistance(material, nR, fv, Kls, t, nC, acri, Sc, ft, dF, KD, KSF, KT):
    PGri = []
    for i in range(len(material)):
        if material[i] == "Wood":
            PRi1 = 1.2*fv[i]*KD[i]*KSF[i]*KT[i]*Kls[i]*t[i]*nC*acri[0]
            PRinR = 1.2*fv[i]*KD[i]*KSF[i]*KT[i]*Kls[i]*t[i]*nC*acri[nC-1]
            APGi = t[i]*nR*Sc - nR*dF
            PGri.append(0.7*((PRi1+PRinR)/2+ft[i]*KD[i]*KSF[i]*KT[i]*APGi))
    PGrT = sum(PGri)
    print("Parallel To Grain Group Tear-Out Resistance = ", PGrT)
    return PGrT

def getNetTensionResistance(material, typeWood, ft, An, Ag, ftn, ftg, KD, KH, KSt, KT, KZt):
    # ft: from tables 5.3.1A to 5.3.1D, 5.3.2, and 5.3.3
    # An: from clause 4.3.8
    # KZt: from clause 5.4.5
    # ftn: from table 6.3
    # ftg: from table 6.3

    TNri = []
    for i in range(len(material)):
        if material[i] == "Wood":
            if typeWood == "Sawn":
                Ft = ft[i]*KD[i]*KH[i]*KSt[i]*KT[i]
                TNri.append(0.9*Ft*An[i]*KZt[i])
            else:
                Ftn = ftn[i]*KD[i]*KH[i]*KSt[i]*KT[i]
                Ftg = ftg[i]*KD[i]*KH[i]*KSt[i]*KT[i]
                Tr1 = 0.9*Ftn*An[i]
                Tr2 = 0.9*Ftg*Ag[i]
                TNri.append(min(Tr1, Tr2))
    TNrT = sum(TNri)
    print("Net Tension Resistance = ", TNrT)
    return TNrT

def getPerpendicularToGrainSplittingResistance(material, t, w, ep, KD, KSF, KT):
    QSri = []
    for i in range(len(material)):
        if material[i] == "Wood":
            de = w[i]-ep[i]
            QSi = 14*t[i]*(de/(1-de/w[i]))
            QSri.append(0.7*QSi*KD[i]*KSF[i]*KT[i])
    QSrT = sum(QSri)
    print("Perpendicular To Grain Splitting Resistance = ", QSrT)
    return QSrT

# 5.4.5 Exceptions needed to be implemented
def getKZ(w, t, BucklingDirection, L):
    KZt = []
    KZb = []
    KZv = []
    KZcp = []
    KZc  = []
    KZ = []
    for i in range(len(w)):
        if w[i] <= 38:
            KZt.append(1.5)
            KZb.append(1.7)
        elif w[i] <= 64:
            KZt.append(1.5)
            KZb.append(1.7)
        elif w[i] <= 89:
            KZt.append(1.5)
            KZb.append(1.7)
        elif w[i] <= 114:
            KZt.append(1.4)
            if t[i] <= 64:
                KZb.append(1.5)
            elif t[i] <= 102:
                KZb.append(1.6)
            else:
                KZb.append(1.3)
        elif w[i] <= 140:
            KZt.append(1.3)
            if t[i] <= 64:
                KZb.append(1.4)
            elif t[i] <= 102:
                KZb.append(1.5)
            else:
                KZb.append(1.3)
        elif w[i] <= 191:
            KZt.append(1.2)
            if t[i] <= 64:
                KZb.append(1.2)
            elif t[i] <= 102:
                KZb.append(1.3)
            else:
                KZb.append(1.3)
        elif w[i] <= 241:
            KZt.append(1.1)
            if t[i] <= 64:
                KZb.append(1.1)
            elif t[i] <= 102:
                KZb.append(1.2)
            else:
                KZb.append(1.2)
        elif w[i] <= 292:
            KZt.append(1.0)
            if t[i] <= 64:
                KZb.append(1.0)
            elif t[i] <= 102:
                KZb.append(1.1)
            else:
                KZb.append(1.1)
        elif w[i] <= 343:
            KZt.append(0.9)
            if t[i] <= 64:
                KZb.append(0.9)
            elif t[i] <= 102:
                KZb.append(1)
            else:
                KZb.append(1)
        else:
            KZt.append(0.8)
            if t[i] <= 64:
                KZb.append(0.8)
            elif t[i] <= 102:
                KZb.append(0.9)
            else:
                KZb.append(0.9)

        KZv.append(KZb[i])

        KZ.append(1.0)

        ratio = w[i]/t[i]
        if ratio <= 2:
            KZcp.append(1)
        else:
            KZcp.append(1.15)

        if BucklingDirection is None:
            KZc.append(0)
        else:
            if BucklingDirection[i] == "t":
                KZc.append(min(6.3*(t[i]*L[i])**-0.13, 1.3))
            else:
                KZc.append(min(6.3 * (w[i] * L[i]) ** -0.13, 1.3))

    return [KZb, KZv, KZt, KZcp, KZc, KZ]

# from table 6.3, grades need to be implemented
def getFtnFtg(typeWood, species, grade):
    ftn = []
    ftg = []
    for i in range(len(typeWood)):
        if grade[i] is None:
            ftn.append(17.0)
            ftg.append(12.7)
        else:
            if typeWood[i] == "GlueLam":
                if species[i] == "Douglas Fir-Larch":
                    ftn.append(20.4)
                    ftg.append(15.3)
                elif species[i] == "Spruce-Lodgepole Pine-Jack Pine":
                    ftn.append(17)
                    ftg.append(12.7)
                elif species[i] == "Hem-Fir":
                    ftn.append(20.4)
                    ftg.append(15.3)
                else:
                    ftn.append(0)
                    ftg.append(0)
            else:
                ftn.append(0)
                ftg.append(0)
    return [ftn, ftg]

def getParallelToGrainResistance(material, typeWood, species, grade, Ag, t, w, fv, ft, nR, nC, Sc, dF, acri, Kls, KD, KH, KSF, KT, KSt):
    # ft: from tables 5.3.1A to 5.3.1D, 5.3.2, and 5.3.3
    An = []
    for i in range(len(material)):
        An.append(Ag[i] - nR*dF)
    [KZb, KZv, KZt, KZcp, KZc, KZ] = getKZ(w, t, None, None)
    [ftn, ftg] = getFtnFtg(typeWood, species, grade)

    PRrT = getParallelToGrainRowShearResistance(material, nR, fv, Kls, t, nC, acri, KD, KSF, KT)
    PGrT = getParallelToGrainGroupTearOutResistance(material, nR, fv, Kls, t, nC, acri, Sc, ft, dF, KD, KSF, KT)
    TNrT = getNetTensionResistance(material, typeWood, ft, An, Ag, ftn, ftg, KD, KH, KSt, KT, KZt)

    Pr = min(PRrT, PGrT, TNrT)
    return Pr

def getPerpendicularToGrainResistance(material, t, w, ep, KD, KSF, KT):
    Qr = getPerpendicularToGrainSplittingResistance(material, t, w, ep, KD, KSF, KT)
    return Qr

def getG(typeWood, species):
    G = 0
    if typeWood == "GlueLam":
        if species == "Douglas Fir-Larch":
            G = 0.49
        elif species == "Hem-Fir":
            G = 0.46
        elif species == "Spruce-Lodgepole Pine-Jack Pine":
            G = 0.44
    elif typeWood == "Sawn":
        if species == "Douglas Fir-Larch":
            G = 0.49
        elif species == "Hem-Fir":
            G = 0.46
        elif species == "Spruce-Pine-Fir":
            G = 0.42
        elif species == "Northern Species":
            G = 0.35

    return G

def getNr(material, typeWood, species, grade, thata, t, w, fv, ft, nR, nC, Sc, dF, acri, ep, fu, fy, ns, Kls, KD, KH, KSF, KT, KSt):

    G = []
    Ag = []
    nf =nR * nC
    for i in range(len(material)):
        G.append(getG(typeWood[i], species[i]))
        Ag.append(t[i]*w[i])


    Pr = getParallelToGrainResistance(material, typeWood, species, grade, Ag, t, w, fv, ft, nR, nC, Sc, dF, acri, Kls, KD, KH, KSF, KT, KSt)
    Qr = getPerpendicularToGrainResistance(material, t, w, ep, KD, KSF, KT)

    Nr1 = (Pr*Qr)/(Pr*(sin(thata))**2+Qr*(cos(thata))**2)
    print("Nr1: " , Nr1)
    Nr2 = getYieldingResistance(material, G, thata, dF, KD, KSF, KT, fu, t, fy, ns, nf)
    print("Nr2: " , Nr2)

    Nr = min(Nr1, Nr2)
    return Nr

#Test Joint Input

# material list
material = ["Wood", "Steel"]
# type of wood list ("Sawn", "GlueLam")
typeWood = ["GlueLam", None]
# Species of wood list
species = ["Spruce-Lodgepole Pine-Jack Pine", None]
# Grade of wood list
grade = [None, None]
# Angle of force to grain of wood
thata = 45

# Thickness of Material List
t = [38.1, 3.175]
# Width of Material List
w = [101.6 , 50.8]

# Number of faseners in each row (num of columb)
nC = 1
# Number of rows
nR = 3
#Sc
Sc = 1
# Diameter of Fasteners
dF = 9.525

#fv
fv = [1.5,1.5]
#ft
ft = [1,1]

#acri
acri= [101.6, 101.6, 101.6]
#ep
ep = [1,1]
#fu: Tensile Strength of steel members (380 MPa normally)
fu = [None,380]
#fy: Yield strength of fastener
fy = 751
#ns: Number of shear planes
ns = 1

#kls
Kls = [1,1]
#kD
KD = [1,1]
#KH
KH = [1,1]
#KSF
KSF = [1,1]
#KT
KT = [1,1]
#KSt
KSt = [1,1]

Nr = getNr(material, typeWood, species, grade, thata, t, w, fv, ft, nR, nC, Sc, dF, acri, ep, fu, fy, ns, Kls, KD, KH, KSF, KT, KSt)

print(" ")
print("Joint Resistance = " , Nr, " N")






