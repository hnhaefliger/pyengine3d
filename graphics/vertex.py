import math

class Vertex:
    def __init__(self, point):
        #store x, y, z coordinates
        (x,y,z) = point
        self.x = x
        self.y = y
        self.z = z

    def flatten(self, scale, distance):
        #calculate 2D coordinates from 3D point
        projectedY = int(((self.y * distance) / (self.z + distance)) * scale)
        projectedX = int(((self.x * distance) / (self.z + distance)) * scale)
        return (projectedX, projectedY)

    def rotate(self, axis, angle):
        #rotate point around axis
        angle = angle / 450 * 180 / math.pi
        sqrt2 = math.sqrt(2)
        if axis == 'z':
            #rotate aroud Z axis
            newX = self.x * math.cos(angle) - self.y * math.sin(angle)
            newY = self.y * math.cos(angle) + self.x * math.sin(angle)
            newZ = self.z
        elif axis == 'x':
            #rotate around X axis
            newY = self.y * math.cos(angle) - self.z * math.sin(angle)
            newZ = self.z * math.cos(angle) + self.y * math.sin(angle)
            newX = self.x
        elif axis == 'y':
            #rotate around Y axis
            newX = self.x * math.cos(angle) - self.z * math.sin(angle)
            newZ = self.z * math.cos(angle) + self.x * math.sin(angle)
            newY = self.y
        else:
            raise ValueError('not a valid axis')
        self.x = newX
        self.y = newY
        self.z = newZ

