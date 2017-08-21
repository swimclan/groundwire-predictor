import sys

def modulize(*args):
    for arg in args:
        sys.path.insert(0, arg)