import os

curr_dir = os.getcwd()
print("current working directory:",curr_dir)

for dirpath, dirnames, filenames in os.walk(curr_dir):
  for file in filenames:
    if file.lower().endswith(".arxml"):
      print(os.path.join(dirpath, file))
