#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Folding management example.


Origami pattern
---------------

Here we got an example of how graphical engine can use rotation around free
axis.  We use those rotations on a rectangular paper sheet and fold it into
origami card box.

The origami pattern is flat modelised with final card box dimensions, so
vertices coordinates are calculated accordly to few parameters.

Folds are a bit complexe to describe:
- Parameter is a list of step-folds;
- Each step-fold is itself a list of line-folds moving together during the
  folding step;
- Each line-fold is a 4 tuple composed by:
  - The angle value in degrees;
  - 2 vertices indexes that defines the rotation axe (oriented);
  - A list of vertices indexes that rotates around this .


Commands
--------

A set of two new commmands are added to the keyboard binding:
-<key N>: forward animation of the next fold
-<key P>: backward animation of the previous fold


Technical remarks
-----------------

- The current drawing engine uses a fast but simple ordering of faces on their
z-middle-coordinate. Then faces are drawn from far to close, and close faces
covers far ones. This way of rendering is quite good enougth to draw volumic
models with single grid faces, but is doesn't render perfect for faces that are
close and almost parallels like folded sheets of paper.  So, until the render
engine is changed for a more complex and strict one, folded models may need to
be turn around to be correctly drawn and understood.

- Some patterns contains faces that are not triangles, but the current engine
only manages triangles. Until other polygones ares managed by main engine,
patterns would use a uniq color to show each rigid polygon (So 2 consecutive
same color triangles do not fold in beetween in the final model - but they can
fold a bit during folding for gaining light paper twist).

- There is no management for polygons intersections during fold visualisation so
there might be vertices that moves a little through faces. During real paper
folding, paper polygons are flexibles so there is no problem.

