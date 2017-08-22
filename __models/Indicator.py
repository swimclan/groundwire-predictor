from Model import Model
from Quotes import Quotes

class Indicator(Model):
    def __init__(self, options={}):
        Model.__init__(self, options)
    
    def props(self):
        return [
            'quote'
        ]
    
    def collections(self):
        return {
            'quote': Quotes
        }