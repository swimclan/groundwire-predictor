from urllib2 import urlopen
import json

class Collection:
    def __init__(self, options=[]):
        self.models = []
        self.url = None
        self.modelClass = None
        self._populate(options)
    
    def _populate(self, models):
        for model in models:
            self.models.append(self.modelClass(model))
        return self

    def toJSON(self):
        ret = []
        for model in self.models:
            ret.append(model.toJSON())
        return ret

    def at(self, index):
        if (index + 1) <= len(self.models):
            return self.models[index]
        else:
            raise ValueError("Index outside of collection range")
    
    def fetch(self):
        opener = urlopen(self.url)
        json_response = json.loads(opener.read())
        print type(json_response)
        if type(json_response) is list:
            return self._populate(json_response)
