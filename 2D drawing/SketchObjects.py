from math import sqrt

class Point:
    def __init__(self, canvas, cords):
        self.canvas = canvas
        self.x = cords[0]
        self.y = cords[1]
        self.selected = False
        self.color = 'black'
        self.item = canvas.create_oval(self.x -2, self.y -2, self.x +2, self.y +2, fill=self.color)

        self.constraints = []

        self.connectedLines = []
        self.pointIDLine = []

class Line:
    def __init__(self, canvas, p1, p2):
        self.canvas = canvas
        self.x1, self.y1 = p1.x, p1.y
        self.x2, self.y2 = p2.x, p2.y
        self.selected = False
        self.color = 'gray'
        self.item = canvas.create_line(self.x1, self.y1, self.x2, self.y2, width=2, fill="black")
        self.constraints = []

    def length(self):
        return sqrt((self.x2 - self.x1)**2 + (self.y2 - self.y1)**2)