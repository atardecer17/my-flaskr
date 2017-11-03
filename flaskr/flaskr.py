import sqlite3
from flask import Flask, request, session, g,\
 redirect, url_for, abort, render_template, flash


def create_db():
	conn = sqlite3.connect('flaskr.db')
	c = conn.cursor()
	c.execute('CREATE TABLE content(id INT(3) PRIMARY KEY, title VARCHAR(20),text VARCHAR(2000))')
	c.execute('CREATE TABLE user(username VARCHAR(20), password VARCHAR(20))')
	c.execute('INSERT INTO user VALUES(\'admin\', \'password\')')
	c.close()
	conn.commit()
	conn.close()



app = Flask(__name__)

@app.route('/', methods=['GET'])
def login():
	return render_template('login.html')

@app.route('/', methods=['POST'])
def login_info():
	username = request.form['username']
	password = request.form['password']
	error = 'bad username or password'

	if username and password:
		conn = sqlite3.connect('flaskr.db')
		c = conn.cursor()
		rel_username = c.execute('SELECT username FROM user')[0][0]
		rel_password = c.execute('SELECT password FROM user')[0][0]
		if username == rel_username and password == rel_password:
			return redirect(url_for(index, '/blog'))
	
	return render_template('login.html', error=error)			


@app.route('/blog', methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/blog', methods=['POST'])
def submit():
	title = request.form['title']
	text = request.form['text']	
	error = 'title or text can not be empty! '
	if title and text:
		conn = sqlite3.connect('flaskr.db')
		c = conn.cursor()
		the_id =(c.execute('SELECT MAX(id) FROM content')[0][0])
		if the_id:
			the_id = int(the_id) + 1
		else:the_id = 1
		c.execute('INSERT INTO content VALUES(the_id, title, text)')
		c.close()
		conn.commit()
		conn.close()
		return render.template('index.html', error='submit successful!')

	return render_template('index.html', error=error)




if __name__ == '__main__':
	 app.run(debug=True) 
