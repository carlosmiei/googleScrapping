import os

path = '/home/pc/Desktop/work2/result'

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        file = file.split('.')
        file = file[0]
        files.append(file)

missing = []
for i in range(30000):
    if not (str(i) in files):
        missing.append(i)
# os que faltam
print('tamanho',len(missing))

