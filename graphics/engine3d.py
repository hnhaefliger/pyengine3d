from graphics.vertex import Vertex
from graphics.face import Face
#how to avoid this ?
from PySide2.QtCore import QPoint

#######################################################################################################################


class Triangle():
    def __init__(self, p1: list, p2: list, p3: list, color: int, depth: float):
        self.a = p1
        self.b = p2
        self.c = p3
        self.color = color
        self.depth = depth

    def set_color(self, color: int):
        self.color = color

    def depth(self):
        return self.depth

    def get_pts(self, pan: list):
        return [QPoint(self.a[0] + pan[0], self.a[1] + pan[1]),
                QPoint(self.b[0] + pan[0], self.b[1] + pan[1]),
                QPoint(self.c[0] + pan[0], self.c[1] + pan[1])]

    def inside(self, pt: list, pan: list):
        x, x1, x2, x3 = pt[0]-pan[0], self.a[0], self.b[0], self.c[0]
        y, y1, y2, y3 = pt[1]-pan[1], self.a[1], self.b[1], self.c[1]
        full   = abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
        first  = abs(x1 * (y2 - y) + x2 * (y - y1) + x * (y1 - y2))
        second = abs(x1 * (y - y3) + x * (y3 - y1) + x3 * (y1 - y))
        third  = abs(x * (y2 - y3) + x2 * (y3 - y) + x3 * (y - y2))
        return abs(first + second + third - full) < .0000001


########################################################################################################################
class Engine3D():
    def __init__(self, points: list, triangles: list, width=1000, height=700, distance=6, scale=100, title='3D',
                 background='black'):
        # object parameters
        super(Engine3D)
        self.background = background
        self.distance = distance
        self.scale = scale
        self.prev = []
        self.start_drag = False
        self.start_pan = False
        self.light_on = True
        # store coordinates
        self.points = []
        self.write_points(points)
        # store faces
        self.triangles = []
        self.write_triangles(triangles)
        #store flatten triangles
        self.flat_tri = []
        self.selected = []
        self.sp = [0, 0]
        self.pan = [width / 2, height / 2]

    ######################################################################################################################

    def write_points(self, points):
        self.points = list(map(lambda p: Vertex(p), points))

    def write_triangles(self, triangles):
        self.triangles = list(map(lambda t: Face(t), triangles))

    ######################################################################################################################
    ## engine API
    def clear(self):
        self.flat_tri = []

    def light(self):
        # crude lighting
        l = list(map(lambda t: t.depth, self.flat_tri))
        first = min(l)
        ratio = 255 / (max(l) - first)
        for i in self.flat_tri:
            i.set_color(ratio * (i.depth - first))

    def must_recompute(self):
        return len(self.get_flat_triangles()) == 0

    def get_flat_triangles(self):
        return self.flat_tri

    def render(self):
        # calculate flattened coordinates (x, y)
        flat = list(map(lambda p: (p.flatten(self.scale, self.distance)), self.points))
        # depth = list(map(lambda t: (t.depth(self.points)), self.triangles))
        # painter algo
        # flatten_triangles [[x,y],[x,y],[x,y],color, depth]
        self.flat_tri = sorted(map(lambda t:
                              Triangle(flat[t.a],
                               flat[t.b],
                               flat[t.c],
                               128,  # default color
                               t.depth(self.points)),
                              self.triangles), key=lambda x: x.depth)
        if self.light_on:
            self.light()

    def rotate(self, axis, angle):
        list(map(lambda p: p.rotate(axis, angle), self.points))

    def reset_drag(self):
        self.prev = []

    def reset_pan(self, x, y):
        self.sp = [x, y]


    def drag(self, x, y):
        if self.prev:
            self.rotate('y', (x - self.prev[0]) / 20)
            self.rotate('x', (y - self.prev[1]) / 20)
            self.clear()
        self.prev = [x, y]
        self.selected = []

    def pan(self, x, y):
        self.pan[0] += x - self.sp[0]
        self.pan[1] += y - self.sp[1]
        self.sp = [x, y]

    def zoom_in(self):
        self.scale += 5.0
        self.clear()
        self.selected = []

    def zoom_out(self):
        self.scale -= 5.0
        self.clear()
        self.selected = []

    def camera_left(self):
        # self.screen.zeros[0] -= 5
        self.clear()

    def camera_right(self):
        # self.screen.zeros[0] += 5
        self.clear()

    def light_toggle(self):
        self.light_on = not self.light_on
        self.clear()

    def select(self, pt: list):
        selected = list(filter(lambda t: t.inside(pt, self.pan), self.flat_tri))
        #only the last one
        if selected is None or len(selected) ==0:
            return None
        self.selected = [selected.pop()]
        return self.selected

    def selected(self):
        return self.selected
    ###################################################################################################################
