from Model import Model

class Newsitem(Model):
    def __init__(self, options={}):
        Model.__init__(self, options)
    
    def props(self):
        return [
            'title',
            'pubDate',
            'link',
            'guid',
            'description'
        ]