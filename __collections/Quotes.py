from Collection import Collection
from Quote import Quote

class Quotes(Collection):
    def __init__(self, options=[]):
        Collection.__init__(self, options)

    def modelClass(self):
        return Quote