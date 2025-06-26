import numpy as np
from SteelCrossSection import getCrossSectionProperties
import SteelCode

class Joint(object):

    def __init__(self, x, y):
        self.resTy = False
        self.resTx = False
        self.memberList = []

        self.loadx = None
        self.loady = None
        self.solved = False
        self.x = x
        self.y = y

    def setRestraints(self, resTx, resTy):
        self.resTx = resTx
        self.resTy = resTy

    def addMember(self, member,):
        self.memberList.append(member)

    def setLoad(self, Lx, Ly):
        self.loadx = Lx
        self.loady = Ly

class CrossSection(object):

    def __init__(self, memberType, d, b, t, w ):
        self.E = 200000
        self.G = 77000
        self.Fy = 210
        self.Fu = 380
        self.n = 1.34
        self.NumSymetry = None
        [self.NumSymetry, self.A, self.Ix, self.Iy, self.Sx, self.Sy, self.Zx, self.Zy, self.J, self.Cw, self.rx, self.ry, self.xo, self.yo] = getCrossSectionProperties(memberType, d, b, t, w)

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
        self.J1I = J1I
        self.J2I = J2I
        self.force = None
        self.Cr = None
        self.Tr = None
        self.K = 1
        self.L = ((J2.x-J1.x)**2 + (J2.y-J1.y)**2)**0.5
        self.usageRatio = None
        self.crossSection = None
        self.crossSection = CrossSection(MemberType, d, b, t, w)

        J1.addMember(self)
        J2.addMember(self)

    def getResistance(self):
        self.Cr = SteelCode.getCompressionResistance(self.crossSection.NumSymetry, self.K, self.L, self.crossSection.rx, self.crossSection.ry, self.crossSection.xo, self.crossSection.yo, self.crossSection.A, self.crossSection.J, self.crossSection.Cw, self.crossSection.Fy, self.crossSection.n, self.crossSection.E, self.crossSection.G)
        self.Tr = SteelCode.getTensionResistance(self.crossSection.A, self.crossSection.Fy)

