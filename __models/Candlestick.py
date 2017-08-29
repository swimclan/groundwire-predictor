from Model import Model

class Candlestick(Model):
    def __init__(self, options={}):
        Model.__init__(self, options)

    def props(self):
        return [
            'time',
            'high',
            'low',
            'open',
            'close',
            'absolute_height',
            'relative_height',
            'color',
            'volume',
            'doji'
        ]

    def onPopulate(self, candlestick):
        self.getColor()
        self.getDoji()
        self.getAbsoluteHeight()
        self.getRelativeHeight()

    def getColor(self):
        if (self.get('close') - self.get('open')) >= 0:
            self.set('color', 'green')
        else:
            self.set('color', 'red')

    def getDoji(self):
        doji = (self.get('open') == self.get('close')) and (self.get('high') > self.get('low'))
        self.set('doji', doji)

    def getAbsoluteHeight(self):
        abs_height = abs(self.get('close') - self.get('open'))
        self.set('absolute_height', abs_height)

    def getRelativeHeight(self):
        if self.get('color') == 'green':
            rel = self.get('absolute_height') / self.get('open')
        else:
            rel = self.get('absolute_height') / self.get('close')
        self.set('relative_height', rel)