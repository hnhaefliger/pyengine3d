import tkinter

class Screen:
    def __init__(self, width, height):
        self.__root = tkinter.Tk()
        self.__root.title('3D Graphics')

        self.__screen = tkinter.Canvas(self.__root, width=width, height=height)
        self.__screen.pack()

        self.__height = height
        self.__width = width
        self.__shapes = []

    def drawTriangle(self, coords, color="white", outline="black"):
        a, b, c = coords[0], coords[1], coords[2]
        coords = [a[0], a[1], b[0], b[1], c[0], c[1]]
        self.__shapes.append(self.__screen.create_polygon(coords, color=color, outline=outline))

    @property
    def heigth(self):
        return self.__height

    @property
    def width(self):
        return self.__width

    @property
    def shapes(self):
        return self.__shapes
