from Model import Model
from Newsitems import Newsitems
import RSSParse as rss
from urllib import urlencode
from urllib2 import urlopen, Request
import process
import utils
import config
import json
import base64

class News(Model):
    def __init__(self, options={}):
        Model.__init__(self, options)
        params = {}
        if utils.has(options, 'symbol'):
            params['identifier'] = options['symbol']
        else:
            params = config.get('intrinio.api.url.params')

        self.url = config.get('intrinio.api.url.root') + '?' + urlencode(params)

    def props(self):
        return [
            'data'
        ]

    def collections(self):
        return {
            'data': Newsitems
        }

    def fetch(self):
        request = Request(self.url)
        base64string = base64.b64encode('%s:%s' % (process.env['INTRINIO_USER'], process.env['INTRINIO_PASS']))
        request.add_header("Authorization", "Basic %s" % base64string)
        try:
            opener = urlopen(url=request, timeout=float(process.env['FETCH_TIMEOUT']))
            json_response = json.loads(opener.read())
        except:
            json_response = {}
        if type(json_response) is dict:
            ret = {'data': []}
            try:
                ret['data'] = utils.serializeNews(json_response['data'])
            except:
                print 'No data response from news fetch'
            self.onFetch(ret)
        return self
