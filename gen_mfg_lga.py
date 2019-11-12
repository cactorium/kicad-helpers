#!/usr/bin/env python3

# QFN/QFP-style packages with ground plane
# version 0.0.7

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
# - add support for rotation
# - separate out ground pad rounding parameter 
#     from normal pad rounding parameter

PARTNAME = "ST-LGA14-L"

total_pins = 14
num_per_edge = total_pins // 4

num_topbottom = 3
num_leftright = 4

M1 = 0.2 # silkscreen margin
M2 = 0.05 # fab outline margin
M3 = 0.3 # courtyard margin

Z = 2.50 - 2*0.1 + 2*0.05 # distance across outer edges of top and bottom pads
G = 2.50 - 2*0.1 - 2*0.475 - 2*0.05  # distance across inner edges of tb pads
Z2 = 3.00 - 2*0.1 + 2*0.05 # distance across outer edges of lr pads
G2 = 2.50 - 2*0.1 - 2*0.475 - 2*0.05  # distance across inner edges of lr pads

Y = (Z+G)/2. # distance between pad centers vertically
X = (Z2+G2)/2. # distance between pad centers horizontally
C = 0.5 # footprint pad spacing
w = 0.25 + 0.05 # footprint pad width
h = (Z-G)/2. # footprint pad length
h2 = (Z2-G2)/2. # footprint pad length

show_fab_pads = False
H1 = 2.50 # distance from physical pad end to opposite pad end vertically
H2 = 3.00 # distance from physical pad end to opposite pad end horizontally
e = C    # physical pad spacing, same as above
b = 0.25 # physical pad width
L1 = -0.475 # physical pad length

D1 = 3.0 # package width
E1 = 2.5 # package height

has_ground_pad = False
G1 = 1.65 # ground pad width
H1 = 1.65 # ground pad height
ground_pad_num = 0

# NOTE: need to test with SMD footprints
# need to make sure pad size adjustment works
# nsmd = positive
solder_mask_margin = 0.10
indicator_circle_dia = 0.3

pad_radius = None
ground_pad_radius = None

rotation = 90

if solder_mask_margin < 0.0:
  w -= 2.0*solder_mask_margin
  h -= 2.0*solder_mask_margin
  G1 -= 2.0*solder_mask_margin
  H1 -= 2.0*solder_mask_margin

import math

def _x(x, y):
  return x*math.cos(rotation*math.pi/180.) - y*math.sin(rotation*math.pi/180.)
def _y(x, y):
  return x*math.sin(rotation*math.pi/180.) + y*math.cos(rotation*math.pi/180.)
def xy(x, y):
  return (_x(x, y), _y(x, y))
def xyxy(x1, y1, x2, y2):
  return (_x(x1, y1), _y(x1, y1), _x(x2, y2), _y(x2, y2))


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
inner_edge = C*(num_per_edge/2 - 0.5) + w/2 + M1
x = D1/2 + M1
y = E1/2 + M1
for x, y, nx, ny in [
    (-x, -inner_edge, -inner_edge, -y),

    (-x, y, -x, inner_edge), (-inner_edge, y, -x, y), 
    (inner_edge, y, x, y), (x, y, x, inner_edge),
    (x, -inner_edge, x, -y), (x, -y, inner_edge, -y)]:
  print("""  (fp_line (start {} {}) (end {} {}) (layer F.SilkS) (width 0.15))""".
      format(*xyxy(x, y, nx, ny)))

if indicator_circle_dia is not None:
  x = D1/2 + M1 #+ 0.5*indicator_circle_dia
  y = E1/2 + M1 #+ 0.5*indicator_circle_dia
  # add indicator circle
  print("""  (fp_circle (center {} {}) (end {} {}) (layer F.SilkS) (width 0.15))""".
      format(*xyxy(-x, -y, -x, -y - indicator_circle_dia/2.0)))


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

if show_fab_pads:
  for i in range(num_leftright):
    x_pos = -D1/2 - M2
    y_pos = C*(i-(num_leftright/2.-0.5))
    print("""  (fp_line (start {} {}) (end {} {}) (layer F.Fab) (width 0.15))""".
        format(*xyxy(x_pos, y_pos - b/2 - M2, x_pos - L1, y_pos - b/2 - M2)))
    print("""  (fp_line (start {} {}) (end {} {}) (layer F.Fab) (width 0.15))""".
        format(*xyxy(x_pos - L1, y_pos - b/2 - M2, x_pos - L1, y_pos + b/2 + M2)))
    print("""  (fp_line (start {} {}) (end {} {}) (layer F.Fab) (width 0.15))""".
        format(*xyxy(x_pos - L1, y_pos + b/2 + M2, x_pos, y_pos + b/2 + M2)))

  for i in range(num_topbottom):
    x_pos = C*(i-(num_topbottom/2.-0.5))
    y_pos = E1/2 + M2
    print("""  (fp_line (start {} {}) (end {} {}) (layer F.Fab) (width 0.15))""".
        format(*xyxy(x_pos - b/2 - M2, y_pos, x_pos - b/2 - M2, y_pos + L1)))
    print("""  (fp_line (start {} {}) (end {} {}) (layer F.Fab) (width 0.15))""".
        format(*xyxy(x_pos - b/2 - M2, y_pos + L1, x_pos + b/2 + M2, y_pos + L1)))
    print("""  (fp_line (start {} {}) (end {} {}) (layer F.Fab) (width 0.15))""".
        format(*xyxy(x_pos + b/2 + M2, y_pos + L1, x_pos + b/2 + M2, y_pos)))

  for i in range(num_leftright):
    x_pos = D1/2 + M2
    y_pos = -C*(i-(num_leftright/2.-0.5))
    print("""  (fp_line (start {} {}) (end {} {}) (layer F.Fab) (width 0.15))""".
        format(*xyxy(x_pos, y_pos + b/2 + M2, x_pos + L1, y_pos + b/2 + M2)))
    print("""  (fp_line (start {} {}) (end {} {}) (layer F.Fab) (width 0.15))""".
        format(*xyxy(x_pos + L1, y_pos + b/2 + M2, x_pos + L1, y_pos - b/2 - M2)))
    print("""  (fp_line (start {} {}) (end {} {}) (layer F.Fab) (width 0.15))""".
        format(*xyxy(x_pos + L1, y_pos - b/2 - M2, x_pos, y_pos - b/2 - M2)))

  for i in range(num_topbottom):
    x_pos = -C*(i-(num_top_bottom/2-0.5))
    y_pos = -E1/2 - M2
    print("""  (fp_line (start {} {}) (end {} {}) (layer F.Fab) (width 0.15))""".
        format(*xyxy(x_pos + b/2 + M2, y_pos, x_pos + b/2 + M2, y_pos - L1)))
    print("""  (fp_line (start {} {}) (end {} {}) (layer F.Fab) (width 0.15))""".
        format(*xyxy(x_pos + b/2 + M2, y_pos - L1, x_pos - b/2 - M2, y_pos - L1)))
    print("""  (fp_line (start {} {}) (end {} {}) (layer F.Fab) (width 0.15))""".
        format(*xyxy(x_pos - b/2 - M2, y_pos - L1, x_pos - b/2 - M2, y_pos)))


