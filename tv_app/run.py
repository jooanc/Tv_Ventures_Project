import os
import uuid, datetime

from flask import Flask, render_template, request, redirect

from tv_app.db_connector import connect_to_db, execute
from tv_app import random_name, random_start_date, random_phone_number, random_zipcode
from tv_app.mock_data import sample_subscribers, sample_packages, sample_installations, sample_technicians, \
    sample_subscriptions, sample_genres, sample_channel_packages, sample_channels

app = Flask(__name__)


# ---- INSTALLATIONS ----
@app.route('/populate-installations')
def populate_installs():
    db_object = connect_to_db()
    execute(db_object, "DROP TABLE if EXISTS installations;")
    create_install_table = "CREATE TABLE installations(installation_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, " \
                        "technician_id INT(11) NOT NULL," \
                        "installation_rating INT(11) NULL," \
                        "comments VARCHAR(1096) NULL," \
                        "installation_date DATE NOT NULL," \
                        "FOREIGN KEY fk_tech(technician_id) " \
                        "REFERENCES `technicians`(`technician_id`) " \
                        "ON UPDATE CASCADE " \
                        "ON DELETE CASCADE );" 
    execute(db_object, create_install_table)
    number_of_installs = 20
    for i in range(0, number_of_installs):
        technician_id = 1
        installation_rating = 5
        comments = "Good"
        installation_date = random_start_date.generate_date()
        query = 'INSERT INTO installations (technician_id, installation_rating, comments, installation_date) VALUES (%s, %s, %s, %s)'
        data = (technician_id, installation_rating, comments, installation_date)
        execute(db_object, query, data)
    return str(number_of_installs) + " installations have been populated to table installations"


@app.route('/installations')
def install_home():
    db_object = connect_to_db()
    installs = execute(db_object, "SELECT * from installations;")
    for install in installs:
        print(f"{install[0]}, {install[1]}, {install[2]}, {install[4]}, {install[3]}")
    return render_template('installs.html', installs = installs)

@app.route('/update-install/<install_id>', methods=['GET', 'POST'])
def update_install(install_id):
    db_object = connect_to_db()

    if request.method == 'GET':
        install_query = 'SELECT * from installations WHERE installation_id = %s' % (install_id)
        installs = execute(db_object, install_query).fetchone()

        technician_query = 'SELECT first_name, last_name, technician_id from technicians'
        technicians = execute(db_object, technician_query).fetchall()

        if installs == None:
            return "No installation has been found."

        return render_template('update_installs.html', installs = installs, technicians = technicians)

    elif request.method == 'POST':

        tech_id = request.form['technician_id']
        first_name = request.form['fname']
        last_name = request.form['lname']
        start_date = request.form['start_date']
        update_tech_query = "UPDATE technicians SET first_name = %s, last_name = %s, start_date = %s WHERE technician_id = %s"
        data = (first_name, last_name, start_date, tech_id)
        execute(db_object, update_tech_query, data)
        print("Technician updated")
        techs = execute(db_object, "SELECT * from technicians;")
        return render_template('techs.html', techs = techs)

    return render_template('update_installs.html', install=install_id)

@app.route('/add-install', methods=['GET', 'POST'])
def add_install():
    if request.method == 'GET':
        # TODO: query to get all tehcnicians
        return render_template('add_install_form.html', technicians=sample_technicians)
    elif request.method == 'POST':
        # TODO: send data to database and add new row
        return render_template('tmp_base.html')


# ---- TECHNICIANS ----
@app.route('/technicians')
def tech():
    db_object = connect_to_db()
    techs = execute(db_object, "SELECT * from technicians;")
    for tech in techs:
        print("Displaying Technician: " + f"{tech[2]}, {tech[1]}")
    return render_template('techs.html', techs = techs)


@app.route('/populate-tech')
def populate_tech():
    db_object = connect_to_db()
    execute(db_object, "DROP TABLE if EXISTS technicians;")
    create_tech_table = "CREATE TABLE technicians(technician_id INT PRIMARY KEY NOT NULL UNIQUE AUTO_INCREMENT, " \
                        "first_name VARCHAR(64) NOT NULL, last_name VARCHAR(64) NOT NULL, employer_id VARCHAR(36) " \
                        "NOT NULL, start_date DATE NOT NULL);"
    execute(db_object, create_tech_table)
    number_of_techs = 20
    for i in range(0, number_of_techs):
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
        start_date = request.form['start_date']
        query = 'INSERT INTO technicians (first_name, last_name, employer_id, start_date) VALUES (%s, %s, %s, %s)'
        data = (first_name, last_name, employer_id, start_date)
        execute(db_object, query, data)
        print("Technician " + first_name + " " + last_name + " has been onboarded on date " + start_date + ".")
        return render_template('techs.html')


