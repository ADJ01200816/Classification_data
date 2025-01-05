
from setting import *
import classify
import read_information
import tools
file_path = language + '/data/example/example.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    file_info = file.readlines()
file.close()
name = []
level = []
for info in file_info:
    info = info.split('|')
    level.append(info[0])
    name.append(info[1][0:len(info[1])-1])
print(level)
print(name)
