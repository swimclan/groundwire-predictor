from Observations import Observations
from datetime import datetime
from Screener import Screener
from ChartAnalysis import ChartAnalysis
from Tickcharts import Tickcharts
from Tickchart import Tickchart
import utils
import re

class Sequencer:
    def __init__(self, dt=datetime.now()):
        print 'Sequencer initialized...'
        self.observations = Observations()
        print 'Observations instance initialized with length:', self.observations.length
        self.today = dt
        self.yesterday_market_times = utils.previous_market_times(self.today)
        self.charts = Tickcharts()

    def start(self):
        self.sequence()

    def sequence(self):
        self.getInstruments()
        self.instruments.each(self.getChart)
        self.initialize_observations()
        print '# charts initialized into observations:', self.observations.length
        self.setNumNewHighs()
        self.setNumNewLows()
        print self.observations.at(18).toJSON()
        print self.charts.at(18).toJSON()


    def appendObservation(self, model, index):
        self.observations.append(model)

    def initialize_observations(self):
        print 'initialize_observations()'
        self.charts.each(self.appendObservation)

    def getInstruments(self):
        print 'getInstruments()'
        self.screener = Screener()
        screener_model = self.screener.fetch()
        self.instruments = screener_model.get('DataList')

    def getChart(self, instrument, index):
        print 'getChart()'
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
        print chart_instance.url
        chart = chart_instance.fetch()
        results = chart.get('chart').get('result').at(0)
        if not results.has('timestamp'):
            return None
        timestamps = results.get('timestamp')
        opens = results.get('indicators').get('quote').at(0).get('open')
        closes = results.get('indicators').get('quote').at(0).get('close')
        highs = results.get('indicators').get('quote').at(0).get('high')
        lows = results.get('indicators').get('quote').at(0).get('low')
        volumes = results.get('indicators').get('quote').at(0).get('volume')
        return_chart = Tickchart({
            'symbol': symbol,
            'timestamps': timestamps,
            'opens': opens,
            'closes': closes,
            'highs': highs,
            'lows': lows,
            'volumes': volumes
        })
        return_chart.setAvgVolume()
        return_chart.normalizePrices()
        self.charts.append(return_chart)
        return return_chart

    def getNumNewHighs(self, chart, index):
        print 'getNumNewHighs()'
        count = 0
        abvVolCount = 0
        blwVolCount = 0
        avgVol = chart.get('avg_volume')
        max_high = 0
        for key, high in enumerate(chart.get('highs')):
            if high and high > max_high:
                max_high = high
                count += 1
                if chart.get('volumes')[key] > avgVol:
                    abvVolCount += 1
                else:
                    blwVolCount += 1
        self.observations.at(index).set('num_new_highs', count)
        self.observations.at(index).set('num_highs_abv_avg_vol', abvVolCount)
        self.observations.at(index).set('num_highs_blw_avg_vol', blwVolCount)
        return count

    def setNumNewHighs(self):
        print 'setNumNewHighs()'
        self.charts.each(self.getNumNewHighs)

    def getNumNewLows(self, chart, index):
        print 'getNumNewLows()'
        count = 0
        abvVolCount = 0
        blwVolCount = 0
        avgVol = chart.get('avg_volume')
        min_low = float('inf')
        for key, low in enumerate(chart.get('lows')):
            if low and low < min_low:
                min_low = low
                count += 1
                if chart.get('volumes')[key] > avgVol:
                    abvVolCount += 1
                else:
                    blwVolCount += 1
        self.observations.at(index).set('num_new_lows', count)
        self.observations.at(index).set('num_lows_abv_avg_vol', abvVolCount)
        self.observations.at(index).set('num_lows_blw_avg_vol', blwVolCount)
        return count

    def setNumNewLows(self):
        print 'setNumNewLows()'
        self.charts.each(self.getNumNewLows)
