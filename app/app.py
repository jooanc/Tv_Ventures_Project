from datetime import date

from flask import Flask,render_template
from flask_mysqldb import MySQL

from app.mock_data import sample_technicians, sample_installations, sample_channels, sample_subscribers, \
    sample_channel_packages, sample_genres, sample_packages, sample_susbcriptions

app = Flask(__name__)

app.config['MYSQL_USER'] = "cs340_kuritzb"
app.config['MYSQL_PASSWORD'] = "6188"
app.config['MYSQL_HOST'] = "classmysql.engr.oregonstate.edu"
app.config['MYSQL_DB'] = "cs340_kuritzb"
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/installations')
def install_home():
    # Make call to db, get result list.

    # ----- Example code just for future reference -----
    # cur = mysql.connection.cursor()
    # cur.execute('SELECT * FROM installations;')
    # result = cur.fetchall()
    # result_list = list()
    # result_list.append(result[0])
    # ---------------------------------------------------

    return render_template('installs.html', rows=sample_installations)

@app.route('/technicians')
def technician_home():
    return render_template('techs.html', rows=sample_technicians)

@app.route('/channels')
def channels_home():
    return render_template('channels.html', rows=sample_channels)

@app.route('/channel-packages')
def channel_packages_home():
    return render_template('channel_packages.html', rows=sample_channel_packages)

@app.route('/subscribers')
def subscriber_home():
    return render_template('subscribers.html', rows=sample_subscribers)

@app.route('/subscriptions')
def subscriptions_home():
    return render_template('subscriptions.html', rows=sample_subscriptions)

@app.route('/packages')
def packages_home():
    return render_template('packages.html', rows=sample_packages)

@app.route('/genres')
def genres_home():
    return render_template('genres.html', rows=sample_genres)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
