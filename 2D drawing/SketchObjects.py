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
        self.selectedIndex = None
        self.color = 'black'
        self.item = canvas.create_oval(self.Xold -2, self.Yold -2, self.Xold +2, self.Yold +2, fill=self.color)

        self.constraints = []

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
            self.selectedIndex = None
            canvas.itemconfig(self.item, fill=self.color, outline=self.color)
        else:
            self.selected = True
            self.color = "#ADD8E6"
            self.selectedIndex = len(ListSelected)
            ListSelected.append(self)
            canvas.itemconfig(self.item, fill=self.color, outline=self.color)

class Line:
    def __init__(self, canvas, p1, p2):
        self.canvas = canvas
        self.x1, self.y1 = p1.Xold, p1.Yold
        self.x2, self.y2 = p2.Xold, p2.Yold
        self.selected = False
        self.color = 'gray'
        self.item = canvas.create_line(self.x1, self.y1, self.x2, self.y2, width=2, fill="black")
        self.constraints = []
        ListLines.append(self)

    def length(self):
        return sqrt((self.x2 - self.x1)**2 + (self.y2 - self.y1)**2)