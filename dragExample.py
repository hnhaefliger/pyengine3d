#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""2 coordinates axes rotations with mouse."""

from graphics.engine import read_data_file, Engine3D

vertices = read_data_file('coords/SharkV.txt', 'V')
polygons = read_data_file('coords/SharkP.txt', 'P')
test = Engine3D(vertices, polygons, scale=100, title='Shark')

if __name__ == '__main__':
    test.render()
    test.screen.window.mainloop()
