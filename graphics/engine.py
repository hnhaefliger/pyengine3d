import graphics.screen
import graphics.face
import graphics.vertex

class Engine3D:
    def __init__(self, points, triangles, width=1000, height=700, distance=6, scale=100):
        #object parameters
        self.distance = distance
        self.scale = scale

        #initialize display
        self.screen = graphics.screen.Screen(width, height)

        #store coordinates
        self.points = []
        for point in points:
            self.points.append(graphics.vertex.Vertex(point))

        #store faces
        self.triangles = []
        for triangle in triangles:
            self.triangles.append(graphics.face.Face(triangle))

    def clear(self):
        #clear display
        self.screen.clear()

    def rotate(self, axis, angle):
        #rotate model around axis
        for point in self.points:
            point.rotate(axis, angle)

    def render(self, color='white'):
        #calculate flattened coordinates (x, y)
        points = []
        for point in self.points:
            points.append(point.flatten(self.scale, self.distance))

        #get coordinates to draw triangles
        triangles = []
        for triangle in self.triangles:
            avgZ = -(self.points[triangle.a].z + self.points[triangle.b].z + self.points[triangle.c].z) / 3
            triangles.append((points[triangle.a], points[triangle.b], points[triangle.c], avgZ))

        #sort triangles from furthest back to closest
        triangles = sorted(triangles,key=lambda x: x[3])

        #draw triangles
        for triangle in triangles:
            self.screen.createTriangle(triangle, color)
