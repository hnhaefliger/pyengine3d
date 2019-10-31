import graphics.screen
import graphics.face
import graphics.vertex

class Engine3D:
    def __resetDrag(self, event):
        self.__prev = []
    
    def __drag(self, event):
        if self.__prev:
            self.rotate('y', (event.x - self.__prev[0]) / 20)
            self.rotate('x', (event.y - self.__prev[1]) / 20)
            self.clear()
            self.render()
        self.__prev = [event.x, event.y]
        
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
        self.screen.window.bind('<B1-Motion>', self.__drag)
        self.__prev = []
        self.screen.window.bind('<ButtonRelease-1>', self.__resetDrag)
        
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
