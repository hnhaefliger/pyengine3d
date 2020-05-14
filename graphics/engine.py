import graphics.screen
import graphics.face
import graphics.vertex
import copy

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

    def __select(self, event):
        zeros = self.screen.zeros
        event = (event.x - zeros[0], event.y - zeros[1])
            
        possibilities = []
        for a in range(-6, 5):
            for b in range(-6, 5):
                possibilities.append((event[0] + a, event[1] + b))

        found = [e for e in possibilities if e in self.flattened]
        if found != []:
            self.__moveaxis = None
            self.__selected = self.flattened.index(found[0])

            i = self.points[self.__selected]
            self.__axis = [[copy.deepcopy(i) for a in range(2)] for b in range(3)]
            
            self.__axis[0][0].x -= 40 / self.scale
            self.__axis[0][1].x += 40 / self.scale
            self.__axis[1][0].y -= 40 / self.scale
            self.__axis[1][1].y += 40 / self.scale
            self.__axis[2][0].z -= 40 / self.scale
            self.__axis[2][1].z += 40 / self.scale
            
            self.__axis = [[point.flatten(self.scale, self.distance) for point in i] for i in self.__axis]
            self.__axis = [[[i[0] + zeros[0], i[1] + zeros[1]] for i in j] for j in self.__axis]
            self.__axis = [self.screen.createLine(self.__axis[0], 'red'), self.screen.createLine(self.__axis[1], 'green'), self.screen.createLine(self.__axis[2], 'blue')]

    def __selectx(self, event):
        self.__moveaxis = 'x'

    def __selecty(self, event):
        self.__moveaxis = 'y'

    def __selectz(self, event):
        self.__moveaxis = 'z'

    def __moveup(self, event):
        if self.__selected != None and self.__moveaxis != None:
            self.points[self.__selected].move(self.__moveaxis, 0.1)
            self.clear()
            self.render()

    def __movedown(self, event):
        if self.__selected != None and self.__moveaxis != None:
            self.points[self.__selected].move(self.__moveaxis, -0.1)
            self.clear()
            self.render()

    def __zoomin(self, event):
        self.scale += 2.5
        self.clear()
        self.render()

    def __zoomout(self, event):
        self.scale -= 2.5
        self.clear()
        self.render()

    def __deselect(self, event):
        if self.__selected != None:
            self.__selected = None
            self.__axis = [self.screen.delete(line) for line in self.__axis]
            self.__moveaxis = None

    def __cameraleft(self, event):
        self.screen.zeros[0] -= 5
        self.clear()
        self.render()

    def __cameraright(self, event):
        self.screen.zeros[0] += 5
        self.clear()
        self.render()

    def __cameraup(self, event):
        self.screen.zeros[1] -= 5
        self.clear()
        self.render()

    def __cameradown(self, event):
        self.screen.zeros[1] += 5
        self.clear()
        self.render()
        
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

        self.screen.window.bind('<Up>', self.__zoomin)
        self.screen.window.bind('<Down>', self.__zoomout)
        self.screen.window.bind('w', self.__cameraup)
        self.screen.window.bind('s', self.__cameradown)
        self.screen.window.bind('a', self.__cameraleft)
        self.screen.window.bind('d', self.__cameraright)

        # this is for editing the model
        self.__selected = None
        self.__axis = []
        self.__moveaxis = None
        self.screen.window.bind('<ButtonPress-3>', self.__select)
        self.screen.window.bind('<ButtonRelease-3>', self.__deselect)
        self.screen.window.bind('x', self.__selectx)
        self.screen.window.bind('y', self.__selecty)
        self.screen.window.bind('z', self.__selectz)
        self.screen.window.bind('<Left>', self.__movedown)
        self.screen.window.bind('<Right>', self.__moveup)
        
        #store coordinates
        self.writePoints(points)
        self.flattened = []

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
        self.flattened = []
        for point in self.points:
            self.flattened.append(point.flatten(self.scale, self.distance))

        #get coordinates to draw triangles
        triangles = []
        for triangle in self.triangles:
            avgZ = -(self.points[triangle.a].z + self.points[triangle.b].z + self.points[triangle.c].z) / 3
            triangles.append((self.flattened[triangle.a], self.flattened[triangle.b], self.flattened[triangle.c], triangle.color, avgZ))

        #sort triangles from furthest back to closest
        triangles = sorted(triangles,key=lambda x: x[4])

        #draw triangles
        for triangle in triangles:
            self.screen.createTriangle(triangle[0:3], triangle[3])
