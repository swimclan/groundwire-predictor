from Model import Model
from Candlesticks import Candlesticks
from Newsitems import Newsitems
import utils
from datetime import datetime, timedelta

class Tickchart(Model):
    def __init__(self, options={}):
        Model.__init__(self, options)

    def props(self):
        return [
            'num_ticks',
            'market_open_datetime',
            'market_close_datetime',
            'opens',
            'closes',
            'highs',
            'lows',
            'symbol',
            'volumes',
            'timestamps',
            'avg_volume',
            'percent_change',
            'candlesticks',
            'news',
            'news_age',
            'last_close',
            'next_market_open_margin'
        ]

    def collections(self):
        return {
            'candlesticks': Candlesticks,
            'news': Newsitems
        }

    def onPopulate(self, chart):
        self.set('num_ticks', len(self.get('opens')))
        self.setAvgVolume()
        self.setMarketTimes()
        self.normalizePrices()
        self.setPercentChange()
        self.setLastClose()
        self.setCandlesticks()

    def onChange(self, data):
        if utils.has(data, 'news'):
            self.set('news_age', self.getNewsAge(data['news'].toJSON()))

    def setAvgVolume(self):
        volumes = self.get('volumes')
        new_vols = utils.map(volumes, self.__zeroNonesVol)
        self.set('volumes', new_vols)
        avg = utils.average(new_vols)
        self.set('avg_volume', avg)
        return avg

    def __zeroNonesVol(self, volume, i, arr):
        if not volume:
            return 0
        else:
            return volume

    def setMarketTimes(self):
        self.set('market_open_datetime', datetime.fromtimestamp(self.get('timestamps')[0]))
        self.set('market_close_datetime', datetime.fromtimestamp(self.get('timestamps')[self.get('num_ticks')-1]))

    def normalizePrices(self):
        highs = self.get('highs')
        lows = self.get('lows')
        closes = self.get('closes')
        opens = self.get('opens')
        new_highs = utils.map(highs, self.__flattenNonesPrice)
        new_lows = utils.map(lows, self.__flattenNonesPrice)
        new_opens = utils.map(opens, self.__flattenNonesPrice)
        new_closes = utils.map(closes, self.__flattenNonesPrice)

        self.set('highs', new_highs)
        self.set('lows', new_lows)
        self.set('opens', new_opens)
        self.set('closes', new_closes)

    def __flattenNonesPrice(self, price, index, prices):
        if not price and index > 0:
            current_index = index
            current_price = prices[current_index]
            while not current_price:
                current_index -= 1
                if prices[current_index]:
                    current_price = prices[current_index]
                    return current_price
        elif not price:
            return 0
        else:
            return price

    def setPercentChange(self):
        num_ticks = len(self.get('timestamps'))
        i = 0
        open = self.get('opens')[i]
        while open == 0:
            i += 1
            open = self.get('opens')[i]
        close = self.get('closes')[num_ticks-1]
        percent_change = (close - open) / open
        self.set('percent_change', percent_change)

    def setCandlesticks(self):
        candlesticks = Candlesticks()
        highs = self.get('highs')
        lows = self.get('lows')
        opens = self.get('opens')
        closes = self.get('closes')
        times = self.get('timestamps')
        for key, time in enumerate(times):
            candlesticks.append({
                'time': time,
                'high': highs[key],
                'low': lows[key],
                'open': opens[key],
                'close': closes[key]
            })
        self.set('candlesticks', candlesticks)

    def getNewsAge(self, news):
        newest_age = timedelta(days=365, hours=0, minutes=0, seconds=0)
        now = datetime.utcnow()
        for headline in news:
            age = now - headline['pubDate']
            if age < newest_age:
                newest_age = age
                newest_headline = headline
        return int(newest_age.total_seconds() / 60 / 60)


    def setLastClose(self):
        last_index = len(self.get('closes')) - 1
        self.set('last_close', self.get('closes')[last_index])
