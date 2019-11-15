import csv

PINOUT_CSV = "./ice40lp1k_pinout.csv"
PACKAGE_NAME = "ICE40LP1K-CB81"
nbanks = 9
pinsperbank = 81 // nbanks
packagename = "CB81"


PROLOGUE = """EESchema-LIBRARY Version 2.3
#encoding utf-8
#
# {}
#
DEF {} U 0 40 Y Y {} L N
F0 "U" 0 0 60 H V C CNN
F1 "{}" 0 150 60 H V C CNN
F2 "" 0 0 60 H I C CNN
F3 "" 0 0 60 H I C CNN
DRAW
S 0 -50 600 -1450 0 1 0 N""".format(PACKAGE_NAME, PACKAGE_NAME, nbanks, PACKAGE_NAME)

EPILOGUE = """ENDDRAW
ENDDEF
#
#End Library"""

with open(PINOUT_CSV, "r") as f:
  data = dict()
  reader = csv.reader(f)
  package_col = None
  for i, row in enumerate(reader):
    if i < 4 or len(row[0]) == 0:
      #print(row)
      if i == 3:
        if package_col is None:
          for j, r in enumerate(row):
            if packagename in r:
              package_col = j
              break
      continue
    name = row[0]
    num = row[package_col]
    #print(row)
    if num == '-':
      continue
    #num = int(num)
    ty = 'B'
    realtype = row[1]
    if realtype == 'GND':
      ty = 'P'
    elif realtype.startswith('VCC'):
      ty = 'W'
    elif realtype == 'LED':
      ty = 'w'
    data[num] = [name, ty]

  print(PROLOGUE)
  for b in range(nbanks):
    bankname = "ABCDEFGHJKLMNOP"[b] # NOTE: I is skipped
    for p in range(pinsperbank):
      pinname = bankname + str(p + 1)
      name = data[pinname][0]
      x = -200
      y = -150 - 100 * p
      ty = data[pinname][1]
      print("X {} {} {} {} 200 R 50 50 {} 1 {}".format(name, pinname, x, y, b + 1, ty))
  # add ground paddle pin
  print("X {} {} {} {} 200 R 50 50 {} 1 {}".format('GND', 0, -200, -150 - 100*pinsperbank, 1, 'P'))
  print(EPILOGUE)
