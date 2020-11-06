
def read_file(name, divider=1):
    points = []
    triangles = []
    vertex_file = "coords/" + name + 'V.txt'
    with open(vertex_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            coords = line[:-2].split(' ')
            points.append([float(coords[0])/divider, float(coords[1])/divider, float(coords[2])/divider])
        f.close()
        print('number of points : ', len(points))

    triangle_file = "coords/" + name + 'T.txt'
    with open(triangle_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            coords = line[:-2].split(' ')
            newCoords = []
            for coord in coords[1:4]:
                newCoords.append(int(coord))
            triangles.append(newCoords)
        f.close()
        print('Number of triangles : ', len(triangles))
        return points, triangles