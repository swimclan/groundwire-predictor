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
        self.db.connect()
        try:
            data = self.db.fetchall()
            print 'Successfully fetched observations'
        except:
            data = []
            print 'ERROR! Unable to fetch observations'
        self.populate(data)
        self.db.close()
        return self

    def create(self):
        self.db.connect()
        for item in self.toJSON():
            self.db.create(item)
        self.db.commit()
        self.db.close()
        return self