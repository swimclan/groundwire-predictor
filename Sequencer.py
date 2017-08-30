from Observations import Observations
from datetime import datetime
from Screener import Screener
from ChartAnalysis import ChartAnalysis
from Tickcharts import Tickcharts
from Tickchart import Tickchart
from News import News
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
        self.setNewsitems()
        self.initialize_observations()
        print '# charts initialized into observations:', self.observations.length
        self.setNumNewHighs()
        self.setNumNewLows()
        self.setTallestCandles()
        # print self.observations.at(19).toJSON()
        print self.charts.at(3).get('news').at(2).toJSON()


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
        self.charts.append(return_chart)
        return return_chart

    def getNumNewHighs(self, chart, index):
        print 'getNumNewHighs()'
        highs = chart.get('highs')
        times = chart.get('timestamps')
        volumes = chart.get('volumes')
        count = 0
        abvVolCount = 0
        blwVolCount = 0
        amCount = 0
        pmCount = 0
        avgVol = chart.get('avg_volume')
        max_high = 0
        for key, high in enumerate(highs):
            if high and high > max_high:
                max_high = high
                count += 1
                if volumes[key] > avgVol:
                    abvVolCount += 1
                else:
                    blwVolCount += 1
                if utils.isMorning(times[key]):
                    amCount += 1
                else:
                    pmCount += 1
        self.observations.at(index).set('num_new_highs', count)
        self.observations.at(index).set('num_highs_abv_avg_vol', abvVolCount)
        self.observations.at(index).set('num_highs_blw_avg_vol', blwVolCount)
        self.observations.at(index).set('num_new_highs_am', amCount)
        self.observations.at(index).set('num_new_highs_pm', pmCount)
        return count

    def setNumNewHighs(self):
        print 'setNumNewHighs()'
        self.charts.each(self.getNumNewHighs)

    def getNumNewLows(self, chart, index):
        print 'getNumNewLows()'
        lows = chart.get('lows')
        times = chart.get('timestamps')
        volumes = chart.get('volumes')
        count = 0
        abvVolCount = 0
        blwVolCount = 0
        amCount = 0
        pmCount = 0
        avgVol = chart.get('avg_volume')
        min_low = float('inf')
        for key, low in enumerate(lows):
            if low and low < min_low:
                min_low = low
                count += 1
                if volumes[key] > avgVol:
                    abvVolCount += 1
                else:
                    blwVolCount += 1
                if utils.isMorning(times[key]):
                    amCount += 1
                else:
                    pmCount += 1
        self.observations.at(index).set('num_new_lows', count)
        self.observations.at(index).set('num_lows_abv_avg_vol', abvVolCount)
        self.observations.at(index).set('num_lows_blw_avg_vol', blwVolCount)
        self.observations.at(index).set('num_new_lows_am', amCount)
        self.observations.at(index).set('num_new_lows_pm', pmCount)
        return count

    def setNumNewLows(self):
        print 'setNumNewLows()'
        self.charts.each(self.getNumNewLows)

    def getTallestCandles(self, chart, index):
        print 'getTallestCandles()'
        candles = chart.get('candlesticks').toJSON()
        tallestGreen = 0.0
        tallestRed = 0.0
        for candle in candles:
            if candle['color'] == 'green' and candle['relative_height'] > tallestGreen:
                tallestGreen = candle['relative_height']
            if candle['color'] == 'red' and candle['relative_height'] > tallestRed:
                tallestRed = candle['relative_height']
        self.observations.at(index).set('tallest_green_candlestick', tallestGreen)
        self.observations.at(index).set('tallest_red_candlestick', tallestRed)

    def setTallestCandles(self):
        print 'setTallestCandles()'
        self.charts.each(self.getTallestCandles)

    def getNewsitems(self, chart, index):
        print 'getNewsitems()'
        newsitems = News({'symbol': chart.get('symbol')})
        news = newsitems.fetch()
        chart.set('news', newsitems.get('items'))

    def setNewsitems(self):
        print 'setNewsitems()'
        self.charts.each(self.getNewsitems)

