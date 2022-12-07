import os

# https://adventofcode.com/2022/day/7 - Day 7: No Space Left On Device

test_input = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

def add_dir(nm: str, parent):
    dir = { 'name': nm, 'parent': parent, 'dirs': {}, 'files': [] }
    if parent != None:
        parent['dirs'][nm] = dir
    return dir

def add_file(sz: int, name: str, parent):
    f = { 'name': name, 'size': sz }
    parent['files'].append(f)

def cd(to: str, current):
    if to == '/':
        dir = current
        while dir['parent'] != None:
            dir = dir['parent']
        return dir
    if to == '..':
        return current['parent']
    return current['dirs'][to]

def dir_size(dir, sizes, path):
    sz = 0
    dname = dir['name']
    fullname = path + '/' + dname

    for f in dir['files']:
        sz += f['size']
    for _,d in dir['dirs'].items():
        dsz = dir_size(d, sizes, fullname)
        sz += dsz
    sizes[fullname] = sz
    return sz

#lines = [line.strip().split() for line in test_input.splitlines()]
with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day07-input", "r") as f:
    lines = [line.strip().split() for line in f.readlines()]

# Build it
root = add_dir('root', None)
cwd = root
for line in lines[2:]:
    match line[0]:
        case '$':
            match line[1]:
                case 'cd':
                    cwd = cd(line[2], cwd)
                #case 'ls':
                #    print("ignore ls")
        case 'dir':
            # dir <dir-name>
            add_dir(line[1], cwd)
        case _:
            # file size and name
            add_file(int(line[0]), line[1], cwd)

# Analyse it
dir_sizes = {}
dir_size(root, dir_sizes, '')

free_space = 70000000 - dir_sizes['/root']
required = 30000000 - free_space

# print("Required extra space ", required)
# for path, sz in dir_sizes.items():
#     if sz >= needed:
#         print("Found ", path, sz)

print("Part 1: ", sum([sz for sz in dir_sizes.values() if sz <= 100000]))
print("Part 2: ", min([sz for sz in dir_sizes.values() if sz >= required]))
