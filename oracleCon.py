import cx_Oracle
import config
from flask import g

def get_db():
    if 'db' not in g:
        g.db = cx_Oracle.connect(user = config.USER , password= config.PASSWORD, dsn= config.DSN, encoding="UTF-8")
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
