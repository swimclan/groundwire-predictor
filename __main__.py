import sys

# Setup module directories
from __setmodules__ import modulize
modulize('__models', '__lib', '__collections', '__controllers')

# Get datetime module
from datetime import datetime, date

# Get utils module
import utils

# Setup environment variables
import Process
process = Process.getInstance(open('trading-data/.env', 'r'))

program = sys.argv[1]

if process.env['MASTER_SWITCH'] == 'on':
    if program == 'collect':
        target_date = utils.parseISODate(sys.argv[2])
        # kick off data collection sequence    
        from Collector import Collector
        collector = Collector(target_date, False)
        collector.start()
    elif program == 'predict':
        from Collector import Collector
        collector = Collector(datetime.now(), True)
        collector.start()
    elif program == 'train':
        from Trainer import Trainer
        trainer = Trainer()
        trainer.start()

    else:
        print 'Invalid parameters given.  Shutting down...'

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

# dt = datetime(2017, 8, 23)
# print utils.previous_market_times(dt)

###################### S A M P L E  C O D E  E N D ##########################
