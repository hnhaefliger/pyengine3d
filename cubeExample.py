### Cube ###

import graphics

points = [(-1,-1,-1),(-1,-1,1),(-1,1,1),(-1,1,-1),(1,-1,-1),(1,-1,1),(1,1,1),(1,1,-1)]
triangles = [(0,1,2),(0,2,3), (2,3,7),(2,7,6), (1,2,5),(2,5,6), (0,1,4),(1,4,5), (4,5,6),(4,6,7), (3,7,4),(4,3,0)]

test = graphics.Engine3D(points, triangles)

def animation():
    test.clear()
    test.rotateX(0.0005)
    test.rotateY(0.0005)
    test.rotateZ(0.0005)
    test.render()
    test.window.after(25, animation)

animation()

############