class Truss(object):
    def __init__(self):
        self.listJoints = []
        self.listMembers = []
        self.listMemberNames = []
        self.forceSolutions = {}

    def addJoint(self, x, y):
        newJoint = Joint(x, y)
        self.listJoints.append(newJoint)

    def addMember(self, J1Index, J2Index, MemberType, d, b, t, w):
        newMember = Member(self.listJoints[J1Index], self.listJoints[J2Index], J1Index, J2Index, MemberType, d, b, t, w)
        self.listMembers.append(newMember)

    def addLoad(self, jointIndex, Loadx, Loady):
        self.listJoints[jointIndex].setLoad(Loadx, Loady)

    def addRestraints(self, jointIndex, Tx, Ty):
        self.listJoints[jointIndex].setRestraints(Tx, Ty)

    def solveForces(self):

        joints = {}
        for i in range(len(self.listJoints)):
            joints[str(i)] = [self.listJoints[i].x , self.listJoints[i].y]

        members = []
        for i in range(len(self.listMembers)):
            members.append((str(self.listMembers[i].J1I), str(self.listMembers[i].J2I)))

        supports = {}
        for i in range(len(self.listJoints)):
            if self.listJoints[i].resTx is True or self.listJoints[i].resTy is True:
                supports[str(i)] = (self.listJoints[i].resTx, self.listJoints[i].resTy)

        loads = {}
        for i in range(len(self.listJoints)):
            if self.listJoints[i].loadx != 0 or self.listJoints[i].loady != 0:
                loads[str(i)] = (self.listJoints[i].loadx, self.listJoints[i].loady)
            if loads[str(i)] == (None, None):
                loads[str(i)] = (0, 0)

        num_members = len(members)

        # Assign fixed order to unknowns: members first, then reactions
        reaction_list = []  # (joint, dir), e.g. ('A', 'x')
        for joint, (rx, ry) in supports.items():
            if rx:
                reaction_list.append((joint, 'x'))
            if ry:
                reaction_list.append((joint, 'y'))

        num_reactions = len(reaction_list)
        total_unknowns = num_members + num_reactions

        A = []
        b = []

        for joint in joints:
            row_fx = [0.0] * total_unknowns
            row_fy = [0.0] * total_unknowns

            # Contributions from members
            for idx, (ja, jb) in enumerate(members):
                if joint == ja or joint == jb:

                    # Direction vector from current joint to other joint
                    if joint == ja:
                        dx = joints[jb][0] - joints[ja][0]
                        dy = joints[jb][1] - joints[ja][1]
                    elif joint == jb:
                        dx = joints[ja][0] - joints[jb][0]
                        dy = joints[ja][1] - joints[jb][1]
                    else:
                        continue  # Should never happen

                    L = (dx ** 2 + dy ** 2) ** 0.5

                    row_fx[idx] = dx / L
                    row_fy[idx] = dy / L

            # Contributions from reactions
            for r_idx, (r_joint, r_dir) in enumerate(reaction_list):
                if r_joint == joint:
                    if r_dir == 'x':
                        row_fx[num_members + r_idx] = 1
                    elif r_dir == 'y':
                        row_fy[num_members + r_idx] = 1

            # External loads
            Fx, Fy = loads.get(joint, (0.0, 0.0))

            # Add rows to matrix
            A.append(row_fx)
            b.append(-Fx)
            A.append(row_fy)
            b.append(-Fy)

        # Convert to NumPy arrays
        A = np.array(A)
        b = np.array(b)

        # Solve
        x = np.linalg.solve(A, b)

        # Extract results
        member_forces = x[:num_members]
        reaction_forces = x[num_members:]

        self.forceSolutions = {
            'members': {m: round(f, 3) for m, f in zip(members, member_forces)},
            'reactions': {
                f'R{r_dir.upper()}_{joint}': round(f, 3)
                for (joint, r_dir), f in zip(reaction_list, reaction_forces)
            }
        }
        i = 0
        for m, f in self.forceSolutions['members'].items():
            self.listMembers[i].force = f
            self.listMemberNames.append(m)
            i = i + 1

        return self.forceSolutions

    def solveUsageRatio(self):

        for i in range(len(self.listMembers)):
            self.listMembers[i].getResistance()
            if self.listMembers[i].force >= 0:
                self.listMembers[i].usageRatio = self.listMembers[i].force / self.listMembers[i].Tr
            else:
                self.listMembers[i].usageRatio = -1 *self.listMembers[i].force / self.listMembers[i].Cr

    def printForces(self):
        print("Member Forces:")
        for m, f in self.forceSolutions['members'].items():
            if f > 0:
                print(f"{m}: {f} N (Tension)")
            else:
                print(f"{m}: {abs(f)} N (Compression)")

        print("\nReaction Forces:")
        for r, f in self.forceSolutions['reactions'].items():
            print(f"{r}: {f} N")

    def printUsageRatios(self):
        print("\nUsage Ratios: ")
        for i in range(len(self.listMembers)):
            if self.listMembers[i].usageRatio > 1:
                print(self.listMemberNames[i], ": ", self.listMembers[i].usageRatio, " - Fail")
            else:
                print(self.listMemberNames[i],": " ,self.listMembers[i].usageRatio)

#Test
testTruss = Truss()
testTruss.addJoint(0, 0)
testTruss.addJoint(1, 1)
testTruss.addJoint(2, 0.5)
testTruss.addMember(0,1, "I", 100, 15, 2, 2)
testTruss.addMember(0,2, "I", 100, 15, 2, 2)
testTruss.addMember(1,2, "I", 100, 15, 2, 2)
testTruss.addLoad(2,0,-10000)
testTruss.addRestraints(0,True,True)
testTruss.addRestraints(1,False,True)
forceSolutions = testTruss.solveForces()
testTruss.printForces()
testTruss.solveUsageRatio()
testTruss.printUsageRatios()