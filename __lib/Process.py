import utils

class Process:
    def __init__(self, file):
        self.env = utils.parse_env(file)

global instance
instance = None

def getInstance(file=None):
    global instance
    if not instance:
        instance = Process(file)
    return instance