@app.route('/update-tech/<int:technician_id>', methods=['GET', 'POST'])
def update_tech(technician_id):
    db_object = connect_to_db()
    if request.method == 'GET':
        query = 'SELECT * from technicians WHERE technician_id = %s' % (technician_id)
        out = execute(db_object, query).fetchone()

        if out == None:
            return "No tech has been found."

        return render_template('update_tech.html', tech = out)

    elif request.method == 'POST':
        print('The POST request')
        tech_id = request.form['technician_id']
        first_name = request.form['fname']
        last_name = request.form['lname']
        start_date = request.form['start_date']
        update_tech_query = "UPDATE technicians SET first_name = %s, last_name = %s, start_date = %s WHERE technician_id = %s"
        data = (first_name, last_name, start_date, tech_id)
        execute(db_object, update_tech_query, data)
        print("Technician updated")
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


@app.route('/add-channel', methods=['GET','POST'])
def add_channel():
    if request.method == 'GET':
        # TODO get all genres
        return render_template('add_channel_form.html', genres=sample_genres)
    elif request.method == 'POST':
        # TODO: send data to database and add new row
        return render_template('tmp_base.html')


@app.route('/update-channel/<int:channel_id>', methods=['GET', 'POST'])
def update_channel(channel_id):
    if request.method == 'GET':
        return render_template('update_channel.html', genres=sample_genres, channel_id=channel_id)

    elif request.method == 'POST':
        return render_template('tmp_base.html')


# ---- CHANNEL PACKAGES ----
@app.route('/channel-packages')
def channel_packages_home():
    return render_template('channel_packages.html', rows=sample_channel_packages)


@app.route('/add-channel-package', methods=['GET', 'POST'])
def add_channel_package():
    if request.method == 'GET':
        # TODO get all channels and packages
        return render_template('add_channel_package_form.html', channels=sample_channels, packages=sample_packages)
    elif request.method == 'POST':
        # TODO: send data to database and add new row
        return render_template('tmp_base.html')


@app.route('/update-channel-pkg/<int:channel_package_id>', methods=['GET', 'POST'])
def update_channel_package(channel_package_id):
    if request.method == 'GET':
        return render_template('update_channel_package.html', channels=sample_channels,
                               packages=sample_packages, channel_package_id=channel_package_id)

    elif request.method == 'POST':
        return render_template('tmp_base.html')


# ---- SUBSCRIBER ----
@app.route('/populate-subscribers')
def populate_subscribers():
    db_object = connect_to_db()
    execute(db_object, "DROP TABLE if EXISTS subscribers;")
    create_subscriber_table = "CREATE TABLE subscribers(subscriber_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, " \
                        "first_name VARCHAR(64) NOT NULL," \
                        "last_name VARCHAR(64) NOT NULL," \
                        "phone_number VARCHAR(16)," \
                        "postal_code VARCHAR(11)," \
                        "installation_id INT(11) NOT NULL," \
                        "active boolean NOT NULL DEFAULT 1," \
                        "age INT(11) NULL," \
                        "gender VARCHAR(32) NULL," \
                        "FOREIGN KEY fk_install(installation_id) " \
                        "REFERENCES `installations`(`installation_id`) " \
                        "ON UPDATE CASCADE " \
                        "ON DELETE CASCADE );" 
    execute(db_object, create_subscriber_table)
    number_of_subscribers = 20
    for i in range(0, number_of_subscribers):
        first_name = random_name.generate_first_name()
        last_name = random_name.generate_last_names()
        phone_number = random_phone_number.generate_phone_number()
        postal_code = random_zipcode.generate_zip_code()
        installation_id = 1
        active = 1
        age = 22
        gender = "male"
        query = 'INSERT INTO subscribers (first_name, last_name, phone_number, postal_code, installation_id, active, age, gender) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
        data = (first_name, last_name, phone_number, postal_code, installation_id, active, age, gender)
        execute(db_object, query, data)
    return str(number_of_subscribers) + " subscribers have been populated to table subscribers"

