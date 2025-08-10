from math import sqrt
from SketchObjects import Line, Point, ListLines, ListPoints
import SelectTool
ListRelations = []
ListDimentions = []

class Relation:

    def __init__(self, p1, p2):
        self.Line = None
        self.p1 = p1
        self.p2 = p2
        self.a = None
        self.b = None
        self.t = None
        self.p1Set = False
        self.p2Set = False
        self.slopeTiesIndex = []
        self.slopeInverseTiesIndex = []
        self.LengthTiesIndex = []

    def setP(self, pIndex):
        if pIndex == 1:
            self.p1Set = True
            self.p1.XSolved = self.p1.xOld
            self.p1.YSolved = self.p1.yOld
        else:
            self.p2Set = True
            self.p2.XSolved = self.p2.xOld
            self.p2.YSolved = self.p2.yOld
        self.checkSolve()

    def setLine(self, xChange, yChange):
        L = sqrt(xChange ** 2 + yChange ** 2)
        self.a = xChange / L
        self.b = yChange / L
        self.checkSolve()

        for i in range(len(self.slopeTiesIndex)):
            ListRelations[self.slopeTiesIndex[i]].setLine(self.a, self.b)

        for i in range(len(self.slopeInverseTiesIndex)):
            ListRelations[self.slopeInverseTiesIndex[i]].setLine(self.b, self.a)

    def setLength(self, t):
        self.t = t
        self.checkSolve()

        for i in range(len(self.LengthTiesIndex)):
            ListRelations[self.LengthTiesIndex[i]].setLength(self.t)


    def checkSolve(self):
        global ListRelations
        if self.K is not None and self.a is not None and self.b is not None:
            if self.p1Set:
                self.p2.Xsolved = self.p1.Xsolved + self.a * self.t
                self.p2.Ysolved = self.p1.Ysolved + self.b * self.t

                for j in range(len(ListRelations)):
                    if ListRelations[j].p1.Index == self.p2.index:
                        ListRelations[j].setP(1)
                    elif ListRelations[j].p2.Index == self.p2.index:
                        ListRelations[j].setP(2)
            elif self.p2Set:
                self.p1.Xsolved = self.p2.Xsolved - self.a * self.t
                self.p1.Ysolved = self.p2.Ysolved - self.b * self.t
                for j in range(len(ListRelations)):
                    if ListRelations[j].p1.Index == self.p1.index:
                        ListRelations[j].setP(1)
                    elif ListRelations[j].p2.Index == self.p1.index:
                        ListRelations[j].setP(2)

def setRelations():
    global ListRelations
    for i in range(len(ListLines)):
        NewRelation = Relation(ListLines[i].p1, ListLines[i].p2)
        NewRelation.Line = ListLines[i]
        ListRelations.append(NewRelation)
        ListLines[i].relationIndex = len(ListRelations) -1

    # vertical and horizontal
    for i in range(len(ListRelations)):

        if ListRelations[i].Line.horrizontal:
            ListRelations[i].setLine(1, 0)

        elif ListRelations[i].Line.vertical:
            ListRelations[i].setLine(0, 1)

    # parallel and perpendicular
    for i in range(len(ListRelations)):

        for j in range(len(ListRelations[i].Line.ListParallelIndex)):
            ListRelations[i].slopeTiesIndex.append(ListRelations[i].Line.ListParallelIndex[j])

        for j in range(len(ListRelations[i].Line.ListPerpendicularIndex)):
            ListRelations[i].slopeInverseTiesIndex.append(ListRelations[i].Line.ListPerpendicularIndex[j])

    # equal
    for i in range(len(ListRelations)):
        for j in range(len(ListRelations[i].Line.ListEqual)):
            ListRelations[i].lengthTieIndex.append(ListRelations[i].Line.ListEqual[j])

    # colinear
    for i in range(len(ListLines)):
        for j in range(len(ListLines[i].listColinearIndex)):
            NewRelation = Relation(ListLines[i].p2, ListLines[ListLines[i].listColinearIndex[i]].p1)
            ListRelations.append(NewRelation)
            ListRelations[ListLines[i].relationIndex].slopeTiesIndex.append(ListLines[ListLines[i].listColinearIndex[i]].relationIndex)
            ListRelations[ListLines[i].relationIndex].slopeTiesIndex.append(len(ListRelations)-1)
            ListRelations[ListLines[ListLines[i].listColinearIndex[i]].relationIndex].slopeTiesIndex.append(ListLines[i].relationIndex)
            ListRelations[ListLines[ListLines[i].listColinearIndex[i]].relationIndex].slopeTiesIndex.append(len(ListRelations))

    # Coincidence
    for i in range(len(ListLines)):
        for j in range(len(ListLines[i].listCoincidencePIndex)):
            NewRelation = Relation(ListLines[i].p1, ListPoints[ListLines[i].listCoincidencePIndex])
            ListRelations.append(NewRelation)
            ListRelations[ListLines[i].relationIndex].slopeTiesIndex.append(len(ListRelations))

    # Dimentions
    for i in range(len(ListDimentions)):

        for j in range(len(ListRelations)):
            if ListRelations[j].p1.Index == ListDimentions[i].p1Index:
                if ListRelations[j].p2.Index == ListDimentions[i].p2Index:
                    ListRelations[j].setLength(ListDimentions[i].length)
            elif ListRelations[j].p1.Index == ListDimentions[i].p2Index:
                if ListRelations[j].p2.Index == ListDimentions[i].p1Index:
                    ListRelations[j].setLength(ListDimentions[i].length)

    for i in range(len(ListPoints)):
        if ListPoints[i].fixed:
            for j in range(len(ListRelations)):
                if ListRelations[j].p1.Index == i:
                    ListRelations[j].setP(1)
                elif ListRelations[j].p2.Index == i:
                    ListRelations[j].setP(2)

def addHorizontal(canvas, x, y):
    line = SelectTool.clickOnlyLine(canvas, x, y)
    line.horizontal = True
    line.vertical = False
    line.select(canvas)
    print("Horizontal")

def addVertical(canvas, x, y):
    line = SelectTool.clickOnlyLine(canvas, x, y)
    line.horizontal = False
    line.vertical = True
    line.select(canvas)
    print("Veritcal")

l1 = None
p1 = None

def addParallel(canvas, x, y):
    global l1
    if l1 is None:
        l1 = SelectTool.clickOnlyLine(canvas, x, y)
    else:
        l2 = SelectTool.clickOnlyLine(canvas, x, y)
        if l1 != l2:
            i1 = ListLines.index(l1)
            i2 = ListLines.index(l2)
            l1.ListParallelIndex.append(i2)
            l2.ListParallelIndex.append(i1)
            l1.select(canvas)
            l2.select(canvas)
            l1 = None
        else:
            l1.select(canvas)

def addPerpendicualer(canvas, x, y):
    global l1
    if l1 is None:
        l1 = SelectTool.clickOnlyLine(canvas, x, y)
    else:
        l2 = SelectTool.clickOnlyLine(canvas, x, y)
        if l1 != l2:
            i1 = ListLines.index(l1)
            i2 = ListLines.index(l2)
            l1.ListPerpendicularIndex.append(i2)
            l2.ListPerpendicularIndex.append(i1)
            l1.select(canvas)
            l2.select(canvas)
            l1 = None
        else:
            l1.select(canvas)

def addEqual(canvas, x, y):
    a=1

def addColinear(canvas, x, y):
    a=1

def addCoincidence(canvas, x, y):
    a=1

def addDimentions(canvas, x, y):
    a=1

def addFixed(canvas, x, y):
    a=1