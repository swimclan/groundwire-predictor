from Model import Model
from Newsitems import Newsitems
import RSSParse as rss
from urllib import urlencode
from urllib2 import urlopen
import process
import utils
import config

class News(Model):
    def __init__(self, options={}):
        Model.__init__(self, options)
        params = {}
        if utils.has(options, 'symbol'):
            params['s'] = options['symbol']
        else:
            params = config.get('yahoo.rss.url.params')

        self.url = config.get('yahoo.rss.url.root') + '?' + urlencode(params)

    def props(self):
        return [
            'title',
            'link',
            'lastBuildDate',
            'language',
            'items',
            'copyright',
            'description'
        ]

    def collections(self):
        return {
            'items': Newsitems
        }

    def fetch(self):
        try:
            opener = urlopen(self.url, timeout=float(process.env['FETCH_TIMEOUT']))
            json_response = rss.parse(opener.read())
        except:
            json_response = {}
        if type(json_response) is dict:
            self.onFetch(json_response)
        return self
        
