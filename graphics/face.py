class Face:
    def __init__(self, vertices):
        #store point indexes
        self.points = vertices[:-1]
        self.color = vertices[-1]
