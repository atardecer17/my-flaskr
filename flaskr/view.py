from flaskr import app
from flask import request, url_for, g, redirect, render_template, session, abort, flash
import sqlite3

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/login', methods=['GET'])
def login():
    return render_template('login_new.html')

@app.route('/login', methods=['POST'])
def login_info():
    username = request.form['username']
    password = request.form['password']
    error = 'bad username or password'

    if username == app.config['USERNAME'] and password == app.config['PASSWORD']:
        session['logged_in'] = 1
        flash('You were logged in')
        return redirect(url_for('index', _external=True))
    return render_template('login_new.html', error=error)			

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index', _external=True))
            
@app.route('/', methods=['GET'])
def index():
    cur = g.db.execute('SELECT title, text FROM content ORDER BY id DESC')
    content = [dict(title=row[0], text=row[1])   for row in cur.fetchall()]
    return render_template('blog_new.html', content=content)

@app.route('/', methods=['POST'])
def submit():
    if not session.get('logged_in'):
        flash('Please login')
        return redirect(url_for('index', _external=True))

    title = request.form['title']
    text = request.form['text']	
    if title and text:
        g.db.execute('INSERT INTO content(title,text)  VALUES(?, ?)', (title, text))
        g.db.commit()
        flash('New entry was successfully posted')
        return redirect(url_for('index', _external=True))

    flash('Empty can\'t be posted')
    return redirect(url_for('index', _external=True))
