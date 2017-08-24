# utils module with functions from lodash

def has(obj, target):
    ret = False
    for key, val in obj.iteritems():
        if target == key:
            ret = True
    return ret

def index_of(arr, target):
    ret = -1
    for idx, val in enumerate(arr):
        if target == val:
            ret = idx
    return ret

def parse_env(file):
    ret = {}
    for line in file.readlines():   
        line_list = line.split('=')
        ret[line_list[0]] = line_list[1][0:-1]

    return ret
