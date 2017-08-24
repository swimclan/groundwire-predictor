import psycopg2
from psycopg2.extras import DictCursor
import config
import process

class Database:
    def __init__(self):
        dbuser = {
            'username': config.get('db.connections.%s.user.username' % process.env['DB_ENV']),
            'password': config.get('db.connections.%s.user.password' % process.env['DB_ENV'])
        }
        dbname = config.get('db.name')
        dbhost = config.get('db.connections.%s.host' % process.env['DB_ENV'])
        dbport = config.get('db.connections.%s.port' % process.env['DB_ENV'])
        
        self.connection = psycopg2.connect('host=%s port=%s dbname=%s user=%s' % (dbhost, dbport, dbname, dbuser['username']))
        self.cursor = self.connection.cursor(cursor_factory=DictCursor)


    def fetchall(self):
        executor = self.cursor.execute('SELECT * FROM observations;')
        return self.cursor.fetchall()

    def fetchonebyid(self, id):
        executor = self.cursor.execute('SELECT * FROM observations WHERE id = %s;' % id)
        return self.cursor.fetchone()

    def close(self):
        self.cursor.close()
        self.connection.close()
