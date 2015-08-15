#80#############################################################################

import sqlite3
import json

from flask import Flask, request, session, g, redirect, \
    url_for, abort, render_template, flash
from contextlib import closing
import bcrypt




#cfg
DATABASE = 'db.db'
#
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = b'\t\x00\x8dSAc\x1fM\x9e\x1d0!\x94\x90\xe0\x90\xda\xac\x1a\xdf\xaa3\xd5Q'


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

    
@app.route('/games')
def games():
    pass

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    app.logger.debug('logged out')
    return redirect(url_for("index"))

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        user = g.db.execute('select * from users where username=?',
                            (request.form.get('username'),))
        user_exists = len(user.fetchall())!=0
        if request.form.get('login')!=None:
            if request.form.get('username')==None:
                return redirect(url_for("index"))
            if not user_exists:
                flash(u'No account with this username exists','login error')
                return redirect(url_for("index"))
            pw_sql = g.db.execute('select pw_hash from users where username=?',
                                  (request.form.get('username'),))
            pw_hash = pw_sql.fetchall()[0][0]
            pw_plain = request.form.get('password').encode('UTF-8')
            if bcrypt.hashpw(pw_plain, pw_hash) == pw_hash:
                #app.logger.debug('success!')
                session['logged_in'] = True
            else:
                flash(u'Wrong Password','login error')
                return redirect(url_for("index"))
        elif request.form.get('register')!=None:
            if(user_exists):
                flash(u'Username already taken','login error')
                return redirect(url_for("index"))
            pw_plain = request.form.get('password').encode('UTF-8')
            pw_hash = bcrypt.hashpw(pw_plain, bcrypt.gensalt())
            g.db.execute('insert into users (username, pw_hash) values (?, ?)',
                         (request.form.get('username'),pw_hash))
            g.db.commit()
    return redirect(url_for("index"))
    

@app.route('/')
def index():
    return render_template('index.html')







if __name__ == '__main__':
    app.run
