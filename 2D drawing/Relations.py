from math import sqrt
from turtledemo.sorting_animate import start_ssort

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
        if self.t is not None and self.a is not None and self.b is not None:
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
        print("checking horizontal and vertical")
        if ListRelations[i].Line.horizontal:
            print("set Horizonatl")
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
        for j in range(len(ListLines[i].ListColinearIndex)):
            NewRelation = Relation(ListLines[i].p2, ListLines[ListLines[i].listColinearIndex[i]].p1)
            ListRelations.append(NewRelation)
            ListRelations[ListLines[i].relationIndex].slopeTiesIndex.append(ListLines[ListLines[i].listColinearIndex[i]].relationIndex)
            ListRelations[ListLines[i].relationIndex].slopeTiesIndex.append(len(ListRelations)-1)
            ListRelations[ListLines[ListLines[i].listColinearIndex[i]].relationIndex].slopeTiesIndex.append(ListLines[i].relationIndex)
            ListRelations[ListLines[ListLines[i].listColinearIndex[i]].relationIndex].slopeTiesIndex.append(len(ListRelations))

    # Coincidence
    for i in range(len(ListLines)):
        for j in range(len(ListLines[i].ListCoincidencePIndex)):
            NewRelation = Relation(ListLines[i].p1, ListPoints[ListLines[i].ListCoincidencePIndex])
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
    SelectTool.clickOnlyLine(canvas, x, y).horizontal = True
    SelectTool.clickOnlyLine(canvas, x, y).vertical = False
    SelectTool.clickOnlyLine(canvas, x, y).select(canvas)
    RelationAdded()
    print("Horizontal")

def addVertical(canvas, x, y):
    SelectTool.clickOnlyLine(canvas, x, y).horizontal = False
    SelectTool.clickOnlyLine(canvas, x, y).vertical = True
    SelectTool.clickOnlyLine(canvas, x, y).select(canvas)
    RelationAdded()
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
    RelationAdded()

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
    RelationAdded()

def addEqual(canvas, x, y):
    a=1
    RelationAdded()

def addColinear(canvas, x, y):
    a=1
    RelationAdded()

def addCoincidence(canvas, x, y):
    a=1
    RelationAdded()

def addDimentions(canvas, x, y):
    a=1
    RelationAdded()

def addFixed(canvas, x, y):
    a=1
    RelationAdded()

def RelationAdded():
    a=1
#def RelationAdded(Relation):
    # check if ether point in Relation is defined.
        # if both are check to see if the HardCord or one of the points needs to be changed to make the new relation valid
            # if one does need to be chhange delete Relation and send overdefined mesage
            # if nether does do nothing
        # if one is make sure the other point has a valid location, due to restraints form other points



# using of groupings
# each grouping has all points defined relative to a singular point in the grouping, witch is the one ether in index one, or if fixed
class Relation:
    def __init__(self, a, b, t):
        self.a = a
        self.b = b
        self.t = t

class GroupRealtion:
    def __init__(self, group, pOld, relation):
        self.group = group
        self.pOld = pOld
        self.pOldIndex = group.points.index(pOld)
        self.a = relation.a
        self.b = relation.b
        self.t = relation.t

class Grouping:
    def __init__(self, p1, p2, relation):
        self.points = [p1, p2]
        self.pCordsRelative = [[0,0],[relation.a*relation.t, relation.b*relation.t]]
        self.mainPoint = 0
        self.fixed = False
        self.mainPointCords = [p1.x, p1.y]
        self.checkFixed()

        self.pointsPartial = []
        self.pointsPartialRelation = []
        listGroups.append(self)
        self.redraw = False

    def checkFixed(self):
        for i in range(len(self.points)):
            if self.points[i].fixed:
                self.fixed = True
                self.mainPoint = i
                for j in range(len(self.points)):
                    if j != i:
                        self.pCordsRelative[j] = [self.pCordsRelative[j][0]-self.pCordsRelative[i][0], self.pCordsRelative[j][1]-self.pCordsRelative[i][1]]
                self.pCordsRelative[i][0] = 0
                self.pCordsRelative[i][1] = 0
                break

    def addPoint(self, pNew, pOld, relation):
        pOldIndex = self.points.index(pOld)
        self.points.append(pNew)
        self.pCordsRelative.append([self.pCordsRelative[pOldIndex][0] + relation.a*relation.t, self.pCordsRelative[pOldIndex][1] + relation.b*relation.t])
        if not self.fixed:
            self.checkFixed()

    def addPatialRelationPoint(self, pNew, pOld, relation):
        self.pointsPartial.append(pNew)
        groupRelation = GroupRealtion(self, pOld, relation)
        self.pointsPartialRelation.append(groupRelation)

    def conbineGroups(self, addedGroup, relation, pOld, pNew):
        pOldIndex = self.points.index(pOld)
        p = self.pCordsRelative[pOldIndex]
        pNewRelative = [p + relation.a*relation.t, p + relation.b*relation.t]
        for i in range(len(addedGroup.points)):
            self.points.append(addedGroup.points[i])
            self.pCordsRelative.append([addedGroup.pCordsRelative[0] - pNewRelative[0], addedGroup.pCordsRelative[1] - pNewRelative[1]])
        self.checkFixed()

    def redraw(self):
        self.redraw = True
        # redraws the group after something was changed in it

class PatialGroupingRelation:
    def __init__(self, relP1, relP2, a, b, t, object1, object2):
        self.relitvePoint1 = relP1
        self.relitvePoint2 = relP2
        self.a = a
        self.b = b
        self.t = t
        self.object1 = object1
        self.object2 = object2

    def hasObject(self, O):
        if O == self.object1 or O == self.object2:
            return True
        else:
            return False



class PartialGrouping:
    def __init__(self, object1, object2, relation, p1, p2):
        self.objects = [object1, object2]
        if object1 is Grouping:
            index1 = object1.points.index(p1)
            relP1 = object1.pCordsRelative[index1]
        else:
            relP1 = [0,0]
        if object2 is Grouping:
            index2 = object2.points.index(p2)
            relP2 = object2.pCordsRelative[index2]
        else:
            relP2 = [0,0]

        NewPartialRelation = PatialGroupingRelation(relP1, relP2, relation.a, relation.b, relation.t, object1, object2)
        self.PartialGroupingRelations = [NewPartialRelation]

    def desplySolve(self):

        # finding if there is a fixed object in the group
        iFixed = None
        for i in range(len(self.objects)):
            if self.objects[i].fixed:
                iFixed = i
                break
        # seting that object and redrawing it
        if iFixed is not None:
            self.objects[iFixed].redraw()
            self.redrawRecursive([iFixed])
        else:
            self.objects[0].redraw()
            self.redrawRecursive([0])

    def redrawRecursive(self, iPrevius):
        indeces = []
        for i in range(len(self.PartialGroupingRelations)):
            if self.PartialGroupingRelations[i].hasObject(self.objects[iPrevius]):
                    indeces.append(i)
        for i in range(len(indeces)):
            # get what object is not the preivius object
            # get that objects index
            # redraw that object
            # call self
            a =1



listGroups = []

def addHorizontal(canvas, x, y):
    print("Horizontal")
    p1 = SelectTool.clickOnlyLine(canvas, x, y).p1
    p2 = SelectTool.clickOnlyLine(canvas, x, y).p2

    # check for relation alredy between the 2 points

    relation = Relation(1,0,None)

    if p1.Group is not None and p2.Group is not None:
        a = 0
    elif p1.Group is not None:
        a = 0
    elif p2.Group is not None:
        a = 0
    else:
        a = 0


