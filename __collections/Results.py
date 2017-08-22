from Collection import Collection
from Tool import Tool

class Results(Collection):
    def __init__(self, options=[]):
        Collection.__init__(self, options)

    def modelClass(self):
        return Tool