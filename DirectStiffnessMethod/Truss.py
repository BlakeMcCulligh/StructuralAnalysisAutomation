import numpy as np
import matplotlib.pyplot as plt

class Truss:
    def __init__(self):
        self.E = 1e4
        self.Nodes = []
        self.Bars = []
        self.Area = []
        self.appliedForces = []
        self.supports = []
        self.Forces = []
        self.Reactions = []
        self.Displacements = []

    def addNode(self,x,y):
        self.Nodes.append([x,y])

    def addBar(self,Node1, Node2, CrossSectionArea):
        self.Bars.append([Node1, Node2])
        self.Area.append(CrossSectionArea)

    def addAppliedForce(self, Node, Fx, Fy):
        self.appliedForces.append([Node, Fx, Fy])

    def addSupport(self, Node, Fx, Fy):
        self.supports.append([Node, Fx, Fy])

    def solve(self):
        nodes = np.array(self.Nodes).astype(float)
        bars = np.array(self.Bars)
        A = np.array(self.Area)

        # Applied forces
        P = np.zeros_like(nodes)
        for i in range(len(self.appliedForces)):
            P[self.appliedForces[i][0], 0] = self.appliedForces[i][1]
            P[self.appliedForces[i][0], 1] = self.appliedForces[i][2]

        # Supports
        DOFCON = np.ones_like(nodes).astype(int)
        Ur = []
        for i in range(len(self.supports)):
            if self.supports[i][1] == 0:
                DOFCON[self.supports[i][0], 0] = 0
                Ur.append(0)
            if self.supports[i][2] == 0:
                DOFCON[self.supports[i][0], 1] = 0
                Ur.append(0)

        NN = len(nodes)
        NE = len(bars)
        DOF = 2
        NDOF = DOF * NN

        # structural analysis
        d = nodes[bars[:, 1], :] - nodes[bars[:, 0], :]
        L = np.sqrt((d ** 2).sum(axis=1))
        angle = d.T / L
        a = np.concatenate((-angle.T, angle.T), axis=1)
        K = np.zeros([NDOF, NDOF])
        for k in range(NE):
            aux = 2 * bars[k, :]
            index = np.r_[aux[0]:aux[0] + 2, aux[1]:aux[1] + 2]

            ES = np.dot(a[k][np.newaxis].T * self.E * A[k], a[k][np.newaxis]) / L[k]
            K[np.ix_(index, index)] = K[np.ix_(index, index)] + ES

        freeDOF = DOFCON.flatten().nonzero()[0]
        supportDOF = (DOFCON.flatten() == 0).nonzero()[0]
        Kff = K[np.ix_(freeDOF, freeDOF)]
        Kfr = K[np.ix_(freeDOF, supportDOF)]
        Krf = Kfr.T
        Krr = K[np.ix_(supportDOF, supportDOF)]
        Pf = P.flatten()[freeDOF]
        Uf = np.linalg.solve(Kff, Pf)
        U = DOFCON.astype(float).flatten()
        U[freeDOF] = Uf
        U[supportDOF] = Ur
        U = U.reshape(NN, DOF)
        u = np.concatenate((U[bars[:, 0]], U[bars[:, 1]]), axis=1)
        N = self.E * A[:] / L[:] * (a[:] * u[:]).sum(axis=1)
        R = (Krf[:] * Uf).sum(axis=1) + (Krr[:] * Ur).sum(axis=1)
        self.Forces = np.array(N)[np.newaxis].T
        self.Reactions = np.array(R)
        self.Displacements = U
        return self.Forces, self.Reactions, self.Displacements

    def Plot(self, nodes, bars, c, lt, lw, lg):
        for i in range(len(bars)):
            xi, xf, = nodes[bars[i, 0], 0], nodes[bars[i, 1], 0]
            yi, yf, = nodes[bars[i, 0], 1], nodes[bars[i, 1], 1]
            line, = plt.plot([xi, xf], [yi, yf], color=c, linestyle=lt, linewidth=lw)
        line.set_label(lg)
        plt.legend()

    def print(self, scale):
        print('Axial Forces (positive = tension, negative = compression)')
        print(self.Forces)
        print('Reaction Forces (positive = upward, negative = downword)')
        print(self.Reactions)
        print('Deformation at nodes')
        print(self.Displacements)

        nodes = np.array(self.Nodes).astype(float)
        bars = np.array(self.Bars)
        self.Plot(nodes, bars, 'gray', '--', 1, 'Undeformed')
        Dnodes = self.Displacements * scale + nodes
        self.Plot(Dnodes, bars, 'red', '-', 2, 'deformed')
        plt.show()

truss = Truss()
truss.addNode(0, 120)
truss.addNode(120, 120)
truss.addNode(240, 120)
truss.addNode(360, 120)
truss.addNode(0, 0)
truss.addNode(120, 0)
truss.addNode(240, 0)
truss.addNode(360, 0)

truss.addBar(0,1,0.111)
truss.addBar(1,2,0.111)
truss.addBar(2,3,0.111)
truss.addBar(4,5,0.111)
truss.addBar(5,6,0.111)
truss.addBar(6,7,0.111)

truss.addBar(5,1,0.111)
truss.addBar(6,2,0.111)
truss.addBar(7,3,0.111)

truss.addBar(0,5,0.111)
truss.addBar(4,1,0.111)
truss.addBar(1,6,0.111)
truss.addBar(5,2,0.111)
truss.addBar(2,7,0.111)
truss.addBar(7,3,0.111)

truss.addAppliedForce(7,0,-10)

truss.addSupport(0,0,0)
truss.addSupport(4,0,0)

truss.solve()

truss.print(1)
