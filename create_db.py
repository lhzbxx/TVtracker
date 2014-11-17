#-*- coding: utf-8 -*-

from __future__ import with_statement
import sqlite3
import os
from flask import *
from contextlib import closing

app = Flask(__name__)

DATABASE = os.getcwd() + '/database/eh.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def init_db():
    print DATABASE
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

if __name__ == "__main__":
    init_db()
