import tkinter

class Engine3D:
    def __init__(self, points, triangles, width=1000, height=700, distance=6, scale=100):
        self.width = width
        self.height = height
        self.distance = distance
        self.scale = scale
        
        self.window = tkinter.Tk()
        self.image = tkinter.Canvas(self.window, width=self.width, height=self.height, bg='White')
        self.image.pack()
        
        self.shapes = []
        self.points = points
        self.triangles = triangles

    def __createTriangle(self, points):
        a, b, c = points[0], points[1], points[2]
        coords = [a[0], a[1], b[0], b[1], c[0], c[1]]
        self.shapes.append(self.image.create_polygon(coords, fill="", outline="black"))
        
    def __projectPoint(self, point):
        (x, y, z) = (point[0], point[1], point[2])
        projectedY = int(self.height / 2 + ((y * self.distance) / (z + self.distance)) * self.scale)
        projectedX = int(self.width / 2 + ((x * self.distance) / (z + self.distance)) * self.scale)
        return (projectedX, projectedY)

    def __clear(self):
        for triangle in self.shapes:
            self.image.delete(triangle)

    def render(self):
        self.__clear()
        coords = []
        for point in self.points:
            coords.append(self.__projectPoint(point))
            
        for triangle in self.triangles:
            self.__createTriangle((coords[triangle[0]], coords[triangle[1]], coords[triangle[2]]))

        print('rendered')
        self.window.after(1000, self.render)


points = [(-1,-1,-1),(-1,-1,1),(-1,1,1),(-1,1,-1),(1,-1,-1),(1,-1,1),(1,1,1),(1,1,-1)]
triangles = [(0,1,2),(0,2,3),(2,3,7),(2,7,6),(1,2,5),(2,5,6),(0,1,4),(1,4,5),(4,5,6),(4,6,7)]
test = Engine3D(points, triangles)
test.render()
