########################################################################################################################
import sys
from PySide2 import QtCore, QtWidgets
from PySide2.QtWidgets import QWidget
from PySide2.QtCore import QPoint
from PySide2.QtGui import QPolygon, QColor, QBrush, QPen, QPainter
from graphics.engine3d import Engine3D
########################################################################################################################

class SideEngine3D(QWidget, Engine3D):
    start_pan: bool
    start_drag: bool

    def __init__(self, points, triangles, width=1000, height=700, distance=6, scale=100, title='3D',
                 background='black'):
        super(SideEngine3D)
        Engine3D.__init__(self, points, triangles, width, height, distance, scale, title, background)
        QWidget.__init__(self)

        self.setWindowTitle(title)
        self.setGeometry(300, 300, width, height)
        self.show()

    #################

    # QWidget events

    def resizeEvent(self, event):
        pass

    def mousePressEvent(self, ev):
        if ev.button() == QtCore.Qt.LeftButton:
            if ev.modifiers() & QtCore.Qt.ShiftModifier:
                self.start_drag = True
            else:
                self.select([ev.x(), ev.y()])
                self.update()
        elif ev.button() == QtCore.Qt.RightButton:
            self.start_pan = True
            Engine3D.reset_pan(self, ev.x(), ev.y())

    def mouseReleaseEvent(self, ev):
        if ev.button() == QtCore.Qt.LeftButton:
            self.start_drag = False
            Engine3D.reset_drag(self)
        elif ev.button() == QtCore.Qt.RightButton:
            self.start_pan = False

    def mouseMoveEvent(self, ev):
        if self.start_drag:
            Engine3D.drag(self, ev.x(), ev.y())
            self.update()
        elif self.start_pan:
            Engine3D.pan(self, ev.x(), ev.y())
            self.update()

    def wheelEvent(self, ev):
        if ev.delta() > 0:
            Engine3D.zoom_in(self)
        else:
            Engine3D.zoom_out(self)
        self.update()

    def keyPressEvent(self, ev):
        if ev.key() == QtCore.Qt.Key_Plus:
            Engine3D.zoom_in(self)
        elif ev.key() == QtCore.Qt.Key_Minus:
            Engine3D.zoom_out(self)
        elif ev.key() == QtCore.Qt.Key_Left:
            Engine3D.camera_left(self)
        elif ev.key() == QtCore.Qt.Key_Right:
            Engine3D.camera_right(self)
        elif ev.key() == QtCore.Qt.Key_L:
            self.light_toggle()
        self.update()

    ##this break encapsulation because engine need QPoint
    def draw_triangles(self, qp, tri):
        list(map(lambda t: (qp.setBrush(QBrush(QColor(t.color, t.color, t.color))),
                            qp.drawPolygon(QPolygon(t.get_pts(self.pan)))), tri))

    def paintEvent(self, event):
        if Engine3D.must_recompute(self):
            Engine3D.render(self)
        qp = QPainter()
        qp.setRenderHint(QPainter.Antialiasing)
        qp.begin(self)
        qp.setPen(QPen(QColor(60, 60, 60, 0)))
        self.draw_triangles(qp, Engine3D.get_flat_triangles(self))
        p = QPen(QColor(255, 0, 0))
        p.setWidth(3)
        qp.setPen(p)
        self.draw_triangles(qp, Engine3D.selected(self))
        qp.end()


########################################################################################################################
def app():
    return QtWidgets.QApplication(sys.argv)


def run(app):
    sys.exit(app.exec_())
########################################################################################################################
