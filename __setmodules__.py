import sys

global dirname

def modulize(*args):
    global dirname
    dirname = 'trading-data/'
    for arg in args:
        sys.path.insert(0, dirname + arg)