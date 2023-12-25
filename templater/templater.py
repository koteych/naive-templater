import os
import re
from functools import cmp_to_key

rootpath = '../folder_structures/1'
filelist = []

class CyclicDependencyError(Exception):
    def __init__(self, chain):
        self.chain = chain
        super().__init__(self.chain)

def get_required_directive_file(line):
    pattern = r"require\s+'([^']+)'"

    match = re.search(pattern, line)
    if match:
        return match.group(1)
    else:
        return None

def get_dependencies_of_file(filepath):
    filepath = rootpath + os.sep + filepath
    dependencies = []
    with open(filepath, 'r') as file:
        for line in file:
            dependency = get_required_directive_file(line)
            if dependency != None:
                dependencies.append(dependency)
    return dependencies

def make_filelist(directory, indent=''):    
    if os.path.isfile(directory):
        indent = indent + os.path.basename(directory)
        filelist.append(indent)
    else:
        indent = indent + os.path.basename(directory) + os.sep
        for item in os.listdir(directory):
            make_filelist(os.path.join(directory, item), indent)

make_filelist(rootpath)

_filelist = []

for path in filelist:
    _filelist.append(os.sep.join(path.split(os.sep)[1:]))

filelist = _filelist # this is ours file list

print(filelist)

detection_chain = []
def detect_cycles_for_file(rootfile):
    def recursion_helper(file):
        print('Analyzing file: ' + file)
        detection_chain.append(file)
        deps = get_dependencies_of_file(file)

        if len(deps) == 0:
            return
        
        for dep in deps:
            if dep == rootfile:
                print('Cycle detected: ' + str(detection_chain))
                raise CyclicDependencyError(detection_chain)
            
            recursion_helper(dep)

    recursion_helper(rootfile)



try:
    for file in filelist:
        detect_cycles_for_file('Folder 2/File 2-1')

        def dependency_comparator(a, b):
            adeps = get_dependencies_of_file(a)
            bdeps = get_dependencies_of_file(b)

            for dep in adeps:
                if dep == b:
                    return 1
                
            for dep in bdeps:
                if dep == a:
                    return -1

            return 0

        # first file has no dependencies
        filelist_sorted = sorted(filelist, key=cmp_to_key(dependency_comparator))

        print(filelist_sorted)

        # now we have to patch according to the list
except CyclicDependencyError as e:
    print("We've got cycle", e.chain)

