#!/usr/bin/python3
# -*- coding: utf-8 -*-
### Cube ###

import graphics.engine

points = [[-1,-1,-1],[-1,-1,1],[-1,1,1],[-1,1,-1],[1,-1,-1],[1,-1,1],[1,1,1],[1,1,-1]]
triangles = [[0,1,3],[1,2,3],[1,2,6],[1,5,6],[0,1,4],[1,4,5],[4,5,6],[4,7,6],[0,3,4],[3,4,7],[2,3,6],[3,6,7]]
test = graphics.engine.Engine3D(points, triangles, title='Cube')

def animation():
    test.clear()
    test.rotate('y', 1)
    test.rotate('x', 1)
    test.render()
    test.screen.after(100, animation)

animation()
test.screen.window.mainloop()

############
