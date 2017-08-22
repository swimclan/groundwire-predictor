from Model import Model
from Chart import Chart
from urllib import urlencode
import utils
import config

class ChartAnalysis(Model):
    def __init__(self, options={}):
        Model.__init__(self, options)
        params = config.get('yahoo.api.url.params')
        if utils.has(options, 'startdate') and utils.has(options, 'enddate'):
            params['period1'] = options['startdate']
            params['period2'] = options['enddate']
        if utils.has(options, 'granularity'):
            params['interval'] = options['granularity']
        if utils.has(options, 'ticker'):
            ticker = options['ticker']
        else:
            ticker = config.get('yahoo.api.url.ticker')
        self.url = config.get('yahoo.api.url.root') + ticker + '?' + urlencode(params)

    def props(self):
        return [
            'chart'
        ]
    
    def children(self):
        return {
            'chart': Chart
        }