import numpy as np
from matplotlib import pyplot as plt

# Creates a 4x4 element stiffness matrix, in the global coordinate system
# input:
# nodexy : [[x1,y1],[x2,y2]]
# E : Young's modulus
# A : Cross-section Area
# I : Second moment of Area
def FrameElement2D(nodexy, E, A, I):
    E1 = np.array([(nodexy[1][0] - nodexy[0][0]), (nodexy[1][1] - nodexy[0][1])])
    L = float(np.linalg.norm(E1))
    E1 = E1 / L
    E2 = np.array([-E1[1], E1[0]])
    Kel_bend = np.array([[12 * E * I / (L ** 3), 6 * E * I / (L ** 2), -12 * E * I / (L ** 3), 6 * E * I / (L ** 2)],
                         [6 * E * I / (L ** 2), 4 * E * I / L, -6 * E * I / (L ** 2), 2 * E * I / L],
                         [-12 * E * I / (L ** 3), -6 * E * I / (L ** 2), 12 * E * I / (L ** 3), -6 * E * I / (L ** 2)],
                         [6 * E * I / (L ** 2), 2 * E * I / L, -6 * E * I / (L ** 2), 4 * E * I / L]])
    Kel_axial = E * A / L * np.array([[1, -1], [-1, 1]])

    Kel_LOC = np.zeros(shape=(6,6))
    Kel_LOC[0][0] = Kel_axial[0][0]
    Kel_LOC[0][3] = Kel_axial[0][1]
    Kel_LOC[3][0] = Kel_axial[1][0]
    Kel_LOC[3][3] = Kel_axial[1][1]
    for i in range(4):
        for j in range(4):
            if i == 0:
                ii = 1
            elif i == 1:
                ii = 2
            elif i == 2:
                ii = 4
            else:
                ii = 5
            if j == 0:
                jj = 1
            elif j == 1:
                jj = 2
            elif j == 2:
                jj = 4
            else:
                jj = 5
            Kel_LOC[ii][jj] = Kel_bend[i][j]
    Qrot = [[E1[0],E1[1], 0], [E2[0], E2[1], 0], [0, 0, 1]]
    TmUP = np.append(Qrot, np.zeros(shape = (3,3)), axis=1)
    TmDown = np.append(np.zeros(shape = (3,3)), Qrot, axis=1)
    Tmatrix = np.append(TmUP, TmDown, axis=0)
    Kel = Tmatrix.T @ Kel_LOC @ Tmatrix
    return Kel

# Creates the global stiffness matrix
# K : Global stiffness Matrix
# elems : elements
# Nel : number of elements
# nodes : nodes
# Nnodes : number of nodes
# E : Young's Modulus
# A : cross-section area
# I : second moment of Area
# noinspection SpellCheckingInspection
def MakeGlobalStiffnessMatrix(K, elems, Nel, nodes, E, A, I ):
    for i in range(Nel):
        elnodes = [elems[i][0]-1, elems[i][1]-1]
        nodexy = [[nodes[elnodes[0]][0], nodes[elnodes[0]][1]], [nodes[elnodes[1]][0], nodes[elnodes[1]][1]]]

        Kel = FrameElement2D(nodexy, E[i], A[i], I[i])

        eldofs = np.concatenate([np.arange(3 * (elnodes[0]), 3 * (elnodes[0] + 1)),
                                 np.arange(3 * (elnodes[1]), 3 * (elnodes[1] + 1))])
        K[np.ix_(eldofs, eldofs)] += Kel
    return K

# solves the global stiffness equation to get the deformations, and the forces acting on the members
# K : global stiffness matrix
# f : forces acting on the members
# u : deformations
# doffree : joints that are not restrained
# dofspec : joints that are restrained
# noinspection SpellCheckingInspection
def solveUF(K, f, u, doffree, dofspec):
    u[doffree] = np.linalg.solve(K[np.ix_(doffree, doffree)], f[doffree] - K[np.ix_(doffree, dofspec)] @ u[dofspec])
    f[dofspec] = K[dofspec, :].dot(u)
    return u, f

