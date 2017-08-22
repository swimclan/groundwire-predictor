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
