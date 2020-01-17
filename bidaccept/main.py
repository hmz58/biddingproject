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
	
	
#endpoint for search
@app.route('/biddingsystem/searchjob', methods=['GET', 'POST'])
def search():
    # Check if user is loggedin
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        if request.method == "POST":
            searchStr = request.form['searchStr']
            app.logger.error('Processing default request'+searchStr)
            # search by author or book
            cursor.execute('SELECT jobname, jobdesc FROM jobs WHERE jobname like %s or jobdesc like %s', ('%'+searchStr+'%', '%'+searchStr+'%'))
            mysql.connection.commit()
            datafilled = cursor.fetchall()
            # all in the search box will return all the tuples
            if len(datafilled) == 0 and searchStr == 'all': 
                cursor.execute("SELECT jobname, jobdesc from jobs")
                mysql.connection.commit()
                datafilled = cursor.fetchall()
            return render_template('search.html', data=datafilled)
        return render_template('search.html')
    return redirect("http://localhost:5000/biddingsystem/login")

def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)

def readBLOB(job_id, photo):
    print("Reading BLOB data from table")

    try:
        cursor = mysql.connection.cursor()
        sql_fetch_blob_query = """SELECT data from jobs where id = %s"""

        cursor.execute(sql_fetch_blob_query, (job_id,))
        record = cursor.fetchall()
        for row in record:
            file = row[5]
            
            write_file(image, file)
    except mysql.connector.Error as error:
        print("Failed to read BLOB data from MySQL table {}".format(error))

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

app.run(host= '0.0.0.0')
