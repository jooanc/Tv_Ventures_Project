from flask import Flask, render_template, request, redirect
from db_connector import connect_to_db, execute
import os
import uuid, datetime

import random_name, random_start_date, random_phone_number, random_zipcode

app = Flask(__name__)

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
def tech():
    db_object = connect_to_db()
    techs = execute(db_object, "SELECT * from technicians;")
    for tech in techs:
        print(f"{tech[2]}, {tech[1]}")
    return render_template('techs.html', techs = techs)

@app.route('/populate-tech')
def populate_tech():
    db_object = connect_to_db()
    execute(db_object, "DROP TABLE if EXISTS technicians;")
    create_tech_table = "CREATE TABLE technicians(technician_id INT PRIMARY KEY NOT NULL UNIQUE AUTO_INCREMENT, first_name VARCHAR(64) NOT NULL, last_name VARCHAR(64) NOT NULL, employer_id VARCHAR(32) NOT NULL, start_date DATE NOT NULL);"
    execute(db_object, create_tech_table)
    number_of_techs = 20
    for  i in range(0, number_of_techs):
        first_name = random_name.generate_first_name()
        last_name = random_name.generate_last_names()
        employer_id = uuid.uuid4().hex
        start_date = random_start_date.generate_date()
        query = 'INSERT INTO technicians (first_name, last_name, employer_id, start_date) VALUES (%s, %s, %s, %s)'
        data = (first_name, last_name, employer_id, start_date)
        execute(db_object, query, data)
    return str(number_of_techs) + " technicians have been populated to table technicians"

@app.route('/add-tech', methods=['POST', 'GET'])
def add_tech():
    db_object = connect_to_db()

    if request.method == 'GET':
        query = 'SELECT first_name, last_name from technicians'
        result = execute(db_object, query).fetchall()
        print("Displaying current technicians:\n")
        print(result)
        return render_template('add_tech_form.html')
    elif request.method == 'POST':
        first_name = request.form['fname']
        last_name = request.form['lname']
        employer_id = uuid.uuid4().hex
        start_date = datetime.date.today()
        query = 'INSERT INTO technicians (first_name, last_name, employer_id, start_date) VALUES (%s, %s, %s, %s)'
        data = (first_name, last_name, employer_id, start_date)
        execute(db_object, query, data)
        print("Technician " + first_name + " " + last_name + " has been onboarded.")
        # TODO: send data to database and add new row
        return render_template('add_tech_form.html')

@app.route('/update-tech/<int:technician_id>', methods=['GET', 'POST'])
def update_tech(technician_id):
    db_object = connect_to_db()
    if request.method == 'GET':
        query = 'SELECT technician_id, first_name, last_name from technicians WHERE technician_id = %s' % (technician_id)
        out = execute(db_object, query).fetchone()

        if out == None:
            return "No tech has been found."

        return render_template('update-tech.html', tech = out)

    elif request.method == 'POST':
        print('The POST request')
        tech_id = request.form['technician_id']
        first_name = request.form['fname']
        last_name = request.form['lname']
        update_tech_query = "UPDATE technicians SET first_name = %s, last_name = %s WHERE technician_id = %s"
        data = (first_name, last_name, tech_id)
        execute(db_object, update_tech_query, data)
        print("Technician onboarded")
        techs = execute(db_object, "SELECT * from technicians;")
        return render_template('techs.html', techs = techs)

@app.route('/delete-tech/<int:technician_id>')
def delete_tech(technician_id):
    db_object = connect_to_db()
    data = (technician_id,)
    query = "DELETE FROM technicians WHERE technician_id = %s"
    execute(db_object, query, data)
    print("Technician deleted")
    techs = execute(db_object, "SELECT * from technicians;")
    return render_template('techs.html', techs = techs)

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

@app.route('/populate-subscribers')
def populate_subscribers():
    number = random_phone_number.generate_phone_number()
    zipcode = random_zipcode.generate_zip_code()
    return "Under Construction"

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
