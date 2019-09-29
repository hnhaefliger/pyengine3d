import tkinter, math

class Engine3D:
    def __init__(self, points, triangles, width=1000, height=700, distance=6, scale=100):
        self.width = width
        self.height = height
        self.distance = distance
        self.scale = scale
        
        self.window = tkinter.Tk()
        self.window.title('3D')
        self.image = tkinter.Canvas(self.window, width=self.width, height=self.height, bg='White')
        self.image.pack()

        self.points = points
        self.triangles = triangles

    def rotateZ(self, angle):
        angle = angle / 450 * 180 / math.pi
        sqrt2 = math.sqrt(2)
        for i, point in enumerate(self.points):
            newX = point[0] * math.cos(angle) - point[1] * math.sin(angle)
            newY = point[1] * math.cos(angle) + point[0] * math.sin(angle)
            newZ = point[2]
            self.points[i] = (newX, newY, newZ)

    def rotateX(self, angle):
        angle = angle / 450 * 180 / math.pi
        sqrt2 = math.sqrt(2)
        for i, point in enumerate(self.points):
            newX = point[0]
            newY = point[1] * math.cos(angle) - point[2] * math.sin(angle)
            newZ = point[2] * math.cos(angle) + point[1] * math.sin(angle)
            self.points[i] = (newX, newY, newZ)

    def rotateY(self, angle):
        angle = angle / 450 * 180 / math.pi
        sqrt2 = math.sqrt(2)
        for i, point in enumerate(self.points):
            newX = point[0] * math.cos(angle) - point[2] * math.sin(angle)
            newY = point[1]
            newZ = point[2] * math.cos(angle) + point[0] * math.sin(angle)
            self.points[i] = (newX, newY, newZ)
    
    def createTriangle(self, points, color):
        a, b, c = points[0], points[1], points[2]
        coords = [a[0], a[1], b[0], b[1], c[0], c[1]]
        self.image.create_polygon(coords, fill=color, outline="black")
        
    def projectPoint(self, point):
        (x, y, z) = (point[0], point[1], point[2])
        projectedY = int(self.height / 2 + ((y * self.distance) / (z + self.distance)) * self.scale)
        projectedX = int(self.width / 2 + ((x * self.distance) / (z + self.distance)) * self.scale)
        return (projectedX, projectedY)

    def clear(self):
        self.image.delete('all')

    def render(self, color='white'):
        coords = []
        triangles = []
        
        for point in self.points:
            coords.append(self.projectPoint(point))
            
        for triangle in self.triangles:
            avgZ = -(self.points[triangle[0]][2] + self.points[triangle[1]][2] + self.points[triangle[2]][2]) / 3
            triangles.append((coords[triangle[0]], coords[triangle[1]], coords[triangle[2]], avgZ))

        triangles = sorted(triangles,key=lambda x: x[3])

        for triangle in triangles:
            self.createTriangle(triangle, color)