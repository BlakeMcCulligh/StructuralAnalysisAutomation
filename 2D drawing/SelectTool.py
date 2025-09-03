import numpy as np

from SketchObjects import ListPoints, ListLines
from math import sqrt

def shortest_distance_point_to_line(p1, p2, p3):
    """
    Calculates the shortest distance between a point and an infinite line.

    Args:
        p1 (np.array): A 2D or 3D numpy array representing the first point on the line.
        p2 (np.array): A 2D or 3D numpy array representing the second point on the line.
        p3 (np.array): A 2D or 3D numpy array representing the point whose distance
                       to the line is being calculated.

    Returns:
        float: The shortest distance between the point and the line.
    """
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)

    # Vector representing the line direction
    line_direction = p2 - p1

    # Vector from p1 to p3
    p1_to_p3 = p3 - p1

    # Calculate the projection of p1_to_p3 onto line_direction
    # This gives the scalar 't' in the parametric equation of the line
    # (p1 + t * line_direction)
    t = np.dot(p1_to_p3, line_direction) / np.dot(line_direction, line_direction)

    # Calculate the closest point on the line to p3
    closest_point_on_line = p1 + t * line_direction

    # Calculate the distance between p3 and the closest point on the line
    distance = np.linalg.norm(p3 - closest_point_on_line)

    return distance

def click(canvas, x, y):
    selected = clickOnlyPoint(canvas, x, y)
    if selected is None:
        clickOnlyLine(canvas, x, y)

def clickOnlyLine(canvas, x, y):
    for i in range(len(ListLines)):
        dist = shortest_distance_point_to_line([ListLines[i].p1.Xold, ListLines[i].p1.Yold], [ListLines[i].p2.Xold, ListLines[i].p2.Yold],
                                               [x, y])
        if dist < 5:
            ListLines[i].select(canvas)
            return ListLines[i]
    return None

def clickOnlyPoint(canvas, x, y):
    for i in range(len(ListPoints)):
        difx = abs(ListPoints[i].Xold - x)
        dify = abs(ListPoints[i].Yold - y)

        dist = sqrt((difx) ** 2 + (dify) ** 2)

        if dist < 5:
            ListPoints[i].select(canvas)
            return ListPoints[i]
    return None


