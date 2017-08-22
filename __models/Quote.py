from Model import Model

class Quote(Model):
    def __init__(self, options={}):
        Model.__init__(self, options)

    def props(self):
        return [
            'high',
            'low',
            'close',
            'open',
            'volume'
        ]