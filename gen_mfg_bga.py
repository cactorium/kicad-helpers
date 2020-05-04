#!/usr/bin/env python3

# WLCSP/BGA-style packages with ground plane
# version 0.0.8

# added solder mask parameter
# added optional indicator circle
# added ground pad
# made ground pad optional
# fix silkscreen pin 1 marker
# added rounded pads option
# added reference designator to fab layer
# make fab layer pin drawing optional
# added TI's weird ground pad extensions
# v0.0.5
# added indicator marker to fab layer
# v0.0.6
# removed TI extensions
# converted for use in QFN/QFP packages
# - add pads for QFN/QFP
# - add fab pad drawings for QFN/QFP
# - fix silkscreen
# v0.0.7
# - add ground pad offset
# - add rotation
# v0.0.8
# - convert to BGA pad stuff

PARTNAME = "Fairchild_WLCSP-6"

total_pins = 6
num_per_row = 2
num_per_col = total_pins // num_per_row

M1 = 0.2 # silkscreen margin
M2 = 0.05 # fab outline margin
M3 = 0.3 # courtyard margin

C = 0.40 # footprint pad horizontal spacing
D = 0.40 # footprint pad vertical spacing
w = 0.20 # footprint pad diameter

D1 = 0.88 # package width
E1 = 1.23 # package height

# NOTE: need to test with SMD footprints
# need to make sure pad size adjustment works
# nsmd = positive
solder_mask_margin = 0.10
indicator_circle_dia = 0.3

pad_radius = None

rotation = 0

import math
def _x(x, y):
  return x*math.cos(rotation*math.pi/180.) - y*math.sin(rotation*math.pi/180.)
def _y(x, y):
  return x*math.sin(rotation*math.pi/180.) + y*math.cos(rotation*math.pi/180.)
def xy(x, y):
  return (_x(x, y), _y(x, y))
def xyxy(x1, y1, x2, y2):
  return (_x(x1, y1), _y(x1, y1), _x(x2, y2), _y(x2, y2))

if rotation == 90 or rotation == 270:
  C, D = D, C
  D1, E1 = E1, D1

import time
gen_time = hex(int(time.time()))[2:].upper()


prologue = """(module {} (layer F.Cu) (tedit {})
  (fp_text reference REF** (at 0.0 0.0) (layer F.SilkS)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text user %R (at 0.0 0.0) (layer F.Fab)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text value %V (at 0 -0.5) (layer F.Fab) hide
    (effects (font (size 1 1) (thickness 0.15)))
  )
"""

prologue = prologue.format(PARTNAME, gen_time, PARTNAME)
epilogue = """)"""

print(prologue)

# print silkscreen outline
inner_edge_h = C*(num_per_row/2 - 0.5) + w/2 + M1
inner_edge_v = D*(num_per_col/2 - 0.5) + w/2 + M1
x = D1/2 + M1
y = E1/2 + M1
for x, y, nx, ny in [
    (-x, -inner_edge_v, -inner_edge_h, -y),

    (-x, y, -x, inner_edge_v), (-inner_edge_h, y, -x, y), 
    (inner_edge_h, y, x, y), (x, y, x, inner_edge_v),
    (x, -inner_edge_v, x, -y), (x, -y, inner_edge_h, -y)]:
  print("""  (fp_line (start {} {}) (end {} {}) (layer F.SilkS) (width 0.15))""".
      format(*xyxy(x, y, nx, ny)))

if indicator_circle_dia is not None:
  x = D1/2 + M1 #+ 0.5*indicator_circle_dia
  y = E1/2 + M1 #+ 0.5*indicator_circle_dia
  # add indicator circle
  print("""  (fp_circle (center {} {}) (end {} {}) (layer F.SilkS) (width 0.15))""".
      format(*xyxy(-x, -y, -x - indicator_circle_dia/2.0, -y - indicator_circle_dia/2.0)))


# draw package outline in fab layer
FC = 0.3
fab_points = [(-D1/2 - M2 + FC, -E1/2 - M2),
              (D1/2 + M2, -E1/2 - M2),
              (D1/2 + M2, E1/2 + M2),
              (-D1/2 + -M2, E1/2 + M2),
              (-D1/2 + -M2, -E1/2 - M2 + FC)]
 
nx, ny = fab_points[-1]
for x, y in fab_points:
  print("""  (fp_line (start {} {}) (end {} {}) (layer F.Fab) (width 0.15))""".
      format(*xyxy(x, y, nx, ny)))
  nx, ny = x, y

# print courtyard outline
inner_x = D1/2 + M3
inner_y = E1/2 + M3
pts = [
    (-inner_x, -inner_y),
    (inner_x, -inner_y),
    (inner_x, inner_y),
    (-inner_x, inner_y),
    ]
nx, ny = pts[-1]
for px, py in pts:
  x, y, nx, ny = nx, ny, px, py
  print("""  (fp_line (start {} {}) (end {} {}) (layer F.CrtYd) (width 0.15))""".
      format(*xyxy(x, y, nx, ny)))


padtype = "circle"
padext = ""
if pad_radius is not None:
  padtype = "roundrect"
  padext = "(roundrect_rratio {})".format(pad_radius/min(h, w))

alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
for j in range(0, num_per_row):
  for i in range(0, num_per_col):
    tx, ty = xy(D*(j-(num_per_row/2-0.5)), C*(i-(num_per_col/2-0.5)))
    print("""  (pad {} smd {} (at {} {}) (size {} {}) (layers F.Cu F.Paste F.Mask)
      {} (solder_mask_margin {}))""".
          format(
              alpha[i] + str(j + 1),
              padtype,
              tx,
              ty,
              w,
              w,
              padext,
              solder_mask_margin))

print(epilogue)
