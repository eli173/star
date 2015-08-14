

import sqlite3
import json

from flask import Flask, request, session, g, redirect, \
    url_for, abort, render_template, flash
from contextlib import closing
import flask_login




#cfg
DATABASE = 'db.db'
#
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
def init_db():
    with closing(connect_(db)) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit


@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g,'db',None)
    if db is not None:
        db.close()


@app.route('/games')
@login_required
def games():
    pass

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('somewhere')

@app.route('/')
def index():
    return "hi!"







if __name__ == '__main__':
    app.run
