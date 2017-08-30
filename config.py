from pydash import objects
import process

_config = {
    'msn': {
        'api': {
            'method': 'get',
            'url': {
                'root': 'https://www.msn.com/en-us/money/getfilterresponse',
                'params': {
                    'filters'   :   'Country|USA',
                    'ranges'    :   'RtCap|0;13166~Mc|1000000000;10000000000~Pp|10;25~Nmp|0;2610~PrCh6Mo|0;10',
                    'sortedby'  :   'Mc',
                    'sortorder' :   'DSC',
                    'count'     :   100,
                    'offset'    :   0,
                    'market'    :   'USA',
                    'sectype'   :   'Stock',
                    'ver'       :   '2.0.6436.4302'
                }
            }
        }
    },
    'yahoo': {
        'api': {
            'method': 'get',
            'url': {
                'root': 'https://query1.finance.yahoo.com/v7/finance/chart/',
                'ticker': 'AAPL',
                'params': {
                    'corsDomain'        :   'finance.yahoo.com',
                    'includePrePost'    :   False,
                    'includeTimestamps' :   True,
                    'indicators'        :   'quote',
                    'interval'          :   '1m',
                    'period1'           :   1503063000,
                    'period2'           :   1503086400,
                }
            }
        },
        'rss': {
            'method': 'get',
            'url': {
                'root': 'http://finance.yahoo.com/rss/headline',
                'params': {
                    's'     : 'AAPL'
                }
            }
        }
    },
    'db': {
        'name': 'groundwire',
        'connections': 
            {'production': {
                'host': '127.0.0.1',
                'port': 5432,
                'user': {
                    'username': process.env['DB_USER'],
                    'password': process.env['DB_PASS']
                }
                },
            'development': {
                'host': '127.0.0.1',
                'port': 5432,
                'user': {
                    'username': process.env['DB_USER'],
                    'password': process.env['DB_PASS']
                }
                }
            }
    }
}

def get(path):
    return objects.get(_config, path)
