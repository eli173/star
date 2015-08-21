#80#############################################################################

import sqlite3
import json

from flask import Flask, request, session, g, redirect, \
    url_for, abort, render_template, flash
from contextlib import closing
import bcrypt

import game


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
    if 'logged_in' not in session:
        return redirect(url_for("index"))
    uname = session['username']
    uid = g.db.execute('select id from users where username=?',(uname,))
    games = g.db.execute('select * from games where player1=? or player2=?',
                            (uname,uname)).fetchall()
    glist = []
    for game in games:
        if game['player1'] == uname:
            glist.append((game['player2'],game['whose_turn']==0))
        else:
            glist.append((game['player1'],game['whose_turn']!=0))
    return render_template('games.html')
    
@app.route('/newgame')
def newgame():
    if 'logged_in' not in session:
        return redirect(url_for("index"))
    app.logger.debug(session['username'])
    uid = g.db.execute('select id from users where username=?',
                       (session['username'],)).fetchall()[0][0]
    waiting = g.db.execute('select * from waiting').fetchall()
    app.logger.debug(waiting)
    if len(waiting)!=0:
        opp_id = waiting[0][1]
        app.logger.debug(waiting)
        g.db.execute('delete from waiting where id=?',(waiting[0][0],))
        g.db.execute('insert into games (player1, player2, whose_turn) values (?,?,?)',
                     (uid,opp_id,0))
        g.db.commit()
        return redirect(url_for("play"))
    app.logger.debug('len is 0')
    g.db.execute('insert into waiting (player) values (?)',(uid,))
    g.db.commit()
    return redirect(url_for("games")) # how to tell if on waitlist?

@app.route('/play/<int:game_id>')
def play(game_id):
    g.game_id = game_id
    db_gm = g.db.execute('select * from games where id=?',(game_id,)).fetchall()
    if db_gm == []:
        redirect(url_for("games"))
    the_gm = game.Game(db_gm[0][3],db_gm[0][4],db_gm[0][0])
    the_gm.import_string(db_gm[0][1])
    app.logger.debug(db_gm[0][1])
    g.color_table = {}
    cell_list = []
    for cg in game.cell_groups:
        cell_list += cg
    for cell in cell_list:
        curr_color = "ffff00"
        if cell in the_gm.p1_cells:
            curr_color = "ff0000"
        elif cell in the_gm.p2_cells:
            curr_color = "0000ff"
        g.color_table[cell] = curr_color
    return render_template('play.html')

@app.route('/submit/<int:game_id>/<move>')
def submit(game_id, move):
    # get game from db
    app.logger.debug(g.db.execute('select name from sqlite_master where type = "table"').fetchall())
    db_gm = g.db.execute('select * from games where id=?',(game_id,))
    gdata = db_gm.fetchall()
    if gdata == []:
        return redirect("index")
    app.logger.debug(gdata)
    the_gm = game.Game(gdata[0][3],gdata[0][4],game_id)
    the_gm.import_string(gdata[0][1])
    # check right user
    curr_user = session['username']
    user_id_q = g.db.execute('select id from users where username=?',
                             (curr_user,)).fetchall()
    if user_id_q == []:
        return redirect(url_for("play",game_id=game_id))
    app.logger.debug(move)
    uid = user_id_q[0][0]
    if uid!=gdata[0][2]: # don't need to do more than this
        return redirect(url_for("play",game_id=game_id))
    # checks move valid
    app.logger.debug(the_gm.open_cells)
    if move not in the_gm.open_cells:
        return redirect(url_for("play",game_id=game_id))
    # do it?
    the_gm.move(uid,move)
    estr = the_gm.export_string()
    app.logger.debug(game_id)
    g.db.execute('update games set board=? where id=?',(estr,game_id))
    g.db.commit()
    return redirect(url_for("play",game_id=game_id))

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
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
                session['username'] = request.form.get('username')
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