def solve(nodes, elems, E, A, I, bcs, loads):
    Nel = len(elems)
    Nnodes = len(nodes)

    alldofs = []
    for i in range(3 * Nnodes):
        alldofs.append(i)
    K = np.zeros(shape=(3 * Nnodes, 3 * Nnodes))
    u = np.zeros(shape=(3 * Nnodes, 1))
    f = np.zeros(shape=(3 * Nnodes, 1))

    dofspec = []
    for i in range(len(bcs)):
        thisdof = 3 * (bcs[i][0] - 1) + bcs[i][1]
        dofspec.append(thisdof)
        u[thisdof] = bcs[i][2]
    doffree = alldofs.copy()
    dofspec.sort(reverse=True)
    for index in dofspec:
        del doffree[index - 1]

    for i in range(len(loads)):
        f[3 * (loads[i][0] - 1) + loads[i][1] - 1] = loads[i][2]

    K = MakeGlobalStiffnessMatrix(K, elems, Nel, nodes, E, A, I)
    u, f = solveUF(K, f, u, doffree, dofspec)

    print("Deformation: ", u)
    print("Forces in each member: ", f)
    return u, f

def printResults(nodes, elems, u, mag, numDivs):
    Nel = len(elems)
    Nnodes = len(nodes)
    # ploting
    # undeformed
    for i in range(Nnodes):
        plt.plot(nodes[i][0], nodes[i][1], 'o', color='black')
    for i in range(Nel):
        plt.plot([nodes[elems[i][0] - 1][0], nodes[elems[i][1] - 1][0]],
                 [nodes[elems[i][0] - 1][1], nodes[elems[i][1] - 1][1]], color='black')

    # deformed
    for i in range(Nnodes):
        plt.plot(nodes[i][0] + mag * u[i * 3], nodes[i][1] + mag * u[i * 3 + 1], 'o', color='red')

    for i in range(Nel):
        elnodes = [elems[i][0] - 1, elems[i][1] - 1]
        E1 = np.array([(nodes[elnodes[1]][0] - nodes[elnodes[0]][0]), (nodes[elnodes[1]][1] - nodes[elnodes[0]][1])])
        le = float(np.linalg.norm(E1))
        E1 = E1 / le
        E1 = E1.tolist()
        E2 = [-E1[1], E1[0]]

        eldofs = np.concatenate([np.arange(3 * (elnodes[0]), 3 * (elnodes[0] + 1)),
                                 np.arange(3 * (elnodes[1]), 3 * (elnodes[1] + 1))])
        ut = u.tolist()
        eldisp = []
        for j in range(len(eldofs)):
            eldisp.append(ut[eldofs[j]])
        Qrot = [[E1[0], E1[1], 0], [E2[0], E2[1], 0], [0, 0, 1]]
        TmUP = np.append(Qrot, np.zeros(shape=(3, 3)), axis=1)
        TmDown = np.append(np.zeros(shape=(3, 3)), Qrot, axis=1)
        Tmatrix = np.append(TmUP, TmDown, axis=0)
        eldispLOC = Tmatrix @ eldisp
        plotpts = []
        for j in range(numDivs + 1):
            xi = j / numDivs
            xdispLOC = eldispLOC[0] * (1 - xi) + eldispLOC[3] * xi
            ydispLOC = eldispLOC[1] * (1 - 3 * xi ** 2 + 2 * xi ** 3) + eldispLOC[4] * (3 * xi ** 2 - 2 * xi ** 3) + \
                       eldispLOC[2] * le * (xi - 2 * xi ** 2 + xi ** 3) + eldispLOC[5] * le * (-xi ** 2 + xi ** 3)

            Q = np.array([[Qrot[0][0], Qrot[0][1]], [Qrot[1][0], Qrot[1][1]]])
            xydisp = (Q.T @ np.array([xdispLOC, ydispLOC]))
            x = nodes[elems[i][0] - 1][0] + xi * le * E1[0] + mag * xydisp[0]
            y = nodes[elems[i][0] - 1][1] + xi * le * E1[1] + mag * xydisp[1]
            plotpts.append([x.tolist()[0], y.tolist()[0]])
        for j in range(len(plotpts) - 1):
            plt.plot([plotpts[j][0], plotpts[j + 1][0]], [plotpts[j][1], plotpts[j + 1][1]], color='red')
    plt.show()

# inputs
Nodes = [[0.0,0.0],[0.0,2.0],[1.5,3.0],[3.0,2.0],[3.0,0.0]]
Elems =  [[1,2],[2,3],[3,4],[4,5]]
E = [2e11, 2e11, 2e11, 2e11]
A = [1e-2, 1e-2, 1e-2, 1e-2]
I = [5e-6, 5e-6, 5e-6, 5e-6]
Bcs = [[1,1,0], [1,2,0], [5,1,0], [5,2,0]]
Loads = [[3,2,-20000]]

U, F = solve(Nodes, Elems, E, A, I, Bcs, Loads)
Mag = 20
Ndivs = 20
printResults(Nodes, Elems, U, Mag, Ndivs)