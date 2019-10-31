import graphics.screen
import graphics.face
import graphics.vertex

class Engine3D:
    def writePoints(self, points):
        self.points = []
        for point in points:
            self.points.append(graphics.vertex.Vertex(point))
            
    def writeTriangles(self, triangles):
        self.triangles = []
        for triangle in triangles:
            if len(triangle) != 4:
                triangle.append('gray')
            self.triangles.append(graphics.face.Face(triangle))
            
    def __init__(self, points, triangles, width=1000, height=700, distance=6, scale=100, title='3D', background='white'):
        #object parameters
        self.distance = distance
        self.scale = scale

        #initialize display
        self.screen = graphics.screen.Screen(width, height, title, background)

        #store coordinates
        self.writePoints(points)

        #store faces
        self.writeTriangles(triangles)

    def clear(self):
        #clear display
        self.screen.clear()

    def rotate(self, axis, angle):
        #rotate model around axis
        for point in self.points:
            point.rotate(axis, angle)

    def render(self):
        #calculate flattened coordinates (x, y)
        points = []
        for point in self.points:
            points.append(point.flatten(self.scale, self.distance))

        #get coordinates to draw triangles
        triangles = []
        for triangle in self.triangles:
            avgZ = -(self.points[triangle.a].z + self.points[triangle.b].z + self.points[triangle.c].z) / 3
            triangles.append((points[triangle.a], points[triangle.b], points[triangle.c], triangle.color, avgZ))

        #sort triangles from furthest back to closest
        triangles = sorted(triangles,key=lambda x: x[4])

        #draw triangles
        for triangle in triangles:
            self.screen.createTriangle(triangle[0:3], triangle[3])
