from __setmodules__ import modulize
modulize('./__models', './__lib', './__collections')

from Screener import Screener
from ChartAnalysis import ChartAnalysis

def printStock(stock):
    print stock.get('Sym')

screener = Screener().fetch()
stocks = screener.get('DataList')

# stocks.each(printTicker)

chart = ChartAnalysis({'startdate': 1503322200, 'enddate': 1503345600, 'ticker': 'GEVO'})
chart.fetch()

print chart.get('chart').get('result').at(0).get('indicators').get('quote').at(0).get('volume')