"""

import graphics.engine

# Flat pattern that folds into a parametric box.
W = 1.3 # box width
T = .5 # box thickness
S = .01 # paper thickness causing a little shift on some faces (pre calculated in flat pattern).

points = [
          [-2.5*W-2*T+S, -.5*W, .5*T], [-1.5*W-2*T+S, -.5*W, .5*T], [-1.5*W-T, -.5*W, .5*T], # 0 1 2
          [-.5*W-T, -.5*W, .5*T], [-.5*W, -.5*W, .5*T], [.5*W, -.5*W, .5*T+S/2], # 3 4 5
          [.5*W+T-S, -.5*W, .5*T+S/2], [1.5*W+T-S, -.5*W, .5*T+S/2], [1.5*W+2*T-3*S, -.5*W, .5*T+S/2], # 6 7 8
          [-2.5*W-2*T+S, .5*W, .5*T], [-1.5*W-2*T+S, .5*W, .5*T], [-1.5*W-T, .5*W, .5*T], # 9 10 11
          [-.5*W-T, .5*W, .5*T], [-.5*W, .5*W, .5*T], [.5*W, .5*W, .5*T-S/2], # 12 13 14
          [.5*W+T-S, .5*W, .5*T-S/2], [1.5*W+T-S, .5*W, .5*T-S/2], [1.5*W+2*T-3*S, .5*W, .5*T-S/2], # 15 16 17
          [-2*W-2*T+S, 0, .5*T], [-1.5*W-1.5*T+S, 0, .5*T], [-1*W-T, 0, .5*T], # 18 19 20
          [-.5*W-.5*T, 0, .5*T], [0, 0, .5*T], [.5*W+.5*T, 0, .5*T], # 21 22 23
          [W+T-S, 0, .5*T], [1.5*W+1.5*T-S, 0, .5*T], # 24 25
         ]

quads = [
         [0, 1, 18, 'pink'], [0, 9, 18, 'pink'], [1, 10, 18, 'pink'], [9, 10, 18, 'pink'],
         [1, 2, 19, 'red'], [1, 10, 19, 'red'], [2, 11, 19, 'red'], [10, 11, 19, 'red'],
         [2, 3, 20, 'orange'], [2, 11, 20, 'orange'],
         [3, 12, 20, 'gold'], [11, 12, 20, 'gold'],
         [3, 4, 21, 'lime'], [3, 12, 21, 'lime'], [4, 13, 21, 'lime'], [12, 13, 21, 'lime'],
         [4, 5, 22, 'green'], [4, 13, 22, 'green'], [5, 14, 22, 'green'], [13, 14, 22, 'green'],
         [5, 6, 23, 'cyan'], [5, 14, 23, 'cyan'], [6, 15, 23, 'cyan'], [14, 15, 23, 'cyan'],
         [6, 15, 24, 'royal blue'], [15, 16, 24, 'royal blue'],
         [6, 7, 24, 'blue'], [7, 16, 24, 'blue'],
         [7, 8, 25, 'purple'], [7, 16, 25, 'purple'], [8, 17, 25, 'purple'], [16, 17, 25, 'purple'],
        ]

PA = 15 # small angle to visualise paper marks in pre-fold
folds = [
         [ # pre mark for any final fold
          (PA,  1, 10, [0, 9, 18]), # pink/red
          (PA,  2, 11, [0, 1, 9, 10, 18, 19]), # red/orange
          (PA, 11,  3, [0, 1, 2, 9, 10, 18, 19]), # orange/yellow
          (PA, 12,  3, [0, 1, 2, 9, 10, 11, 18, 19, 20]), # yellow/lime
          (PA, 13,  4, [0, 1, 2, 3, 9, 10, 11, 12, 18, 19, 20, 21]), # lime/green
          (PA,  5, 14, [6, 7, 8, 15, 16, 17, 23, 24, 25]), # green/cyan
          (PA,  6, 15, [7, 8, 16, 17, 24, 25]), # cyan/lightblue
          (PA,  6, 16, [7, 8, 17, 25]), # lightblue/blue
          (PA, 16,  7, [8, 17, 25]), # blue/purple
         ], [ # first step-fold: outside pre 90° folds for bottom
          (90-PA,  1, 10, [0, 9, 18]), # pink/red
          (90-PA,  2, 11, [0, 1, 9, 10, 18, 19]), # red/orange
          (90-PA, 16,  7, [8, 17, 25]), # blue/purple
         ], [ # second step-fold: diagonals for triangle crossing in front part
              # (not 180° to avoid face identity when draw)
          (179-PA, 11,  3, [0, 1, 2, 9, 10, 18, 19]), # orange/yellow
          (179-PA,  6, 16, [7, 8, 17, 25]), # lightblue/blue
         ], [ # third step-fold: face bottom parts, left "outside" side
          (30,  1,  9, [0]), # pink/pink
          (10,  1, 10, [0, 9,  18]), # pink/red
          (30, 11,  2, [0, 1, 9, 10, 18, 19]), # red/orange
          (90-PA, 12,  3, [0, 1, 2, 9, 10, 11, 18, 19, 20]), # yellow/lime
          (60-PA, 13,  4, [0, 1, 2, 3, 9, 10, 11, 12, 18, 19, 20, 21]), # lime/green
         ], [ # fourth step-fold: face bottom parts, right "inside" side
          (35,  5, 13, [6, 7, 8, 14, 15, 16, 17, 23, 24, 25]), # green/green
          (45-PA,  5, 14, [6, 7, 8, 15, 16, 17, 23, 24, 25]), # green/cyan
          (20,  6, 14, [7, 8, 15, 16, 17, 24, 25]), # cyan/cyan
          (75-PA,  6, 15, [7, 8, 16, 17, 24, 25]), # cyan/lightblue
          (60, 24,  7, [8, 16, 17, 25]), # blue/blue
          (45, 16,  7, [8, 17, 25]), # blue/purple
         ], [ # fifth step-fold: slide into bottom and complete box
          (30,  9,  1, [0]), # pink/pink
          (10, 10,  1, [0, 9, 18]), # pink/red
          (30,  2, 11, [0, 1, 9, 10, 18, 19]), # red/orange
          (30, 13,  4, [0, 1, 2, 3, 9, 10, 11, 12, 18, 19, 20, 21]), # lime/green
          (35, 13,  5, [6, 7, 8, 14, 15, 16, 17, 23, 24, 25]), # green/green
          (45,  5, 14, [6, 7, 8, 15, 16, 17, 23, 24, 25]), # green/cyan
          (20, 14,  6, [7, 8, 15, 16, 17, 24, 25]), # cyan/cyan
          (15,  6, 15, [7, 8, 16, 17, 24, 25]), # cyan/lightblue
          (60,  7, 24, [8, 16, 17, 25]), # blue/blue
          (45,  7, 16, [8, 17, 25]), # blue/purple
         ]
        ]

test = graphics.engine.Engine3D(points, quads, folds, title='Fold')
test.render()
test.screen.window.mainloop()
