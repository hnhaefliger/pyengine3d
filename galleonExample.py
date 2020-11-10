### Galleon ###

import graphics.engine

points = []
triangles = []

with open('coords/GalleonV.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        coords = line[:-2].split(' ')
        points.append([float(coords[0])/150, float(coords[1])/150, float(coords[2])/150])
    f.close()

with open('coords/GalleonT.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        coords = line[:-2].split(' ')
        newCoords = []
        for coord in coords[1:4]:
            newCoords.append(int(coord))
        triangles.append(newCoords)
    f.close()

test = graphics.engine.Engine3D(points, triangles, distance=100, title='Galleon')

def animation():
    test.clear()
    test.rotate('y', 0.1)
    test.render()
    test.screen.after(1, animation)

animation()
test.screen.window.mainloop()

################
