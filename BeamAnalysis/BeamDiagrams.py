#
# Plotting shear diagram
#
#import plotly as py
import plotly.graph_objs as go
import numpy as np

class Change:
    def __init__(self,Loc,Type,Mag):
        self.Loc = Loc
        self.Type = Type
        self.Mag = Mag

        self.shearPre = None
        self.shearPost = None

class Beam:

    def __init__(self):
        self.length = None

        self.supportMag = [0,0]
        self.supportLoc = []

        self.PointLoadMag = []
        self.PointLoadLoc = []

        self.UniDistLoadMag = []
        self.UniDistLoadLoc = []

        self.numSections = 1000
        self.shear = []
        self.moment = []

    def Reactions(self):

    # Moment Equation
        MzSup0 = 0

        # Point Loads
        for i in range(len(self.PointLoadMag)):
            distance = abs(self.PointLoadLoc[i] - self.supportLoc[0])
            MzSup0 += self.PointLoadMag[i] * distance

        # Uniformly Distributed Loads
        for i in range(len(self.UniDistLoadMag)):
            Mag = self.UniDistLoadMag[i] * (self.UniDistLoadLoc[i * 2 + 1] - self.UniDistLoadLoc[i * 2])
            dist = abs((self.UniDistLoadLoc[i * 2 + 1] + self.UniDistLoadLoc[i * 2]) / 2 - self.supportLoc[0])
            MzSup0 += dist * Mag

        self.supportMag[1] = -(MzSup0 / (self.supportLoc[1] - self.supportLoc[0]))

    # Force Equation
        Fy = 0
        # Point Loads
        for i in range(len(self.PointLoadMag)):
            Fy += self.PointLoadMag[i]

        # Uniformly Distributed Loads
        for i in range(len(self.UniDistLoadMag)):
            Fy += self.UniDistLoadMag[i] * (self.UniDistLoadLoc[i * 2 + 1] - self.UniDistLoadLoc[i * 2])

        self.supportMag[0] = -(Fy + self.supportMag[1])

    def GetM(self, dist, dif):
        M = 0

        # Supports
        for i in range(len(self.supportMag)):
            if dist > self.supportLoc[i]:
                M += self.supportMag[i]*(dist - self.supportLoc[i])

        # Point Loads
        for i in range(len(self.PointLoadLoc)):
            if dist > self.PointLoadLoc[i]:
                M += self.PointLoadMag[i]*(dist - self.PointLoadLoc[i])

        # Uniformly Distributed Loads
        for i in range(len(self.UniDistLoadMag)):
            if self.UniDistLoadLoc[i*2+1] <= dist:
                Mag = self.UniDistLoadMag[i] * (self.UniDistLoadLoc[i * 2 + 1] - self.UniDistLoadLoc[i * 2])
                dist = abs((self.UniDistLoadLoc[i * 2 + 1] + self.UniDistLoadLoc[i * 2]) / 2 - dist)
                M += dist * Mag
            elif self.UniDistLoadLoc[i*2] < dist:
                Mag = self.UniDistLoadMag[i] * (dist - self.UniDistLoadLoc[i * 2])
                dist = abs((dist + self.UniDistLoadLoc[i * 2]) / 2 - dist)
                M += dist * Mag

        return M

    def MomentSolve(self):
        dif = self.length / self.numSections
        self.moment.append(0)

        distUpTo = 0
        for i in range(self.numSections):
            distUpTo += dif
            M = self.GetM(distUpTo, dif)
            self.moment.append(M)

    def GetFyChange(self, dist, dif):
        Fy = 0

        # Supports
        for i in range(len(self.supportMag)):
            if dist >= self.supportLoc[i] > (dist - dif):
                Fy += self.supportMag[i]

        # Point Loads
        for i in range(len(self.PointLoadLoc)):
            if dist >= self.PointLoadLoc[i] > (dist - dif):
                Fy += self.PointLoadMag[i]

        # Uniformly Distrubuted Loads
        for i in range(len(self.UniDistLoadMag)):
            # (dist - dif) to dist
            # self.DistLoadLoc[i * 2] to self.DistLoadLoc[i * 2 + 1]
            if self.UniDistLoadLoc[i * 2] < dist and self.UniDistLoadLoc[i * 2 + 1] > (dist - dif):

                if self.UniDistLoadLoc[i * 2] < (dist - dif) and self.UniDistLoadLoc[i * 2 + 1] > dist:
                    Fy += self.UniDistLoadMag[i] * dif
                elif self.UniDistLoadLoc[i * 2] < dist and self.UniDistLoadLoc[i * 2 + 1] > dist:
                    Fy += self.UniDistLoadMag[i] * (dist - self.UniDistLoadLoc[i * 2])
                else:
                    Fy += self.UniDistLoadMag[i] * (self.UniDistLoadLoc[i * 2 + 1] - (dist - dif))

        return Fy


    def shearSolve(self):
        dif = self.length/self.numSections

        if self.PointLoadLoc[0] == 0:
            if self.supportLoc[0] == 0:
                FyUpTo = self.PointLoadMag[0] + self.supportMag[0]
            else:
                FyUpTo = self.PointLoadMag[0]
        else:
            if self.supportLoc[0] == 0:
                FyUpTo = self.supportMag[0]
            else:
                FyUpTo = 0

        self.shear.append(FyUpTo)

        distUpTo = 0
        for i in range(self.numSections):
            distUpTo += dif
            FyUpTo = self.GetFyChange(distUpTo, dif) + FyUpTo
            self.shear.append(FyUpTo)

    def solve(self):
        self.Reactions()
        self.shearSolve()
        self.MomentSolve()

    def plotShear(self):
        dif = self.length/self.numSections
        X = np.arange(0, self.length + dif, dif)

        layoutShear = go.Layout(title = {'text': 'Shear Force Diagram'},
            yaxis = dict(title = 'Shear Force (kN)'),
            xaxis = dict(title = 'Distance (m)', range = [-1,self.length+1]),
            showlegend = False,
            )

        lineShear = go.Scatter(
            x = X,
            y = self.shear,
            mode = 'lines',
            name = 'Shear Force',
            fill = 'tonexty',
            line_color = 'green',
            fillcolor = 'rgba(0,255,0,0.1)',
            )

        axis  = go.Scatter(
            x = [0,self.length],
            y = [0,0],
            mode = 'lines',
            line_color = 'black'
            )

        figShear = go.Figure(data=[lineShear,axis], layout=layoutShear)
        figShear.show()

    def plotMoment(self):
        dif = self.length/self.numSections
        X = np.arange(0, self.length + dif, dif)

        layoutMoment = go.Layout(title = {'text': 'Bending Moment Diagram'},
            yaxis = dict(title = 'Bending Moment (kN m)'),
            xaxis = dict(title = 'Distance (m)', range = [-1,self.length+1]),
            showlegend = False,
            )

        lineMoment = go.Scatter(
            x = X,
            y = self.moment,
            mode = 'lines',
            name = 'Bending Moment',
            fill = 'tonexty',
            line_color = 'red',
            fillcolor = 'rgba(255,0,0,0.1)',
            )

        axis  = go.Scatter(
            x = [0,self.length],
            y = [0,0],
            mode = 'lines',
            line_color = 'black'
            )

        figMoment = go.Figure(data=[lineMoment,axis], layout=layoutMoment)
        figMoment.show()


B = Beam()
B.length = 5

B.supportLoc = [1,4]

B.PointLoadLoc = [5]
B.PointLoadMag = [-100]

B.UniDistLoadMag = [-10]
B.UniDistLoadLoc = [0, 5]

B.solve()

print(B.supportMag)
B.plotShear()
B.plotMoment()
