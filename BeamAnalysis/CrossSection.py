#
# HSS Combined Sections
#

class HSS:
    def __init__(self, d, w, t, A, M, Ix, Iy, Sx, Sy, rx, ry, Zx, Zy, J):
        self.d = d
        self.w = w
        self.t = t
        self.A = A
        self.M = M
        self.Ix = Ix
        self.Iy = Iy
        self.Sx = Sx
        self.Sy = Sy
        self.rx = rx
        self.ry = ry
        self.Zx = Zx
        self.Zy = Zy
        self.J = J

def getCentroid(ListSections, ListRotations):
    listDistances = []
    distUpTo = 0
    listDistToCentroid = []

    for i in range(len(ListSections)):
        if ListRotations[i] == "X":
            listDistances.append(ListSections[i].d / 2 + distUpTo)
            distUpTo += ListSections[i].d
        elif ListRotations[i] == "Y":
            listDistances.append(ListSections[i].w / 2 + distUpTo)
            distUpTo += ListSections[i].w
    Numerator = 0
    Denominator = 0
    for i in range(len(ListSections)):
        Numerator += ListSections[i].A * listDistances[i]
        Denominator += ListSections[i].A
    Centroid = Numerator / Denominator

    for i in range(len(ListSections)):
        if ListRotations[i] == "X":
            listDistToCentroid.append(abs(Centroid - listDistances[i]))
        elif ListRotations[i] == "Y":
            listDistToCentroid.append(abs(Centroid - listDistances[i]))
    return Centroid, listDistToCentroid, Denominator


def getICombineStrong(ListSections, ListRotations, listDistToCentroid):
    I = 0
    for i in range(len(ListSections)):
        if ListRotations[i] == "X":
            I += ListSections[i].Ix + ListSections[i].A * listDistToCentroid[i] ** 2
        elif ListRotations[i] == "Y":
            I += ListSections[i].Iy + ListSections[i].A * listDistToCentroid[i] ** 2
    return I


def getICombineWeek(ListSections, ListRotations):
    I = 0
    for i in range(len(ListSections)):
        if ListRotations[i] == "X":
            I += ListSections[i].Iy
        elif ListRotations[i] == "Y":
            I += ListSections[i].Ix
    return I


def getSStrong(ListSections, ListRotations, I):
    x = 0
    for i in range(len(ListSections)):
        if ListRotations[i] == "X":
            x += ListSections[i].d
        elif ListRotations[i] == "Y":
            x += ListSections[i].w
    S = 2 * I / x
    return S, x


def getSWeek(ListSections, ListRotations, I):
    y = 0
    for i in range(len(ListSections)):
        if ListRotations[i] == "X":
            y += ListSections[i].w
        elif ListRotations[i] == "Y":
            y += ListSections[i].d
    S = 2 * I / y
    return S, y


def getM(ListSections):
    M = 0
    for i in range(len(ListSections)):
        M += ListSections[i].M
    return M


def getr(A, Ix, Iy):
    rx = (Ix / A) ** 0.5
    ry = (Iy / A) ** 0.5
    return rx, ry


def getZStrong(ListSections, ListRotations, ListDistToCentroid):
    iSplit = None
    for i in range(len(ListSections)):
        if ListRotations[i] == "X":
            if ListSections[i].d / 2 < ListDistToCentroid[i]:
                iSplit = i
                break
        if ListRotations[i] == "Y":
            if ListSections[i].w / 2 < ListDistToCentroid[i]:
                iSplit = i
                break

    Z = 0
    if iSplit is not None:
        if ListRotations[iSplit] == "X":
            offSet = ListSections[iSplit].d / 2 - ListDistToCentroid[iSplit]
            if abs(offSet) < ListSections[iSplit].d / 2 - ListSections[iSplit].t:
                offSetArea = offSet * 2 * ListSections[iSplit].t
            else:
                offSetArea = (ListSections[iSplit].d / 2 - ListSections[iSplit].t) * 2 * ListSections[iSplit].t + (abs(offSet) - ListSections[iSplit].d / 2 - ListSections[iSplit].t) * ListSections[iSplit].w
        else:
            offSet = ListSections[iSplit].w / 2 - ListDistToCentroid[iSplit]
            if abs(offSet) < ListSections[iSplit].w / 2 - ListSections[iSplit].t:
                offSetArea = offSet * 2 * ListSections[iSplit].t
            else:
                offSetArea = (ListSections[iSplit].w / 2 - ListSections[iSplit].t) * 2 * ListSections[iSplit].t + (abs(offSet) - ListSections[iSplit].w / 2 - ListSections[iSplit].t) * ListSections[iSplit].d

        A1 = ListSections[iSplit].A - offSetArea
        A2 = ListSections[iSplit].A + offSetArea

        if ListRotations[iSplit] == "X":
            endArea = ListSections[iSplit].w * ListSections[iSplit].t
            sideArea = A1 - endArea
            if sideArea < 0:
                sideArea = 0
                C1 = 0
                C2 = ListSections[iSplit].d / 2
            else:
                distToEnd1 = (ListSections[iSplit].d / 2 - ListSections[iSplit].t - offSet)
                C1 = ((distToEnd1 + ListSections[iSplit].t / 2) * endArea + distToEnd1 / 2 * sideArea) / A1
                sideArea = A2 - endArea
                distToEnd2 = (ListSections[iSplit].d / 2 - ListSections[iSplit].t + offSet)
                C2 = ((distToEnd2 + ListSections[iSplit].t / 2) * endArea + distToEnd2 / 2 * sideArea) / A2
        else:
            endArea = ListSections[iSplit].d * ListSections[iSplit].t
            sideArea = A1 - endArea
            if sideArea < 0:
                sideArea = 0
                C1 = 0
                C2 = ListSections[iSplit].w / 2
            else:
                distToEnd1 = (ListSections[iSplit].w / 2 - ListSections[iSplit].t - offSet)
                C1 = ((distToEnd1 + ListSections[iSplit].t / 2) * endArea + distToEnd1 / 2 * sideArea) / A1

                sideArea = A2 - endArea
                distToEnd2 = (ListSections[iSplit].w / 2 - ListSections[iSplit].t + offSet)
                C2 = ((distToEnd2 + ListSections[iSplit].t / 2) * endArea + distToEnd2 / 2 * sideArea) / A2
        Z = A1 * C1 + A2 * C2

    for i in range(len(ListSections)):
        if i != iSplit:
            Z += ListSections[i].A * ListDistToCentroid[i]
    return Z


