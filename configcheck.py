import os
import json
import sys
from lxml import etree

curr_dir = os.getcwd()
print("current working directory:",curr_dir)
arxmlfiles=[]
for dirpath, dirnames, filenames in os.walk(curr_dir):
  for file in filenames:
    if file.lower().endswith(".arxml"):
      arxmlfiles.append(os.path.join(dirpath, file))

print(arxmlfiles)
CONFIG_PATH = os.path.join(curr_dir, "config_check.json")

def configcheck(file_path, config_path):
  
  
  
