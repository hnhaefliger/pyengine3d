### Shark ###

import graphics

points = []
triangles = []

with open('SharkV.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        coords = line[:-2].split(' ')
        points.append((float(coords[0]), float(coords[1]), float(coords[2])))
    f.close()

with open('SharkT.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        coords = line[:-2].split(' ')
        newCoords = []
        for coord in coords[1:4]:
            newCoords.append(int(coord))
        triangles.append(newCoords)
    f.close()

test = graphics.Engine3D(points, triangles, scale=100)

def animation():
    test.clear()
    test.rotateY(0.0005)
    test.render()
    test.window.after(25, animation)

animation()

##############
