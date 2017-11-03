import sqlite3
from flask import Flask, request, session, g,\
 redirect, url_for, abort, render_template, flash


def create_db():
	conn = sqlite3.connect('flaskr.db')
	c = conn.cursor()
	c.execute('CREATE TABLE content(id INT(3) PRIMARY KEY, title VARCHAR(20) NOT NULL,\
					txt VARCHAR(2000)) NOT NULL')
	c.close()
	conn.commit()
	conn.close()
d


app = Flask(__name__)

@app.route('/', method=['GET'])
def login():
	return render_template('login.html')

@app.route('/', method=['POST'])
def login_info():
	username = request.form['username']
	password = request.form['password']
	error = None

	if username and password:
		conn = sqlite3.connect('flaskr.db')
		c = conn.cursor()
		rel_username = c.execute('SELECT username FROM user')[0][0]
		rel_password = c.execute('SELECT password FROM user')[0][0]
		if username == rel_username and password == rel_password:
			return redirect(url_for(index, '/blog'))
		else: error = 'bad username or password '
	
	return render_template('login.html', error=error)			


@app.route('/blog', method=['GET'])
def index():
	return render_template('index.html')

@app.route('/blog', method=['POST'])
def submit():
	title = request.form['title']
	text = request.form['text']
	
	if title and text:
		conn = sqlite3.connect('flaskr.db')
		c = conn.cursor()
		the_id =(c.execute('SELECT MAX(id) FROM content')][0][0])
		if the_id:
			the_id = int(the_id) + 1
		else:the_id = 1
		c.execute('INSERT INTO content VALUES(the_id, title, text)')
		c.close()
		conn.commit()
		conn.close()
	return render.template('index.html', error='submit successful!')

	else: 
		error = 'title or text can not be empty! '
		return render_template('index.html', error=error)




if __name__ == '__main__':
	app.run()

