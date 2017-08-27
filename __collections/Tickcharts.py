from Collection import Collection
from Tickchart import Tickchart

class Tickcharts(Collection):
    def __init__(self, options=[]):
        Collection.__init__(self, options)

    def modelClass(self):
        return Tickchart