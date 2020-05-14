# PyEngine3D

PyEngine3D is a simple module using only the python standard library to display and interact with 3D designs.

---

The main module can be found in the "graphics" directory, the other files are demos of different features.

---

The first step is to create an Engine object which requires a set of points and a set of triangles linking them together.

From your code, you can modify the display using the writePoints, writeTriangles, rotate, clear and render methods.

You can also use the following keys to interact with the display.

Left mouse button + Drag -> Rotate the view
Up arrow -> Zoom in
Down arrow -> Zoom out
w, a, s, d -> Move the view up, left, down or right

The module now also allows you to move points on the model (this is still a work in progress)

1. Select a point using the right mouse button (holding)
2. Select an axis to move along by pressing x, y or z
3. Use the right and left arrow keys to move along the axis

---

If you would like to help me improve this project
