import numpy as np

pointLoads = np.array([[0,0,0]]) # Point Load (location, xMag, yMag)
pointMoments = np.array([[0,0]]) # Point Moments (location, Mag)
distributedLoads = np.array([[0,0,0]]) # distributed Loads (xStart, xEnd, Mag)
linearLoads = np.array([[0,0,0,0]]) # Distributed loads with linear variation (xStart, XEnd, startMeg, endMeg)

#input
span = 2.6416 # length of beam
A = 0 # distance to support A
B = 2 # distance to support B

# Force Data
pointLoads = np.append(pointLoads, [np.array([6,0,-90])], axis=0)
#pointMoments = np.append(pointMoments, [np.array([15,50])], axis=0)
#distributedLoads = np.append(distributedLoads, [np.array([1.2196,2.6415,1.2])], axis=0)
#linearLoads = np.append(linearLoads, [np.array([1.2196,2.6415,0,14.931])], axis=0)

#
# Defaults and initialisation
#
divs = 10000
delta = span/divs
X = np.arange(0, span+delta, delta)

nPL = len(pointLoads[0])
nPM = len(pointMoments[0])
nUDL = len(distributedLoads[0])
nLDL = len(linearLoads[0])

reactions = np.array([0.0,0,0])
shearForce = np.empty([0,len(X)])
bendingMoments = np.empty([0,len(X)])

#
# Reactions Calculater
#
def Reactions_PL(j, a, b):
    xp = pointLoads[j,0]
    fx = pointLoads[j,1]
    fy = pointLoads[j,2]

    la_p = a - xp
    mp = fy * la_p
    la_vb = b - a

    Vb = mp / la_vb
    Va = -fy - Vb
    Ha = - fx

    return Va, Vb, Ha

def reactions_PM(j, a, b):
    m = pointMoments[j, 1]
    la_vb = b - a

    Vb = m / la_vb
    Va = -Vb

    return Va, Vb

def reactions_UDL(j, a, b):
    xStart = distributedLoads[j, 0]
    xEnd = distributedLoads[j, 1]
    fy = distributedLoads[j, 2]

    fy_Res = fy * (xEnd - xStart)
    x_Res = xStart + 0.5 * (xEnd - xStart)

    la_p = a - x_Res
    mp = fy_Res * la_p
    la_vb = b - a

    Vb = mp / la_vb
    Va = -fy_Res - Vb

    return Va, Vb

def reactions_LDL(j, a, b):
    xStart = linearLoads[j, 0]
    xEnd = linearLoads[j, 1]
    fy_start = linearLoads[j, 2]
    fy_end = linearLoads[j, 3]

    if abs(fy_start) > 0:
        fy_Res = 0.5 * fy_start * (xEnd - xStart)
        x_Res = xStart + (1/3) * (xEnd - xStart)
    else:
        fy_Res = 0.5 * fy_end * (xEnd - xStart)
        x_Res = xStart + (2/3) * (xEnd - xStart)

    la_p = a - x_Res
    mp = fy_Res * la_p
    la_vb = b - a

    Vb = mp / la_vb
    Va = -fy_Res - Vb

    return Va, Vb


PL_record = np.empty([0,3])
if nPL>0:
    for n, p in enumerate(pointLoads):
        va, vb, ha = Reactions_PL(n, A, B)
        PL_record = np.append(PL_record, [np.array([va, ha, vb])], axis =0)
        reactions[0] = reactions[0] + va
        reactions[1] = reactions[1] + ha
        reactions[2] = reactions[2] + vb

PM_record = np.empty([0,2])
if nPM>0:
    for n, p in enumerate(pointMoments):
        va, vb = reactions_PM(n, A, B)
        PM_record = np.append(PM_record, [np.array([va,vb])], axis = 0)
        reactions[0] = reactions[0] + va
        reactions[2] = reactions[2] + vb

UDL_record = np.empty([0,2])
if nUDL>0:
    for n, p in enumerate(distributedLoads):
        va, vb = reactions_UDL(n, A, B)
        UDL_record = np.append(UDL_record, [np.array([va,vb])], axis = 0)
        reactions[0] = reactions[0] + va
        reactions[2] = reactions[2] + vb

LDL_record = np.empty([0,2])
if nLDL>0:
    for n, p in enumerate(linearLoads):
        va, vb = reactions_LDL(n, A, B)
        LDL_record = np.append(LDL_record, [np.array([va,vb])], axis = 0)
        reactions[0] = reactions[0] + va
        reactions[2] = reactions[2] + vb

#
# Shear and Moment Calculater
#
def Shear_Moment_PL(j, a, b):
    xp = pointLoads[j,0]
    fy = pointLoads[j,2]
    Va = PL_record[j,0]
    Vb = PL_record[j,2]

    S = np.zeros(len(X))
    M = np.zeros(len(X))

    for i, x in enumerate(X):
        if x>a:
            S[i] += Va
            M[i] -= Va * (x - a)

        if x>b:
            S[i] += Vb
            M[i] -= Vb * (x - b)

        if x>xp:
            S[i] += fy
            M[i] -= fy * (x-xp)

    return S, M


def shear_moment_PM(j, a, b):
    m = pointMoments[j, 1]
    Va = PM_record[j, 0]
    Vb = PM_record[j, 1]

    S = np.zeros(len(X))
    M = np.zeros(len(X))

    for i, x in enumerate(X):

        if x > a:
            S[i] += Va
            M[i] -= Va * (x - a)
        if x > b:
            S[i] += Vb
            M[i] -= Vb * (x - b)
        if x > m:
            M[i] -= m

    return S, M

