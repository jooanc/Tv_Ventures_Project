from flask import Flask,render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_USER'] = "cs340_kuritzb"
app.config['MYSQL_PASSWORD'] = "6188"
app.config['MYSQL_HOST'] = "classmysql.engr.oregonstate.edu"
app.config['MYSQL_DB'] = "cs340_kuritzb"
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute('DROP TABLE IF EXISTS diagnostic;')
    cur.execute('CREATE TABLE diagnostic(id INT PRIMARY KEY AUTO_INCREMENT, text VARCHAR(255) NOT NULL);')
    cur.execute('INSERT INTO diagnostic (text) VALUES ("MySQL is working");')
    cur.execute('SELECT * FROM diagnostic;')
    result = cur.fetchall()
    result_list = list()
    result_list.append(result[0])
    return render_template('task_result.html', rows=result_list)
    # return "MySQL Results:\n" + str(result)