def getZWeek(ListSections, ListRotations):
    Z = 0
    for i in range(len(ListSections)):
        if ListRotations[i] == "X":
            Z += ListSections[i].Zy
        else:
            Z += ListSections[i].Zx
    return Z

class CrossSection:
    def __init__(self):
        self.ListSections = []
        self.ListRotations = []

        self.Centroid = None
        self.listDistToCentroid = None

        self.A = None
        self.Ix = None
        self.Iy = None
        self.Sx = None
        self.Sy = None
        self.x = None
        self.y = None
        self.M = None
        self.rx = None
        self.ry = None
        self.Zx = None
        self.Zy = None
        self.Fy = 210

    def addSection(self, x, y, t, A, M, Ix, Iy, Sx, Sy, rx, ry, Zx, Zy, j, rotation):
        self.ListSections.append(HSS(x, y, t, A, M, Ix, Iy, Sx, Sy, rx, ry, Zx, Zy, j))
        self.ListRotations.append(rotation)

    def setFy(self, Fy):
        self.Fy = Fy

    def solve(self):
        self.Centroid, self.listDistToCentroid, self.A = getCentroid(self.ListSections, self.ListRotations)
        self.Ix = getICombineStrong(self.ListSections, self.ListRotations, self.listDistToCentroid)
        self.Iy = getICombineWeek(self.ListSections, self.ListRotations)
        self.Sx, self.x = getSStrong(self.ListSections, self.ListRotations, self.Ix)
        self.Sy, self.y = getSWeek(self.ListSections, self.ListRotations, self.Iy)
        self.M = getM(self.ListSections)
        self.rx, self.ry = getr(self.A, self.Ix, self.Iy)
        self.Zx = getZStrong(self.ListSections, self.ListRotations, self.listDistToCentroid)
        self.Zy = getZWeek(self.ListSections, self.ListRotations)

    def getBendingClass(self):
        Max = 0
        FyClass4 = None
        iMax = None
        for i in range(len(self.ListSections)):
            if self.ListRotations == "X":
                Value = self.ListSections[i].w * self.Fy ** 0.5 / self.ListSections[i].t
            else:
                Value = self.ListSections[i].d * self.Fy ** 0.5 / self.ListSections[i].t
            Max = max(Max, Value)
            if Value == Max:
                iMax = i
        if Max <= 525:
            Bclass = 1
        elif Max <= 670:
            Bclass = 3
        else:
            Bclass = 4

            if self.ListRotations == "X":
                FyClass4 = (670 * self.ListSections[iMax].t / self.ListSections[iMax].w) ** 2
            else:
                FyClass4 = (670 * self.ListSections[iMax].t / self.ListSections[iMax].d) ** 2
        return Bclass , FyClass4


    def getMomentResistance(self):
        Bclass, FyClass4 = self.getBendingClass()
        if Bclass <= 2:
            Mr = 0.9 * self.Zx * self.Fy
        elif Bclass == 3:
            Mr = 0.9 * self.Sx * self.Fy
        else:
            Mr = 0.9 * self.Sx * FyClass4
        return Mr

Base = CrossSection()
Base.addSection(76.2, 76.2, 6.35, 1530, 13.1, 1.23*10**6, 1.23*10**6, 32.2*10**3, 32.2*10**3, 28.4, 28.4, 39.6*10**3, 39.6*10**3, 2060*10**3, "X")
Base.addSection(152.4, 76.2, 6.35, 2400, 20.7, 6.89*10**6, 2.31*10**6, 90.4*10**3, 60.7*10**3, 53.6, 31.0, 114*10**3, 70.3*10**3, 5760*10**3, "X")
Base.solve()
print(Base.Ix *2)
print(Base.Sx *2)
print(Base.Zx *2)
Mr = Base.getMomentResistance() * 2

print(Mr)

Post = CrossSection()
Post.addSection(152.4, 101.6, 6.35, 2690, 23.2, 8.45*10**6, 4.5*10**6, 111*10**3, 88.6*10**3, 56, 40.9, 136*10**3, 103*10**3, 9530*10**3, "X")
Post.addSection(101.6, 101.6, 6.35, 2110, 18.3, 3.17*10**6, 3.17*10**6, 62.3*10**3, 62.3*10**3, 38.7, 38.7, 74.8*10**3, 74.8*10**3, 5170*10**3, "X")
Post.addSection(152.4, 101.6, 6.35, 2690, 23.2, 8.45*10**6, 4.5*10**6, 111*10**3, 88.6*10**3, 56, 40.9, 136*10**3, 103*10**3, 9530*10**3, "X")
Post.solve()
print("Post Ix: ", Post.Ix)
print("Post Iy: ", Post.Iy)

Mr = Post.getMomentResistance()
print("Post Mr: ", Mr)