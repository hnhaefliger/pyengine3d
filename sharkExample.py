#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Complex model example: Shark"""

from graphics.engine import read_data_file, Engine3D

vertices = read_data_file('coords/SharkV.txt', 'V')
polygons = read_data_file('coords/SharkP.txt', 'P')
test = Engine3D(vertices, polygons, scale=100, title='Shark')

def animation():
    test.clear()
    test.rotate('y', 0.1)
    test.render()
    test.screen.after(1, animation)

if __name__ == '__main__':
    animation()
    test.screen.window.mainloop()
