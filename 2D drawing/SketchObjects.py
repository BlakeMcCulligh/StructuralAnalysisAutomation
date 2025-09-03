from math import sqrt

ListLines = []
ListPoints = []
ListSelected = []

class Point:
    def __init__(self, canvas, cords):
        self.canvas = canvas
        self.Xold = cords[0]
        self.Yold = cords[1]
        self.selected = False
        self.color = 'black'
        self.item = canvas.create_oval(self.Xold -2, self.Yold -2, self.Xold +2, self.Yold +2, fill=self.color)

        self.fixed = False
        self.connectedLines = []
        self.pointIDLine = []

        self.Xsolved = None
        self.Ysolved = None
        ListPoints.append(self)

    def select(self, canvas):
        if self.selected:
            self.selected = False
            self.color = "black"
            ListSelected.remove(self)
            canvas.itemconfig(self.item, fill=self.color, outline=self.color)
        else:
            self.selected = True
            self.color = "#ADD8E6"
            ListSelected.append(self)
            canvas.itemconfig(self.item, fill=self.color, outline=self.color)

class Line:
    def __init__(self, canvas, p1, p2):
        self.canvas = canvas
        self.p1 = p1
        self.p2 = p2
        self.selected = False
        self.color = 'gray'
        self.item = canvas.create_line(self.p1.Xold, self.p1.Yold, self.p2.Xold, self.p2.Yold, width=2, fill="black")
        ListLines.append(self)

        self.horizontal = False
        self.vertical = False
        self.ListEqual = []
        self.ListParallelIndex = []
        self.ListPerpendicularIndex = []
        self.ListColinearIndex = []
        self.ListCoincidencePIndex = []

    def length(self):
        return sqrt((self.p2.Xold - self.p1.Xold)**2 + (self.p2.Yold - self.p1.Yold)**2)

    def select(self, canvas):
        if self.selected:
            self.selected = False
            self.color = "black"
            ListSelected.remove(self)
            canvas.itemconfig(self.item, fill=self.color)
        else:
            self.selected = True
            self.color = "#ADD8E6"
            ListSelected.append(self)
            canvas.itemconfig(self.item, fill=self.color)