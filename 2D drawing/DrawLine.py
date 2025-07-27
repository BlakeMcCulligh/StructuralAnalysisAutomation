from SketchObjects import Point
from SketchObjects import Line

p1 = None
p2 = None

def draw(window, canvas, x, y):
    global p1
    global p2

    if p1 is None:
        p1 = Point(canvas, (x, y))
    else:
        p2 = Point(canvas, (x, y))

        newLine = Line(canvas, p1, p2)
        window.listLines.append(newLine)
        p1.connectedLines.append(newLine)
        p2.connectedLines.append(newLine)
        p1.pointIDLine.append(0)
        p2.pointIDLine.append(1)

        window.listPoints.append(p1)
        window.listPoints.append(p2)

        p1 = None
        p2 = None

def exitDrawLine(canvas):
    global p1
    global p2

    if p1 is not None:
        canvas.delete(p1.item)
        p1 = None
