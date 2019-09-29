import math

def projectPoint(point, height, distance, scale):
    (x, y, z) = (point[0], point[1], point[2])
    projectedY = int(height / 2 + ((y * distance) / (z + distance)) * scale)
    projectedX = int(width / 2 + ((x * distance) / (z + distance)) * scale)
    return (projectedX, projectedY)

def rotateY(point, angle):
    angle = angle / 450 * 180 / math.pi
    sqrt2 = math.sqrt(2)
    newA = point[0] * math.cos(angle) - point[1] * math.sin(angle)
    newB = point[1] * math.cos(angle) + point[0] * math.sin(angle)
    return (newA, newB)
