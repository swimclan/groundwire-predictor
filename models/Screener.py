from Model import Model
from urllib import urlencode
from Instruments import Instruments
import config

class Screener(Model):
    def __init__(self, options={}):
        Model.__init__(self, options)
        self.url = config.get('msn.api.url.root') + '?' + urlencode(config.get('msn.api.url.params'))

    def props(self):
        return [
            'Count',
            'DataList'
        ]

    def collections(self):
        return {
            DataList: Instruments
        }