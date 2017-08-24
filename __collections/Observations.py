from Collection import Collection
from Observation import Observation
from db import Database as db

class Observations(Collection):
    def __init__(self, options=[]):
        Collection.__init__(self, options)
        self.db = db()
    
    def modelClass(self):
        return Observation
    
    def fetch(self):
        data = self.db.fetchall()
        self.populate(data)
        self.db.close()
        return self