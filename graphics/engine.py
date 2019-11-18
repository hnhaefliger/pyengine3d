import graphics.screen
import graphics.face
import graphics.vertex

class Engine3D:
    def __resetDrag(self, event):
        #reset mouse drag handler
        self.__dragprev = []
    
    def __drag(self, event):
        #handler for mouse drag event
        if self.__dragprev:
            self.rotate('y', (event.x - self.__dragprev[0]) / 20)
            self.rotate('x', (event.y - self.__dragprev[1]) / 20)
            self.clear()
            self.render()
        self.__dragprev = [event.x, event.y]

    def __keypress(self, event):
        #handler for keyboard events
        if event.keysym == 'Up':
            self.rotate('x', -0.5)
        elif event.keysym == 'Down':
            self.rotate('x', 0.5)
        elif event.keysym == 'Right':
            self.rotate('y', 0.5)
        elif event.keysym == 'Left':
            self.rotate('y', -0.5)
        elif event.keysym == 'period':
            self.scale += 1
        elif event.keysym == 'comma' and self.scale > 1:
            self.scale -= 1
        self.clear()
        self.render()
        
    def writePoints(self, points):
        #set object points
        self.points = []
        for point in points:
            self.points.append(graphics.vertex.Vertex(point))
            
    def writeShapes(self, shapes):
        #set object shapes
        self.shapes = []
        for shape in shapes:
            if type(shape[-1]) != str:
                shape.append('gray')
            self.shapes.append(graphics.face.Face(shape))
            
    def __init__(self, points, shapes, width=1000, height=700, distance=6, scale=100, title='3D', background='white'):
        #object parameters
        self.distance = distance
        self.scale = scale

        #initialize display
        self.screen = graphics.screen.Screen(width, height, title, background)
        self.screen.window.bind('<B1-Motion>', self.__drag)
        self.__dragprev = []
        self.screen.window.bind('<ButtonRelease-1>', self.__resetDrag)
        self.screen.window.bind_all('<Key>', self.__keypress)
        
        #store coordinates
        self.writePoints(points)

        #store faces
        self.writeShapes(shapes)

    def rotate(self, axis, angle):
        #rotate model around axis
        for point in self.points:
            point.rotate(axis, angle)

    def render(self):
        #calculate flattened coordinates (x, y)
        points = []
        for point in self.points:
            points.append(point.flatten(self.scale, self.distance))

        #get coordinates to draw shapes
        shapes = []
        for shape in self.shapes:
            avgZ = 0
            temp = []
            for point in shape.points:
                avgZ -= self.points[point].z
                temp.append(points[point])
            temp.append(shape.color)
            temp.append(avgZ / len(shape.points))
            shapes.append(temp)
            
        #sort shapes from furthest back to closest
        shapes = sorted(shapes, key=lambda x: x[-1])
        
        #draw shapes
        for shape in shapes:
            self.screen.createShape(shape[0:-2], shape[-2])

    def clear(self):
        #clear display
        self.screen.clear()

    def after(self, time, function):
        #call tk.Tk's after() method
        self.screen.after(time, function)

    def mainloop(self):
        #call tk.Tk's mainloop() method
        self.screen.mainloop()
