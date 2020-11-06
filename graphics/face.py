class Face:
    def __init__(self, vertices):
        #store point indexes
        (a, b, c) = vertices
        self.a = a
        self.b = b
        self.c = c
        self.color = 'blue'

    def depth(self, points):
        return -(points[self.a].z + points[self.b].z + points[self.c].z) / 3