from flask import Flask
import sqlite3
from contextlib import closing

DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'myflaskr'
USERNAME = 'admin'
PASSWORD = 'password'

app = Flask(__name__)
app.config.from_object(__name__)

from flaskr import view
