from datetime import date

from flask import Flask,render_template
from flask_mysqldb import MySQL

from app.mock_data import sample_technicians, sample_installations, sample_channels, sample_subscribers, \
    sample_channel_packages, sample_genres, sample_packages, sample_subscriptions

app = Flask(__name__)

app.config['MYSQL_USER'] = "cs340_kuritzb"
app.config['MYSQL_PASSWORD'] = "6188"
app.config['MYSQL_HOST'] = "classmysql.engr.oregonstate.edu"
app.config['MYSQL_DB'] = "cs340_kuritzb"
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# ---- INSTALLATIONS ----
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

@app.route('/update-install/<install_id>')
def update_install(install_id):

    return render_template('installs_update.html', install=install_id)

@app.route('/add-install', methods=['POST'])
def add_install():
    # TODO: send data to database and add new row
    return render_template('tmp_base.html')

@app.route('/add-install-form')
def add_install_form():
    # TODO: query to get all tehcnicians
    return render_template('add_install_form.html', technicians=sample_technicians)

# ---- TECHNICIANS ----
@app.route('/technicians')
def technician_home():
    return render_template('techs.html', rows=sample_technicians)

@app.route('/add-tech', methods=['POST'])
def add_tech():
    # TODO: send data to database and add new row
    return render_template('tmp_base.html')

@app.route('/add-tech-form')
def add_tech_form():
    return render_template('add_tech_form.html')

# ---- CHANNELS ----
@app.route('/channels')
def channels_home():
    return render_template('channels.html', rows=sample_channels)

@app.route('/add-channel', methods=['POST'])
def add_channel():
    # TODO: send data to database and add new row
    return render_template('tmp_base.html')

@app.route('/add-channel-form')
def add_channel_form():
    # TODO get all genres
    return render_template('add_channel_form.html', genres=sample_genres)

# ---- CHANNEL PACKAGES ----
@app.route('/channel-packages')
def channel_packages_home():
    return render_template('channel_packages.html', rows=sample_channel_packages)

@app.route('/add-channel-package', methods=['POST'])
def add_channel_package():
    # TODO: send data to database and add new row
    return render_template('tmp_base.html')

@app.route('/add-channel-package-form')
def add_channel_package_form():
    # TODO get all channels and packages
    return render_template('add_channel_package_form.html', channels=sample_channels, packages=sample_packages)

# ---- SUBSCRIBER ----
@app.route('/subscribers')
def subscriber_home():
    return render_template('subscribers.html', rows=sample_subscribers)

@app.route('/add-subscriber', methods=['POST'])
def add_subscriber():
    # TODO: send data to database and add new row
    return render_template('tmp_base.html')

@app.route('/add-subscriber-form')
def add_subscriber_form():
    # TODO get all installations
    return render_template('add_subscriber_form.html', installations=sample_installations)

# ---- SUBSCRIPTIONS ----
@app.route('/subscriptions')
def subscriptions_home():
    return render_template('subscriptions.html', rows=sample_subscriptions)

@app.route('/add-subscription', methods=['POST'])
def add_subscription():
    # TODO: send data to database and add new row
    return render_template('tmp_base.html')

@app.route('/add-subscription-form')
def add_subscription_form():
    # TODO get all packages and subscribers
    return render_template('add_subscription_form.html', packages=sample_packages, subscribers=sample_subscribers)

# ---- PACKAGES ----
@app.route('/packages')
def packages_home():
    return render_template('packages.html', rows=sample_packages)

@app.route('/add-package', methods=['POST'])
def add_package():
    # TODO: send data to database and add new row
    return render_template('tmp_base.html')

@app.route('/add-package-form')
def add_package_form():
    return render_template('add_package_form.html')

# ---- GENRES ----
@app.route('/genres')
def genres_home():
    return render_template('genres.html', rows=sample_genres)

@app.route('/add-genre', methods=['POST'])
def add_genre():
    # TODO: send data to database and add new row
    return render_template('tmp_base.html')

@app.route('/add-genre-form')
def add_genre_form():
    return render_template('add_genre_form.html')

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
