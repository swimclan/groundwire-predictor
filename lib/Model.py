import pydash as _
from urllib2 import urlopen
import json

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

    def get(self, property):
        return self.attributes[property]

    def set(self, property, value):
        if _.arrays.index_of(self.props(), property) != -1:
            self.attributes[property] = value
            return self
        else:
            raise ValueError("Invalid model property passed: %s" % property)

    
    def toJSON(self):
        return self.attributes
    
    def __populate(self, options):
        for prop in self.props():
            if _.objects.has(options, prop):
                if _.objects.has(self.children(), prop):
                    self.attributes[prop] = self.children()[prop](options[prop])
                elif _.objects.has(self.collections, prop):
                    self.attributes[prop] = self.collections()[prop](options[prop])
                else:
                    self.attributes[prop] = options[prop]
        return self

    def fetch(self):
        opener = urlopen(self.url)
        json_response = json.loads(opener.read())
        self.__populate(json_response)
        return self
