import psycopg2
from psycopg2.extras import DictCursor
import config
import process
import sys
import utils

class Database:
    def connect(self):
        dbuser = {
            'username': config.get('db.connections.%s.user.username' % process.env['DB_ENV']),
            'password': config.get('db.connections.%s.user.password' % process.env['DB_ENV'])
        }
        dbname = config.get('db.name')
        dbhost = config.get('db.connections.%s.host' % process.env['DB_ENV'])
        dbport = config.get('db.connections.%s.port' % process.env['DB_ENV'])
        
        self.connection = psycopg2.connect('host=%s port=%s dbname=%s user=%s password=%s' % (dbhost, dbport, dbname, dbuser['username'], dbuser['password']))
        self.cursor = self.connection.cursor(cursor_factory=DictCursor)

    def fetchall(self):
        executor = self.cursor.execute('SELECT * FROM observations;')
        return self.cursor.fetchall()

    def fetchonebyid(self, id):
        executor = self.cursor.execute('SELECT * FROM observations WHERE id = %s;' % id)
        return self.cursor.fetchone()

    def create(self, item):
        query = 'INSERT INTO observations %s VALUES %s;' % utils.dictList(item)
        try:
            if int(process.env['DB_WRITE']) != 0:
                executor = self.cursor.execute(query)
                print 'Successfully inserted observation'
            else:
                print 'DB Write disabled.  No insert performed'
        except Exception, e:
            print sys.exc_info()
            print e.pgerror
        self.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()

    def commit(self):
        self.connection.commit()
