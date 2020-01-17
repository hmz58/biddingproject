from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'hosting@12345'
app.config['MYSQL_DB'] = 'biddingsystem'

# Intialize MySQL
mysql = MySQL(app)

	
# http://localhost:5001/biddingsystem - this will be the home page, only accessible for loggedin users
@app.route('/biddingsystem/postjob')
def postjob():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('postjob.html', userid=session['id'])
    # User is not loggedin redirect to login page
    return redirect("http://localhost:5000/biddingsystem/login")
	

# http://localhost:5000/pythinlogin/savejob - this will be the registration page, we need to use both GET and POST requests
@app.route('/biddingsystem/savejob', methods=['GET', 'POST'])
def savejob():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'jobname' in request.form and 'jobdescription' in request.form and 'file' in request.files and 'price' in request.form and 'userid' in request.form:
        # Create variables for easy access
        jobname = request.form['jobname']
        price = request.form['price']
        jobdescription = request.form['jobdescription']
        userid = request.form['userid']
        filedata = request.files['file']
		
		
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO jobs VALUES (NULL, %s, %s, %s, %s, data)', (jobname, jobdescription, userid, price))
        mysql.connection.commit()
        msg = 'You have successfully posted job!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('postjob.html', msg=msg)
	
app.run(host= '0.0.0.0')
