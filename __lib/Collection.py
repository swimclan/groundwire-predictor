from urllib2 import urlopen
import json

class Collection:
    def __init__(self, options=[]):
        self.models = []
        self.url = None
        self.length = 0
        self.populate(options)
    
    def modelClass(self):
        return None

    def populate(self, models):
        Model = self.modelClass()
        for model in models:
            self.models.append(Model(model))
            self.length += 1
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
            return self.populate(json_response)

    def each(self, callback):
        for model in self.models:
            callback(model)
        return True
