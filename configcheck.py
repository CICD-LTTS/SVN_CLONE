import os

curr_dir = os.getcwd()
print("current working directory:",curr_dir)
arxmlfiles=[]
for dirpath, dirnames, filenames in os.walk(curr_dir):
  for file in filenames:
    if file.lower().endswith(".arxml"):
      arxmlfiles.append(os.path.join(dirpath, file))

print(arxmlfiles)
