from Model import Model
import utils

class Tickchart(Model):
    def __init__(self, options={}):
        Model.__init__(self, options)
    
    def props(self):
        return [
            'opens',
            'closes',
            'highs',
            'lows',
            'symbol',
            'volumes',
            'timestamps',
            'avg_volume'
        ]

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
        

