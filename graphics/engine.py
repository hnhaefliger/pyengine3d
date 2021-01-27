import graphics.screen
import graphics.structures
import copy


def read_data_file(filename, data_type, scale=1):
    """Open a data file and creates a list of corresponding datas.

    Data_type can be either 'V' for vertices coordinates (a line = 3 ints)
    either 'P' for polygons (a line = an int for polygon size, n indexes of
    vertices and an optional color name).

    Scale is an optional zoom factor for vertices coordinates.
    """
    with open(filename, 'r') as f:
        if data_type == 'V':
            return [list(map(lambda c:float(c)*scale, l[:-1].strip().split())) for l in f.readlines()]
        else: # data_type == 'P'
            formated_lines = [l[:-1].strip().split() for l in f.readlines()]
            return [list(map(int, fl[1:int(fl[0])+1])) + fl[int(fl[0])+1:] for fl in formated_lines]


class Engine3D:
    # number of pictures in fold animations
    anim_steps = 20
    # colors for show vectors in grabbing
    axis_colors = ['red', 'green', 'blue']

    def __init__(self, vertices, polygons, folds=[], width=1000, height=700, distance=6, scale=100, title='3D', background='white'):
        # vertices
        self.vertices = [graphics.structures.Vertex(v) for v in vertices]
        # faces
        self.polygons = [graphics.structures.Polygon(*p) for p in polygons]
        # folds
        self.folds = folds

        # initialize display
        self.screen = graphics.screen.Screen(width, height, title, background)

        # viewing
        self.distance = distance
        self.scale = scale
        self.screen.window.bind('<ButtonRelease-4>', self.__zoom_in)
        self.screen.window.bind('<ButtonRelease-5>', self.__zoom_out)
        self.screen.window.bind('<Up>', self.__camera_up)
        self.screen.window.bind('<Down>', self.__camera_down)
        self.screen.window.bind('<Left>', self.__camera_left)
        self.screen.window.bind('<Right>', self.__camera_right)

        # folding animation
        self.fold_index = 0
        self.screen.window.bind('n', self.__next_fold)
        self.screen.window.bind('p', self.__prev_fold)

        # grabbing
        self.__reset_drag()
        self.screen.window.bind('<B1-Motion>', self.__drag)
        self.screen.window.bind('<ButtonRelease-1>', self.__reset_drag)

        # model edition
        self.__selected = None
        self.screen.window.bind('<ButtonPress-3>', self.__select)
        self.screen.window.bind('<ButtonRelease-3>', self.__deselect)
        self.screen.window.bind('x', self.__select_x)
        self.screen.window.bind('y', self.__select_y)
        self.screen.window.bind('z', self.__select_z)
        self.screen.window.bind('+', self.__move_down)
        self.screen.window.bind('-', self.__move_up)

    def __reset_drag(self, event=None):
        self.__prev = []

    def __drag(self, event):
        if self.__prev:
            self.rotate('y', (event.x - self.__prev[0]) / 20)
            self.rotate('x', (event.y - self.__prev[1]) / 20)
            self.clear()
            self.render()
        self.__prev = [event.x, event.y]

    def __build_axis(self, selection, direction, orientation):
        res = copy.deepcopy(selection)
        setattr(res, direction, getattr(res, direction) + 40 * orientation / self.scale)
        res.flatten(self.scale, self.distance)
        return (res.get_flat()[0] + self.screen.zeros[0], res.get_flat()[1] + self.screen.zeros[1])

    def __select(self, event):
        zeros = self.screen.zeros
        ex, ey = event.x - zeros[0], event.y - zeros[1]
        exm, exp, eym, eyp = ex - 6, ex + 5, ey - 6, ey + 5
        possible_vertices = [i for i,v in enumerate(self.vertices)
                               if exm < v.flat_x < exp and eym < v.flat_y < eyp]
        if possible_vertices != []:
            self.__moveaxis = None
            self.__selected = self.vertices[possible_vertices[0]]
            axis = [[self.__build_axis(self.__selected, d, o) for o in [-1,1]] for d in 'xyz']
            self.__axis = [self.screen.create_arrow(a, self.axis_colors[i]) for i,a in enumerate(axis)]

    def __select_x(self, event):
        self.__moveaxis = 'x'

    def __select_y(self, event):
        self.__moveaxis = 'y'

    def __select_z(self, event):
        self.__moveaxis = 'z'

    def __move_up(self, event):
        if self.__selected != None and self.__moveaxis != None:
            self.__selected.move(self.__moveaxis, 0.1)
            self.clear()
            self.render()

    def __move_down(self, event):
        if self.__selected != None and self.__moveaxis != None:
            self.__selected.move(self.__moveaxis, -0.1)
            self.clear()
            self.render()

    def __deselect(self, event):
        if self.__selected != None:
            self.__selected = None
            for line in self.__axis:
                self.screen.delete(line)
            self.__axis = []

    def __zoom_in(self, event):
        self.scale += 2.5
        self.clear()
        self.render()

    def __zoom_out(self, event):
        self.scale -= 2.5
        self.clear()
        self.render()

    def __camera_left(self, event):
        self.screen.zeros[0] -= 5
        self.clear()
        self.render()

    def __camera_right(self, event):
        self.screen.zeros[0] += 5
        self.clear()
        self.render()

    def __camera_up(self, event):
        self.screen.zeros[1] -= 5
        self.clear()
        self.render()

    def __camera_down(self, event):
        self.screen.zeros[1] += 5
        self.clear()
        self.render()

    def __next_fold(self, event):
        if self.fold_index < len(self.folds):
            for i in range(self.anim_steps):
                self.screen.after(int(1000/self.anim_steps), self.__fold_animate(self.folds[self.fold_index]))
            self.fold_index += 1

    def __prev_fold(self, event):
        if self.fold_index > 0:
            for i in range(self.anim_steps):
                self.screen.after(int(1000/self.anim_steps), self.__fold_animate(self.folds[self.fold_index-1],False))
            self.fold_index -= 1

    def __fold_animate(self, folds, do=True):
        for subfolds in folds:
            angle, axe1, axe2, vertices = subfolds
            if do == True:
                angle = angle / self.anim_steps
            else:
                angle = -angle / self.anim_steps
            self.part_free_rotate(angle, axe1, axe2, vertices)
        self.clear()
        self.render()
        self.screen.window.update_idletasks()

    def rotate(self, axis, angle):
        # rotate model around axis
        for point in self.vertices:
            point.rotate(axis, angle)

    def part_free_rotate(self, angle, A, B, vertices):
        # rotate part of model around free vector (from self.vertices[A] to self.vertices[B])
        for point in [self.vertices[index] for index in vertices]:
            point.free_rotate(angle, self.vertices[A], self.vertices[B])

    def free_rotate(self, angle, A, B):
        # rotate model around free vector (from self.vertices[A] to self.vertices[B])
        for point in self.vertices:
            point.free_rotate(angle, self.vertices[A], self.vertices[B])

    def clear(self):
        # clear display
        self.screen.clear()

    def render(self):
        # flatten vertices into screen positions
        for vert in self.vertices:
            vert.flatten(self.scale, self.distance)

        # calculate polygons average depth (z)
        for poly in self.polygons:
            poly.depth = sum([self.vertices[v_i].z for v_i in poly.vertices])

        # draw flattent polygons from furthest to closest
        for poly in reversed(sorted(self.polygons, key=lambda x: x.depth)):
            self.screen.create_polygon([self.vertices[v].get_flat() for v in poly.vertices], poly.color)

