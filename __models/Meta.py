from Model import Model

class Meta(Model):
    def __init__(self, options={}):
        Model.__init__(self, options)

    def props(self):
        return [
            'currency',
            'symbol'
            'exchangeName',
            'instrumentType',
            'firstTradeDate',
            'gmtoffset',
            'timezone',
            'exchangeTimezoneName',
            'previousClose',
            'scale',
            'dataGranularity'
        ]