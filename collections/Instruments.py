from Collection import Collection
from Instrument import Instrument

class Instruments(Collection):
    def __init__(self, options=[]):
        Collection.__init__(self, options)
        self.modelClass = Instrument
