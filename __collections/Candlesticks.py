from Collection import Collection
from Candlestick import Candlestick

class Candlesticks(Collection):
    def __init__(self, options=[]):
        Collection.__init__(self, options)

    def modelClass(self):
        return Candlestick