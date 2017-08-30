from Collection import Collection
from Newsitem import Newsitem

class Newsitems(Collection):
    def __init__(self, options=[]):
        Collection.__init__(self, options)

    def modelClass(self):
        return Newsitem