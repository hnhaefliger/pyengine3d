#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Animated pyramid example"""

from graphics.engine import Engine3D

vertices = [[0,0,0],[0,-1,0],[-1,1,-1],[-1,1,1],[1,1,1],[1,1,-1]]
polygons = [[2,3,4,5],[1,2,3],[1,3,4],[1,4,5],[1,2,5]]
test = Engine3D(vertices, polygons, title='Cube')

def animation():
    test.clear()
    test.free_rotate(.75, 0, 1) # angle in degree, axe defined by 2 vertices
    test.render()
    test.screen.after(10, animation)

if __name__ == '__main__':
    animation()
    test.screen.window.mainloop()
