import math

import SteelCode
from SteelCrossSection import getCrossSectionProperties


class Joint(object):

    def __init__(self, x, y):
        self.resTy = False
        self.resTx = False

        self.loadx = None
        self.loady = None

        self.x = x
        self.y = y

        self.memberList = []

        self.Jointx = []
        self.Jointy = []
        self.JointM = []

    def setRestraints(self, resTx, resTy):
        self.resTx = resTx
        self.resTy = resTy

    def addMember(self, member, Jx, Jy, JM):
        self.memberList.append(member)
        self.Jointx.append(Jx)
        self.Jointy.append(Jy)
        self.JointM.append(JM)

    def setLoad(self, Lx, Ly):
        self.loadx = Lx
        self.loady = Ly

class CrossSection(object):

    def __init__(self, memberType, d, b, t, w):
        self.memberType = memberType
        self.d = d
        self.b = b
        self.t = t
        self.w = w
        self.E = 200000
        self.G = 77000
        self.Fy = 210
        self.Fu = 380
        self.n = 1.34
        self.NumSymetry = None
        [self.NumSymetry, self.bClassX, self.bClassY, self.A, self.Ix, self.Iy, self.Sx, self.Sy, self.Zx, self.Zy, self.J, self.Cw, self.rx,
             self.ry, self.xo, self.yo] = getCrossSectionProperties(memberType, d, b, t, w)

    def setMaterialProperties(self, E, G, Fy, Fu, n):
        self.E = E
        self.G = G
        self.Fy = Fy
        self.Fu = Fu
        self.n = n

class Member(object):

    def __init__(self, J1, J2, J1I, J2I, MemberType, d, b, t, w):
        self.J1 = J1
        self.J2 = J2
        J1.addMember(self)
        J2.addMember(self)
        self.J1I = J1I
        self.J2I = J2I
        self.J1x = None
        self.J1y = None
        self.J1M = None
        self.J2x = None
        self.J2y = None
        self.J2M = None

        self.loadx = 0
        self.loady = 0

        self.K = 1
        self.L = ((J2.x-J1.x)**2 + (J2.y-J1.y)**2)**0.5
        self.crossSection = CrossSection(MemberType, d, b, t, w)
        self.axis = None

        self.ForceX = None
        self.ForceY = None

        self.Cr = None
        self.Tr = None
        self.Mr = None
        self.usageRatio = None

        self.deflection = None

    def getResistance(self):
        self.Cr = SteelCode.getCompressionResistance(self.crossSection.NumSymetry, self.K, self.L, self.crossSection.rx, self.crossSection.ry, self.crossSection.xo, self.crossSection.yo, self.crossSection.A, self.crossSection.J, self.crossSection.Cw, self.crossSection.Fy, self.crossSection.n, self.crossSection.E, self.crossSection.G)
        self.Tr = SteelCode.getTensionResistance(self.crossSection.A, self.crossSection.Fy)
        if self.axis == "x":
            self.Mr = SteelCode.getBendingResistanceLaterallySupported(self.crossSection.bClassX, self.crossSection.Zx, self.crossSection.Sx, self.crossSection.Fy)
        else:
            self.Mr = SteelCode.getBendingResistanceLaterallySupported(self.crossSection.bClassY, self.crossSection.Zy,
                                                                       self.crossSection.Sy, self.crossSection.Fy)

class Frame(object):
    def __init__(self):
        self.listJoints = []
        self.listMembers = []
        self.listMemberNames = []

    def addJoint(self, x, y):
        newJoint = Joint(x, y)
        self.listJoints.append(newJoint)

    def addMember(self, J1Index, J2Index, MemberType, d, b, t, w, J1x, J1y, J1M, J2x, J2y, J2M):
        newMember = Member(self.listJoints[J1Index], self.listJoints[J2Index], J1Index, J2Index, MemberType, d, b, t, w)
        self.listMembers.append(newMember)
        self.listMemberNames.append((str(J1Index), str(J2Index)))
        self.listJoints[J1Index].addMember(self, newMember, J1x, J1y, J1M)
        self.listJoints[J2Index].addMember(self, newMember, J2x, J2y, J2M)

    def addJointLoad(self, jointIndex, Loadx, Loady):
        self.listJoints[jointIndex].setLoad(Loadx, Loady)

    def addRestraints(self, jointIndex, Tx, Ty):
        self.listJoints[jointIndex].setRestraints(Tx, Ty)

    def solveForces(self):
        listMemberForces = []
        listNumForcesKnown = []
        for i in range(len(self.listMembers)):
            memberForce = [i, self.listMembers[i].ForceX, self.listMembers[i].ForceY]
            if self.listMembers[i].ForceX is None and self.listMembers[i].ForceY is None:
                listNumForcesKnown.append(0)
            elif self.listMembers[i].ForceX is not None and self.listMembers[i].ForceY is None:
                listNumForcesKnown.append(1)
            elif self.listMembers[i].ForceX is None and self.listMembers[i].ForceY is not None:
                listNumForcesKnown.append(1)
            elif self.listMembers[i].ForceX is not None and self.listMembers[i].ForceY is not None:
                listNumForcesKnown.append(2)
            listMemberForces.append(memberForce)

        SortedMemberForces = [x for _, x in sorted(zip(listNumForcesKnown, listMemberForces))]
        sortedlistNumForcesKnown = sorted(listNumForcesKnown)



        # returns a list of
        listJointForces = []
        NumUnknownForcesX = []
        NumUnknownForcesY = []
        for i in range(len(self.listJoints)):
            jointForce = [i, self.listJoints[i].loadx, self.listJoints[i].loady]
            listJointForces.append(jointForce)
            NumUnknownForcesX.append(0)
            NumUnknownForcesY.append(0)

        for i in range(len(self.listMembers)):
            jointForces1 = listJointForces[self.listMembers[i].J1Index]
            jointForces2 = listJointForces[self.listMembers[i].J2Index]
            if  self.listMembers[i].ForceX is None:
                NumUnknownForcesX[self.listMembers[i].J1Index] = NumUnknownForcesX[self.listMembers[i].J1Index] + 1
                NumUnknownForcesX[self.listMembers[i].J2Index] = NumUnknownForcesX[self.listMembers[i].J2Index] + 1
            else:
                jointForces1[1] = jointForces1[1] + self.listMembers[i].ForceX
                jointForces2[1] = jointForces2[1] + self.listMembers[i].ForceX

            if self.listMembers[i].ForceY is None:
                NumUnknownForcesY[self.listMembers[i].J1Index] = NumUnknownForcesY[self.listMembers[i].J1Index] + 1
                NumUnknownForcesY[self.listMembers[i].J2Index] = NumUnknownForcesY[self.listMembers[i].J2Index] + 1
            else:
                jointForces1[2] = jointForces1[2] + self.listMembers[i].ForceY
                jointForces2[2] = jointForces2[2] + self.listMembers[i].ForceY

