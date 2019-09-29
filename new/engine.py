import display
import algebra
import random

class Mesh:
    def __init__(self, coords, color):
        self.a = coords[0]
        self.b = coords[1]
        self.c = coords[2]
        self.color = color

points = [(-1,-1,-1),(-1,-1,1),(-1,1,1),(-1,1,-1),(1,-1,-1),(1,-1,1),(1,1,1),(1,1,-1)]
triangles = [(0,1,2),(0,2,3), (2,3,7),(2,7,6), (1,2,5),(2,5,6), (0,1,4),(1,4,5), (4,5,6),(4,6,7), (3,7,4),(4,3,0)]

screen = display.Screen(800, 600)

class Engine:
    def __init__(self, points, triangles, width=800, height=600):
        self.diplay = display.Screen(width, height)

        self.points = points
        self.meshes = []
        colors = ['red', 'blue', 'green']
        for triangle in triangles:
            self.meshes.append(Mesh(triangle, colors[random.randint(0, len(colors)-1)]))

    def render(self):
        points = []
        for point in self.points:
            algebra.projectPoint(point, 
        for mesh in self.meshes:
            
