from urllib2 import urlopen
import json
from Model import Model
import process

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
        try:
            opener = urlopen(self.url, timeout=float(process.env['FETCH_TIMEOUT']))
            json_response = json.loads(opener.read())
        except:
            json_response = {}
        if type(json_response) is list:
            return self.populate(json_response)

    def each(self, callback):
        i = 0
        for model in self.models:
            callback(model, i)
            i += 1
        return True

    def append(self, model):
        SubModel = self.modelClass()
        if isinstance(model, Model):
            insert_model = SubModel(model.toJSON())
        else:
            insert_model=SubModel(model)
        self.models.append(insert_model)
        self.length += 1

    def destroy(self):
        self.models = []
        return self
