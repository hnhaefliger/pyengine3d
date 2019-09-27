### Galleon ###

import graphics

points = []
triangles = []

with open('coords/GalleonV.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        coords = line[:-2].split(' ')
        points.append((float(coords[0])/150, float(coords[1])/150, float(coords[2])/150))
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

test = graphics.Engine3D(points, triangles, distance=100)

def animation():
    test.clear()
    test.rotateY(0.0005)
    test.render('gray')
    test.window.after(25, animation)

animation()

################
