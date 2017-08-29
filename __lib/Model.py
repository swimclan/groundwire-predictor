from urllib2 import urlopen
import json
import utils as _
import process

class Model:
    def __init__(self, options={}):
        self.url = None
        self.attributes = {}
        self.__populate(options)
    
    def props(self):
        return []

    def collections(self):
        return {}

    def children(self):
        return {}

    def get(self, prop):
        return self.attributes[prop]

    def set(self, prop, value):
        if _.index_of(self.props(), prop) != -1:
            self.attributes[prop] = value
            self.onChange({prop: value})
            return self
        else:
            raise ValueError("Invalid model property passed: %s" % property)
    
    def toJSON(self):
        return self.attributes
    
    def __populate(self, options):
        for prop in self.props():
            if _.has(options, prop):
                if _.has(self.children(), prop):
                    self.attributes[prop] = self.children()[prop](options[prop])
                elif _.has(self.collections(), prop):
                    if isinstance(options[prop], list):
                        self.attributes[prop] = self.collections()[prop](options[prop])
                    else:
                        self.attributes[prop] = options[prop]
                else:
                    self.attributes[prop] = options[prop]
        self.onPopulate(self.toJSON())
        return self

    def fetch(self):
        try:
            opener = urlopen(self.url, timeout=float(process.env['FETCH_TIMEOUT']))
            json_response = json.loads(opener.read())
        except:
            json_response = {}
        self.__populate(json_response)
        return self

    def has(self, prop):
        return _.has(self.attributes, prop)

    def destroy(self):
        self.attributes = {}

    def onPopulate(self, obj={}):
        return None

    def onChange(self, obj):
        return None
