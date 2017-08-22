from Model import Model
from Meta import Meta
from Indicator import Indicator

class Tool(Model):
    def __init__(self, options={}):
        Model.__init__(self, options)

    def props(self):
        return [
            'meta',
            'timestamp',
            'indicators'
        ]

    def children(self):
        return {
            'meta': Meta,
            'indicators': Indicator
        }