def shear_moment_UDL(j, a, b):
    xStart = distributedLoads[j, 0]
    xEnd = distributedLoads[j, 1]
    fy = distributedLoads[j, 2]
    Va = UDL_record[j, 0]
    Vb = UDL_record[j, 1]

    S = np.zeros(len(X))
    M = np.zeros(len(X))

    for i, x in enumerate(X):
        if x > a:
            S[i] += Va
            M[i] -= Va * (x - a)
        if x > b:
            S[i] += Vb
            M[i] -= Vb * (x - b)
        if xStart < x <= xEnd:
            S[i] += fy * (x - xStart)
            M[i] -= fy * (x - xStart) * 0.5 * (x - xStart)
        elif x > xEnd:
            S[i] += fy * (xEnd - xStart)
            M[i] -= fy * (xEnd - xStart) * (x - xStart - 0.5 * (xEnd - xStart))

    return S, M


def shear_moment_LDL(j, a, b):
    xStart = linearLoads[j, 0]
    xEnd = linearLoads[j, 1]
    fy_start = linearLoads[j, 2]
    fy_end = linearLoads[j, 3]
    Va = LDL_record[j, 0]
    Vb = LDL_record[j, 1]

    S = np.zeros(len(X))
    M = np.zeros(len(X))

    for i, x in enumerate(X):

        if x > a:
            S[i] += Va
            M[i] -= Va * (x - a)
        if x > b:
            S[i] += Vb
            M[i] -= Vb * (x - b)

        if xStart < x < xEnd:
            if abs(fy_start) > 0:
                x_base = x - xStart
                f_out = fy_start - x_base * (fy_start / (xEnd - xStart))
                R1 = 0.5 * x_base * (fy_start - f_out)
                R2 = x_base * f_out
                S[i] += R1 + R2
                M[i] -= R1 * (2/3) * x_base - R2 * (x_base / 2)
            else:
                x_base = x - xStart
                f_out = fy_end * (x_base*(xEnd-xStart))
                R = 0.5 * x_base * f_out
                S[i] += R
                M[i] -= R * (x_base / 3)

        elif x > xEnd:
            if abs(fy_start) > 0:
                R = 0.5 * fy_start * (xEnd - xStart)
                xr = xStart + (1/3) * (xEnd - xStart)
                S[i] += R
                M[i] -= R * (x - xr)
            else:
                R = 0.5 * fy_end * (xEnd - xStart)
                xr = xStart + (2/3) * (xEnd - xStart)
                S[i] += R
                M[i] -= R * (x - xr)

    return S, M

if nPL > 0:
    for n, p in enumerate(pointLoads):
        Shear, Moment = Shear_Moment_PL(n, A, B)
        shearForce = np.append(shearForce, [Shear], axis = 0)
        bendingMoments = np.append(bendingMoments, [Moment], axis = 0)

if nPM>0:
    for n, p in enumerate(pointMoments):
        Shear, Moment = shear_moment_PM(n, A, B)
        shearForce = np.append(shearForce, [Shear], axis = 0)
        bendingMoments = np.append(bendingMoments, [Moment], axis = 0)

if nUDL>0:
    for n, p in enumerate(distributedLoads):
        Shear, Moment = shear_moment_UDL(n, A, B)
        shearForce = np.append(shearForce, [Shear], axis = 0)
        bendingMoments = np.append(bendingMoments, [Moment], axis = 0)

if nLDL>0:
    for n, p in enumerate(linearLoads):
        Shear, Moment = shear_moment_LDL(n, A, B)
        shearForce = np.append(shearForce, [Shear], axis = 0)
        bendingMoments = np.append(bendingMoments, [Moment], axis = 0)


print('The vertical reaction at A is {one} kN'.format(one = round(reactions[0],4)))
print('The vertical reaction at B is {one} kN'.format(one = round(reactions[2],4)))
#print('The horizontal reaction at A is {one} kN'.format(one = round(reactions[1],4)))

#
# Plotting shear diagram
#
#import plotly as py
import plotly.graph_objs as go

layoutShear = go.Layout(title = {'text': 'Shear Force Diagram'},
    yaxis = dict(title = 'Shear Force (kN)'),
    xaxis = dict(title = 'Distance (m)', range = [-1,span+1]),
    showlegend = False,
    )

lineShear = go.Scatter(
    x = X,
    y = sum(shearForce),
    mode = 'lines',
    name = 'Shear Force',
    fill = 'tonexty',
    line_color = 'green',
    fillcolor = 'rgba(0,255,0,0.1)',
    )

axis  = go.Scatter(
    x = [0,span],
    y = [0,0],
    mode = 'lines',
    line_color = 'black'
    )

figShear = go.Figure(data=[lineShear,axis], layout=layoutShear)

#
# Plotting moment diagram
#
layoutMoment = go.Layout(title = {'text': 'Bending Moment Diagram'},
    yaxis = dict(title = 'Bending Moment (kN m)', autorange = 'reversed'),
    xaxis = dict(title = 'Distance (m)', range = [-1,span+1]),
    showlegend = False,
    )

lineMoment = go.Scatter(
    x = X,
    y = -sum(bendingMoments),
    mode = 'lines',
    name = 'Bending Moment',
    fill = 'tonexty',
    line_color = 'red',
    fillcolor = 'rgba(255,0,0,0.1)',
    )

figMoment = go.Figure(data=[lineMoment,axis], layout=layoutMoment)

figShear.show()
figMoment.show()
