import os
print("current working directory:",os.getcwd())
for item in os.listdir():
  if os.path.isdir(item):
    print(item)
