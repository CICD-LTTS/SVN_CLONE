import os
import json
import sys
from openpyxl import Workbook
from lxml import etree

curr_dir = os.getcwd()
print("current working directory:",curr_dir)
arxmlfiles=[]
for dirpath, dirnames, filenames in os.walk(curr_dir):
  for file in filenames:
    if file.lower().endswith(".arxml"):
      arxmlfiles.append(os.path.join(dirpath, file))

print(arxmlfiles)
ARXML_PATH = os.path.join(curr_dir, "test.arxml")
CONFIG_PATH = os.path.join(curr_dir, "config_check.json")





def configcheck(file_path, config_path):
  try:
    with open(config_path, "r", encoding="utf-8") as f:
      CONFIG = json.load(f)
  except Exception as e:
    print(f"CONFIG_ERROR: {e}")
    print("RESULT=FALSE")
    sys.exit(1)
    
  try:
    tree = etree.parse(file_path)
  except Exception as e:
    print(f"XML PARSING ERROR: {e}")
    print("RESULT=FALSE")
    sys.exit(1)

  all_ok = True
  details = []

  for element_name, allowed_values in CONFIG.items():
    nodes = tree.findall(f".//{element_name}")
    if not nodes:
      all_ok = False
      details.append(f"{element_name}: MISSING")
      continue

    values = [(n.text or "").strip() for n in nodes]

    if element_name == "Baudrate":
      range_str = allowed_values[0]
      try:
        min_val, max_val = map(int, range_str.split("-"))
      except:
        all_ok = False
        details.append(f"Baudrate: INVALID FORMAT FOR CONFIG. SHOULD BE RANGE")
        continue

      invalid_nums=[]
      for v in values:
        try:
          num = int(v)
          if not (min_val <= num <= max_val):
            invalid_nums.append(v)
        except:
          invalid_nums.append(v)

      if invalid_nums:
        all_ok = False
        details.append(f"Baudrate: INVALID -> {', '.join(invalid_nums)} ; allowed range = {min_val}-{max_val}")

    else:
      invalid = [v for v in values if v not in allowed_values]

      if invalid:
        all_ok = False
        details.append(f"{element_name}: INVALID -> {', '.join(invalid)} ; allowed range = {allowed_values}")

  print("CONFIG CHECK SUMMARY FOR:", file_path)
  if details:
    for line in details:
      print(line)
  else:
    print("ALL OK!")
  result = "TRUE" if all_ok else "FALSE"
  print(f"RESULT={result}")

for item in arxmlfiles:
  configcheck(item, CONFIG_PATH)

wb=Workbook()
ws=wb.active
ws.title = "Config Check"
ws.append(["File Check","Status","Value in arxml", "Allowed Values"])
wb.save("Config_Report.xlsx")