@app.route('/subscribers')
def subscriber_home():
    return render_template('subscribers.html', rows=sample_subscribers)


@app.route('/add-subscriber', methods=['GET', 'POST'])
def add_subscriber():
    if request.method == 'GET':
        # TODO get all installations
        return render_template('add_subscriber_form.html', installations=sample_installations)
    elif request.method == 'POST':
        # TODO: send data to database and add new row
        return render_template('tmp_base.html')


@app.route('/update-subscriber/<int:subscriber_id>', methods=['GET', 'POST'])
def update_subscriber(subscriber_id):
    if request.method == 'GET':
        return render_template('update_subscriber.html', subscriber_id=subscriber_id,
                               installations=sample_installations)

    elif request.method == 'POST':
        return render_template('tmp_base.html')


# ---- SUBSCRIPTIONS ----
@app.route('/subscriptions')
def subscriptions_home():
    return render_template('subscriptions.html', rows=sample_subscriptions)


@app.route('/add-subscription', methods=['GET', 'POST'])
def add_subscription():
    if request.method == 'GET':
        # TODO get all packages and subscribers
        return render_template('add_subscription_form.html', packages=sample_packages, subscribers=sample_subscribers)
    elif request.method == 'POST':
        # TODO: send data to database and add new row
        return render_template('tmp_base.html')


@app.route('/update-subscription/<int:subscription_id>', methods=['GET', 'POST'])
def update_subscription(subscription_id):
    if request.method == 'GET':
        return render_template('update_subscription.html', subscription_id=subscription_id,
                               packages=sample_packages, subscribers=sample_subscribers)
    elif request.method == 'POST':
        return render_template('tmp_base.html')


# ---- PACKAGES ----
@app.route('/packages')
def packages_home():
    return render_template('packages.html', rows=sample_packages)


@app.route('/add-package', methods=['GET', 'POST'])
def add_package():
    if request.method == 'GET':
        return render_template('add_package_form.html')
    elif request.method == 'POST':
        # TODO: send data to database and add new row
        return render_template('tmp_base.html')


@app.route('/update-package/<int:package_id>', methods=['GET', 'POST'])
def update_package(package_id):
    if request.method == 'GET':
        return render_template('update_package.html', package_id=package_id)
    elif request.method == 'POST':
        return render_template('tmp_base.html')


# ---- GENRES ----
@app.route('/populate-genres')
def populate_genre():
    db_object = connect_to_db()
    execute(db_object, "DROP TABLE if EXISTS channel_genres;")
    create_genre_table = "CREATE TABLE channel_genres(channel_genre_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, " \
                        "genre_name VARCHAR(32) NOT NULL UNIQUE," \
                        "kid_friendly boolean NOT NULL DEFAULT 0);"
    execute(db_object, create_genre_table)
    number_of_genres = 1
    for i in range(0, number_of_genres):
        genre_name = "horror1"
        kid_friendly = 0
        query = 'INSERT INTO channel_genres (genre_name, kid_friendly) VALUES (%s, %s)'
        data = (genre_name, kid_friendly)
        execute(db_object, query, data)
    return str(number_of_genres) + " genres have been populated to table channel_genres"

@app.route('/genres')
def genres_home():
    kid_friendly = request.args.get('kidfriendly')
    if kid_friendly is not None:
        genres = list()
        if kid_friendly.upper() == "TRUE":
            genres.append(sample_genres[0])
            genres.append(sample_genres[2])
        elif kid_friendly.upper() == "FALSE":
            genres.append(sample_genres[1])
        else:
            genres = sample_genres
    else:
        genres = sample_genres
    return render_template('genres.html', rows=genres)


@app.route('/add-genre', methods=['GET', 'POST'])
def add_genre():
    if request.method == 'GET':
        return render_template('add_genre_form.html')
    elif request.method == 'POST':
        # TODO: send data to database and add new row
        return render_template('tmp_base.html')


@app.route('/update-genre/<int:genre_id>', methods=['GET', 'POST'])
def update_genre(genre_id):
    if request.method == 'GET':
        return render_template('update_genre.html', genre_id=genre_id)
    elif request.method == 'POST':
        return render_template('tmp_base.html')


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
