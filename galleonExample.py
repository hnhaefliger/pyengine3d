#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Complex model example: Galleon"""

from graphics.engine import read_data_file, Engine3D

vertices = read_data_file('coords/GalleonV.txt', 'V', scale=1/150)
polygons = read_data_file('coords/GalleonP.txt', 'P')
test = Engine3D(vertices, polygons, distance=100, title='Galleon')

def animation():
    test.clear()
    test.rotate('y', 0.1)
    test.render()
    test.screen.after(1, animation)

if __name__ == '__main__':
    animation()
    test.screen.window.mainloop()
