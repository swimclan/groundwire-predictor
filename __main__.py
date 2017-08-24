# Setup module directories
from __setmodules__ import modulize
modulize('__models', '__lib', '__collections')

# Setup environment variables
import Process
process = Process.getInstance(open('trading-data/.env', 'r'))

# kick off data collection sequence
from Sequencer import Sequencer
sequencer = Sequencer()

###################### S A M P L E  C O D E  S T A R T ######################

# from Screener import Screener
# from ChartAnalysis import ChartAnalysis

# def printStock(stock):
#     print stock.get('Sym')

# screener = Screener().fetch()
# stocks = screener.get('DataList')

# stocks.each(printTicker)

# chart = ChartAnalysis({'startdate': 1503322200, 'enddate': 1503345600, 'ticker': 'GEVO'})
# chart.fetch()

# print chart.get('chart').get('result').at(0).get('indicators').get('quote').at(0).get('volume')

# from Observations import Observations
# observations = Observations().fetch()
# print observations.at(0).get('percent_change')

###################### S A M P L E  C O D E  E N D ##########################
