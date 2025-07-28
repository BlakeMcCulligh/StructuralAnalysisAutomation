from SketchObjects import ListPoints, ListLines
from math import sqrt

def click(canvas, x, y):

    for i in range(len(ListPoints)):
        difx = abs(ListPoints[i].Xold - x)
        dify = abs(ListPoints[i].Yold - y)

        dist = sqrt((difx) ** 2 + (dify) ** 2)

        if dist < 5:
            ListPoints[i].select(canvas)