# print courtyard outline
inner_x = D1/2. + M3
outer_x = max(X/2. + h/2. + M3/2., inner_x)
#inner_y = C*(num_per_edge/2-0.5) + b/2 + M3/2
inner_y = E1/2. + M3
outer_y = max(Y/2. + h/2. + M3/2., inner_y)
pts = [
    (-inner_x, -outer_y),
    (inner_x, -outer_y),
    (inner_x, -inner_y),
    (outer_x, -inner_y),
    (outer_x, inner_y),
    (inner_x, inner_y),
    (inner_x, outer_y),
    (-inner_x, outer_y),
    (-inner_x, inner_y),
    (-outer_x, inner_y),
    (-outer_x, -inner_y),
    (-inner_x, -inner_y)
    ]
nx, ny = pts[-1]
for px, py in pts:
  x, y, nx, ny = nx, ny, px, py
  print("""  (fp_line (start {} {}) (end {} {}) (layer F.CrtYd) (width 0.15))""".
      format(*xyxy(x, y, nx, ny)))

if rotation == 90 or rotation == 270:
  h, w = w, h
  G1, H1 = H1, G1

padtype = "rect"
padext = ""
if pad_radius is not None:
  padtype = "roundrect"
  padext = "(roundrect_rratio {})".format(pad_radius/min(h, w))

for i in range(0, num_leftright):
  tx, ty = xy(-X/2., C*(i-(num_leftright/2.-0.5)))
  print("""  (pad {} smd {} (at {} {}) (size {} {}) (layers F.Cu F.Paste F.Mask)
    {} (solder_mask_margin {}))""".
        format(
            i+1,
            padtype,
            tx,
            ty,
            h,
            w,
            padext,
            solder_mask_margin))

for i in range(0, num_topbottom):
  tx, ty = xy(C*(i-(num_topbottom/2.-0.5)), Y/2.)
  print("""  (pad {} smd {} (at {} {}) (size {} {}) (layers F.Cu F.Paste F.Mask)
    {} (solder_mask_margin {}))""".
        format(
          i+1+num_leftright,
          padtype,
          tx,
          ty,
          w,
          h,
          padext,
          solder_mask_margin))

for i in range(0, num_leftright):
  tx, ty = xy(X/2., -C*(i-(num_leftright/2.-0.5)))
  print("""  (pad {} smd {} (at {} {}) (size {} {}) (layers F.Cu F.Paste F.Mask)
    {} (solder_mask_margin {}))""".
        format(
          i+1+num_leftright+num_topbottom,
          padtype,
          tx,
          ty,
          h,
          w,
          padext,
          solder_mask_margin))

for i in range(0, num_topbottom):
  tx, ty = xy(-C*(i-(num_topbottom/2.-0.5)), -Y/2.)
  print("""  (pad {} smd {} (at {} {}) (size {} {}) (layers F.Cu F.Paste F.Mask)
    {} (solder_mask_margin {}))""".
        format(
          i+1+2*num_leftright+num_topbottom,
          padtype,
          tx,
          ty,
          w,
          h,
          padext,
          solder_mask_margin))


if has_ground_pad: 
  if ground_pad_radius is None:
    # add ground pad
    print("""  (pad {} smd {} (at {} {}) (size {} {}) (layers F.Cu F.Paste F.Mask)
      (solder_mask_margin {}))""".
          format(
              ground_pad_num,
              "rect",
              0,
              0,
              G1,
              H1,
              solder_mask_margin))
  else:
    print("""  (pad {} smd {} (at {} {}) (size {} {}) (layers F.Cu F.Paste F.Mask)
      (roundrect_rratio {}) (solder_mask_margin {}))""".
          format(
              ground_pad_num,
              "roundrect",
              0,
              0,
              G1,
              H1,
              ground_pad_radius/min(G1, H1),
              solder_mask_margin))

print(epilogue)
