import argparse
import csv

def main():
  parser = argparse.ArgumentParser(description="Generates a Digikey BOM from Joost's KiCAD BOM")
  parser.add_argument("input", help="input BOM")
  parser.add_argument("output", help="output BOM")
  parser.add_argument("--m", help="quantity multiplier", default="1")

  args = parser.parse_args()
  multiplier = 1 if args.m is None else int(args.m)

  print("multiplier: {}".format(multiplier))

  digikey_idx = None
  count_idx = None
  components = []
  # TODO skip until it sees "Collated Components"
  with open(args.input, 'r') as f:
    reader = csv.reader(f)
    found_start = False
    for line_number, line in enumerate(reader):
      if not found_start:
        if any(["Collated" in p for p in line]):
          #print("header at {}".format(line_number + 1))
          found_start = True
        continue
      if digikey_idx is None or count_idx is None:
        for i, part in enumerate(line):
          if 'Digikey' == part:
            digikey_idx = i
          elif 'Qty' == part:
            count_idx = i
        continue
      if len(line) < max(digikey_idx, count_idx):
        print("[WARN] line {} is missing fields".format(line_number + 1))
        continue
      part_num = line[digikey_idx]
      count = line[count_idx]
      if len(part_num) == 0:
        print("[WARN] line {} is missing part number".format(line_number + 1))
        print(parts)
        continue
      if count == 0:
        print("[WARN] line {} has zero quantity".format(line_number + 1))
      if part_num == 'NoPart':
        continue
      components.append((part_num, count))

  with open(args.output, 'w') as f:
    # header is necessary if you don't want to miss the first part
    f.write("Digikey,Quantity\n")
    for c in components:
      f.write("\"{}\",{}\n".format(c[0], multiplier*int(c[1])))

if __name__ == "__main__":
  main()
