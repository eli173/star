

import sqlite3
import json

from flask import Flask, request, session, g, redirect, \
    url_for, abort, render_template, flash
from contextlib import closing





#cfg
DATABASE = 'db.db'
#
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = b'\t\x00\x8dSAc\x1fM\x9e\x1d0!\x94\x90\xe0\x90\xda\xac\x1a\xdf\xaa3\xd5Q'


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
def init_db():
    with closing(connect_(db)) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()




@app.route('/games')
def games():
    pass

@app.route('/logout')
def logout():
    pass#return redirect('somewhere')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        #login
        session['username'] = request.form.get('username')
    return redirect(url_for("index"))
    

@app.route('/')
def index():
    return render_template('index.html')







if __name__ == '__main__':
    app.run
