from Observations import Observations
from Observation import Observation
from datetime import datetime
from Screener import Screener
from ChartAnalysis import ChartAnalysis
import utils
import re

class Sequencer:
    def __init__(self, dt=datetime.now()):
        print 'Sequencer initialized...'
        self.observations = Observations()
        self.observation = Observation()
        print 'Observations instance initialized with length:', self.observations.length
        self.today = dt
        self.yesterday_market_times = utils.previous_market_times(self.today)
        self.charts = []

    def start(self):
        self.sequence()

    def sequence(self):
        self.getInstruments()
        self.instruments.each(self.getChart)
        self.initialize_observations()
        for chart in self.charts: self.getNumNewHighs(chart)

    def initialize_observations(self):
        for chart in self.charts:
            self.observations.append({'symbol': chart['symbol']})
        print self.observations.length

    def getInstruments(self):
        self.screener = Screener()
        screener_model = self.screener.fetch()
        self.instruments = screener_model.get('DataList')

    def getChart(self, instrument):
        symbol = instrument.get('Eqsm')
        regex = re.compile(r'(\S+[\.\/]\S+$)', re.I)
        search_symbol = regex.search(symbol)
        if search_symbol:
            return {}
        chart_instance = ChartAnalysis({
            'startdate': self.yesterday_market_times[0],
            'enddate': self.yesterday_market_times[1],
            'ticker': symbol
        })
        chart = chart_instance.fetch()
        results = chart.get('chart').get('result').at(0)
        timestamps = results.get('timestamp')
        opens = results.get('indicators').get('quote').at(0).get('open')
        closes = results.get('indicators').get('quote').at(0).get('close')
        highs = results.get('indicators').get('quote').at(0).get('high')
        lows = results.get('indicators').get('quote').at(0).get('low')
        return_chart = {
            'symbol': symbol,
            'timestamps': timestamps,
            'opens': opens,
            'closes': closes,
            'highs': highs,
            'lows': lows
        }
        self.charts.append(return_chart)
        return return_chart

    def getNumNewHighs(self, chart):
        count = 0
        max_high = 0
        for high in chart['highs']:
            if high > max_high:
                max_high = high
                count += 1
        self.observation.set('num_new_highs', count)
        return count
