# PyEngine3D

Example of a simple landscape         |  Example of a mountain landscape
:-------------------------:|:-------------------------:
![](images/landscape1.png?raw=true)  |  ![](images/landscape2.png?raw=true )

The code here is explained in my medium.com post <https://medium.com/quick-code/3d-graphics-using-the-python-standard-library-99914447760c>

---

PyEngine3D is a simple module using only the python standard library to display and interact with 3D designs.

---

The main module can be found in the "graphics" directory, the other files are demos of different features.

---

The first step is to create an Engine object which requires a set of points and a set of triangles linking them together.

```Python
test = Engine3D([[1, 1, 1], [0, 0, 0], [2, 2, 2]], [[0, 1, 2]]) # this will create a single triangle between these points
test = Engine3D([[1, 1, 1], [0, 0, 0], [2, 2, 2]], [[0, 1, 2, "green"]]) # you can also change the color of the triangle (the default is green)
```

From your code, you can modify the display using the writePoints, writeTriangles, rotate, clear and render methods.

```Python
test.writePoints([[3, 3, 3], [0, 0, 0], [2, 2, 2]]) # change the points
test.writeTriangles([[2, 1, 0, "blue"]]) # the order of the points does not matter
test.rotate("y", 45) # rotate the object 45 degrees around the y axis
test.clear() # clear the display
test.render() # update the image
```

You can also use the following keys to interact with the display.

1. Left mouse button + Drag -> Rotate the view
2. Up arrow -> Zoom in
3. Down arrow -> Zoom out
4. w, a, s, d -> Move the view up, left, down or right

The module now also allows you to move points on the model (this is still a work in progress)

1. Select a point using the right mouse button (holding)
2. Select an axis to move along by pressing x, y or z
3. Use the right and left arrow keys to move along the axis

---

If you would like to help me improve this project, you can contact me at code@henryhaefliger.com
