from Model import Model
from Results import Results

class Chart(Model):
    def __init__(self, options={}):
        Model.__init__(self, options)

    def props(self):
        return [
            'result'
        ]

    def collections(self):
        return {
            'result': Results
        }