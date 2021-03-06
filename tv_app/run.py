import os
import sys
import uuid

from datetime import datetime

from flask import Flask, render_template, request

from tv_app.db_connector import connect_to_db, execute
from tv_app import random_name, random_start_date, random_phone_number, random_zipcode
from tv_app.mock_data import sample_subscribers, sample_packages, sample_installations

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
        query = 'INSERT INTO installations (technician_id, installation_rating, comments, installation_date) ' \
                'VALUES (\"%s\", \"%s\", \"%s\", \"%s\");'
        data = (technician_id, installation_rating, comments, installation_date)
        execute(db_object, query, data)
    return str(number_of_installs) + " installations have been populated to table installations"


@app.route('/installations')
def install_home():
    db_object = connect_to_db()
    try:
        installs = execute(db_object,   "SELECT installation_id, CONCAT(first_name, ' ' ,last_name) AS full_name, installation_rating, installation_date, comments " \
                                        "FROM installations JOIN technicians ON installations.technician_id = technicians.technician_id;")

        for install in installs:
            print(f"{install[0]}, {install[1]}, {install[2]}, {install[4]}, {install[3]}")

        final_list = list()
        for i in installs:
            if i[2] == 0:
                rating = "N/A"
            else:
                rating = i[2]
            final_list.append((i[0], i[1], rating, i[3], i[4]))

        return render_template('installs.html', installs=final_list)
    except Exception as e:
        return render_template('error.html', e=e)


@app.route('/update-install/<install_id>', methods=['GET', 'POST'])
def update_install(install_id):
    db_object = connect_to_db()
    if request.method == 'GET':
        try:
            install_query = 'SELECT * from installations WHERE installation_id = "%s"' % (install_id)
            install_out = execute(db_object, install_query).fetchone()

            technician_query = 'SELECT * from technicians'
            tech_out = execute(db_object, technician_query).fetchall()

            if install_out == None:
                return "No installation has been found."

            return render_template('update_installs.html', install = install_out, techs = tech_out)
        except Exception as e:
            return render_template('error.html', e=e)

    elif request.method == 'POST':
        try:
            technician_id = request.form['technician_id']
            installation_rating = request.form['installation_rating']
            comments = request.form['comments']
            installation_date = request.form['installation_date']
            update_install_query = "UPDATE installations SET technician_id = \"%s\", installation_rating = \"%s\", " \
                                   "comments = \"%s\", installation_date = \"%s\" WHERE installation_id = \"%s\""
            data = (technician_id, installation_rating, comments, installation_date)
            execute(db_object, update_install_query, data)
            print("Installation updated")
            install_out = execute(db_object, "SELECT * from installations;")
            return render_template('installs.html', installs = install_out)
        except Exception as e:
            return render_template('error.html', e=e)


@app.route('/delete-install/<int:installation_id>')
def delete_install(installation_id):
    db_object = connect_to_db()
    data = (installation_id,)
    query = "DELETE FROM installations WHERE installation_id = \"%s\";"
    result = execute(db_object, query, data)
    print("Installation deleted")
    print(str(result.rowcount) + "row deleted")
    installs = execute(db_object,   "SELECT installation_id, CONCAT(first_name, ' ' ,last_name) AS full_name, installation_rating, installation_date, comments " \
                                    "FROM installations JOIN technicians ON installations.technician_id = technicians.technician_id")
    return render_template('installs.html', installs = installs)


@app.route('/add-install', methods=['GET', 'POST'])
def add_install():
    db_object = connect_to_db()
    if request.method == 'GET':
        try:
            techs = execute(db_object, 'SELECT * FROM technicians;')
            result = list(techs.fetchall())
            return render_template('add_install_form.html', techs=result)
        except Exception as e:
            return render_template('error.html', e=e)
    elif request.method == 'POST':
        try:
            tech = request.form.get('install-tech')
            rating = request.form.get('rating')
            install_date = request.form.get('install-date')
            install_comment = request.form.get('install-comment')
            if len(install_date) < 1 or install_date is None:
                msg = "Installation date is required."
                raise Exception(msg)

            # Input checking.
            if len(rating) > 0 and (int(rating) > 5 or int(rating) <= 0):
                msg = "Installation rating must be between 1 and 5."
                raise Exception(msg)

            if len(rating) > 0:
                rating = int(rating)
                query = "INSERT INTO `installations` (`technician_id`, `installation_rating`, `comments`, `installation_date`) " \
                        "VALUES (%d, %d, \"%s\", \"%s\");" % (int(tech), rating, install_comment, install_date)
            else:
                rating = None
                query = "INSERT INTO `installations` (`technician_id`, `installation_rating`, `comments`, `installation_date`) " \
                        "VALUES (%d, \"%s\", \"%s\", \"%s\");" % (int(tech), rating, install_comment, install_date)

            execute(db_object, query)
            return render_template('tmp_base.html', page_name="Installations", redirect="installations")
        except Exception as e:
            return render_template('error.html', e=e)


# ---- TECHNICIANS ----
@app.route('/technicians')
def tech_home():
    db_object = connect_to_db()
    try:
        techs = execute(db_object, "SELECT * FROM technicians;")
        result = list(techs.fetchall())
        print(result)
        for tech in techs:
            print("Displaying Technician: " + f"{tech[2]}, {tech[1]}")
        return render_template('techs.html', techs=result)
    except Exception as e:
        return render_template('error.html', e=e)


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
        query = 'INSERT INTO technicians (first_name, last_name, employer_id, start_date) ' \
                'VALUES (\"%s\", \"%s\", \"%s\", \"%s\");'
        data = (first_name, last_name, employer_id, start_date)
        execute(db_object, query, data)
    return str(number_of_techs) + " technicians have been populated to table technicians"


@app.route('/add-tech', methods=['POST', 'GET'])
def add_tech():
    db_object = connect_to_db()
    if request.method == 'GET':
        try:
            query = 'SELECT first_name, last_name from technicians;'
            result = list(execute(db_object, query).fetchall())
            print("Displaying current technicians:\n")
            print(result)
            return render_template('add_tech_form.html')
        except Exception as e:
            return render_template('error.html', e=e)
    elif request.method == 'POST':
        try:
            first_name = request.form['fname']
            last_name = request.form['lname']
            employer_id = uuid.uuid4().hex
            start_date = request.form['start_date']

            if first_name is None or len(first_name) < 1:
                msg = "First name is required."
                raise Exception(msg)
            if last_name is None or len(last_name) < 1:
                msg = "Last name is required."
                raise Exception(msg)

            query = 'INSERT INTO `technicians` (`first_name`, `last_name`, `employer_id`, `start_date`) ' \
                    'VALUES (\"%s\", \"%s\", \"%s\", \"%s\");'
            data = (first_name, last_name, employer_id, start_date)
            execute(db_object, query, data)
            print("Technician " + first_name + " " + last_name + " has been onboarded on date " + start_date + ".")
            return render_template('tmp_base.html', page_name="Technicians", redirect="technicians")
        except Exception as e:
            return render_template('error.html', e=e)


@app.route('/update-tech/<int:technician_id>', methods=['GET', 'POST'])
def update_tech(technician_id):
    db_object = connect_to_db()
    if request.method == 'GET':
        query = 'SELECT * from technicians WHERE technician_id = \"%s\"' % (technician_id)
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
        update_tech_query = "UPDATE technicians SET first_name = \"%s\", last_name = \"%s\", start_date = \"%s\" WHERE technician_id = \"%s\";"
        data = (first_name, last_name, start_date, tech_id)
        execute(db_object, update_tech_query, data)
        print("Technician updated")
        techs = execute(db_object, "SELECT * from technicians;")
        return render_template('techs.html', techs = techs)


@app.route('/delete-tech/<int:technician_id>')
def delete_tech(technician_id):
    db_object = connect_to_db()
    data = (technician_id,)
    query = "DELETE FROM technicians WHERE technician_id = \"%s\";"
    result = execute(db_object, query, data)
    result.close()
    print(str(result.rowcount) + " row deleted")

    print("Technician deleted")
    techs = execute(db_object, "SELECT * from technicians;")
    return render_template('techs.html', techs = techs)


# ---- CHANNELS ----
@app.route('/channels')
def channels_home():
    db_object = connect_to_db()
    try:
        query = 'SELECT channel_id, channel_name, channel_number, genre_name, kid_friendly FROM channels ' \
                'JOIN channel_genres ON channels.channel_genre_id=channel_genres.channel_genre_id;'
        channels = execute(db_object, query)
        result = list(channels.fetchall())

        # Change int booleans to strings.
        final_list = list()
        for r in result:
            if r[4] == 0:
                kf = "False"
            else:
                kf = "True"
            final_list.append((r[0], r[1], r[2], r[3], kf))

        return render_template('channels.html', rows=final_list)
    except Exception as e:
        return render_template('error.html', e=e)


@app.route('/add-channel', methods=['GET', 'POST'])
def add_channel():
    db_object = connect_to_db()
    if request.method == 'GET':
        try:
            genres = execute(db_object, 'SELECT * FROM channel_genres;')
            result = list(genres.fetchall())
            return render_template('add_channel_form.html', genres=result)
        except Exception as e:
            return render_template('error.html', e=e)

    elif request.method == 'POST':
        try:
            name = request.form.get('channel-name')
            number = request.form.get('channel-number')
            genre = request.form.get('channel-genre')

            # Input checking.
            if name is None:
                msg = "Channel name is required."
                raise Exception(msg)
            if number is not None:
                number = int(number)
            else:
                msg = "Channel number is required."
                raise Exception(msg)
            if genre is not None:
                genre = int(genre)
            else:
                msg = "Channel genre is required."
                raise Exception(msg)
            if number <= 0 or number >= 1000:
                msg = "Channel number must be between 0 and 1000."
                raise Exception(msg)

            # Execute insert statement.
            query = "INSERT INTO `channels` (`channel_name`, `channel_number`, `channel_genre_id`) " \
                    "VALUES (\"%s\", %d, %d);" % (name, number, genre)
            execute(db_object, query)
            return render_template('tmp_base.html', page_name="Channels", redirect="channels")
        except Exception as e:
            return render_template('error.html', e=e)


@app.route('/update-channel/<int:channel_id>', methods=['GET', 'POST'])
def update_channel(channel_id):
    db_object = connect_to_db()
    if request.method == 'GET':
        genres = execute(db_object, 'SELECT * FROM channel_genres;')
        result = list(genres.fetchall())
        return render_template('update_channel.html', genres=result, channel_id=channel_id)

    elif request.method == 'POST':
        return render_template('tmp_base.html')


# ---- CHANNEL PACKAGES ----
@app.route('/channel-packages')
def channel_packages_home():
    db_object = connect_to_db()
    try:
        ch_pkgs = execute(db_object, 'SELECT channel_package_id, channel_name, package_name FROM channel_packages '
                                     'JOIN channels ON channel_packages.channel_id=channels.channel_id '
                                     'JOIN packages ON channel_packages.package_id=packages.package_id;')
        result = list(ch_pkgs.fetchall())
        return render_template('channel_packages.html', rows=result)
    except Exception as e:
        return render_template('error.html', e=e)


@app.route('/add-channel-package', methods=['GET', 'POST'])
def add_channel_package():
    db_object = connect_to_db()
    if request.method == 'GET':
        try:
            channels = execute(db_object, 'SELECT * FROM channels;')
            result_channels = list(channels.fetchall())
            packages = execute(db_object, 'SELECT * FROM packages;')
            result_packages = list(packages.fetchall())
            return render_template('add_channel_package_form.html', channels=result_channels, packages=result_packages)
        except Exception as e:
            return render_template('error.html', e=e)
    elif request.method == 'POST':
        try:
            channel_id = request.form.get('channel')
            package_id = request.form.get('package')

            # Input checking.
            if channel_id is None:
                msg = "Channel is required."
                raise Exception(msg)
            if package_id is None:
                msg = "Package is required."
                raise Exception(msg)

            # Execute query.
            query = "INSERT INTO `channel_packages` (`package_id`, `channel_id`) VALUES (%d, %d);" \
                    % (int(package_id), int(channel_id))
            execute(db_object, query)
            return render_template('tmp_base.html', page_name="Channel Packages", redirect="channel-packages")
        except Exception as e:
            return render_template('error.html', e=e)


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
        query = 'INSERT INTO subscribers (first_name, last_name, phone_number, postal_code, installation_id, active, age, gender) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")'
        data = (first_name, last_name, phone_number, postal_code, installation_id, active, age, gender)
        execute(db_object, query, data)
    return str(number_of_subscribers) + " subscribers have been populated to table subscribers"


@app.route('/subscribers', methods=['GET', 'POST'])
def subscriber_home():
    db_object = connect_to_db()
    if request.method == 'GET':
        try:
            query = 'SELECT * FROM subscribers;'
            subrs = execute(db_object, query)
            result = list(subrs.fetchall())
            final_list = list()
            for r in result:
                if r[7] == 0:
                    age = "N/A"
                else:
                    age = r[7]
                if len(r[8]) == 0:
                    gender = "N/A"
                else:
                    gender = r[8]
                final_list.append((r[0], r[1], r[2], r[3], r[4], r[5], age, gender))

            return render_template('subscribers.html', rows=final_list)
        except Exception as e:
            return render_template('error.html', e=e)

    # Means user submitted a search.
    if request.method == 'POST':
        try:
            # Iterate through the form and pull out the submitted search values into a dictionary.
            fname = request.form.get('fname', None)
            lname = request.form.get('lname', None)
            zipcode = request.form.get('zipcode', None)

            params = {}
            if fname is not None and fname != "":
                params.update({"first_name": fname})
            if lname is not None and lname != "":
                params.update({"last_name": lname})
            if zipcode is not None and zipcode != "":
                params.update({"postal_code": zipcode})

            # Handle case where someone submits a completely empty search.
            if len(params) == 0:
                query = 'SELECT * FROM subscribers;'
                subrs = execute(db_object, query)
                result = list(subrs.fetchall())
                return render_template('subscribers.html', rows=result)

            # Form search string
            search_string = "WHERE"
            for k, v in params.items():
                # Determine if we're adding the first search param, or if we're adding the second and beyond as we need
                # to use AND with these. Determine by seeing if the string is still just WHERE, meaning nothing has been
                # appended yet.
                if search_string[-5:] == "WHERE":
                    search_string = f'{search_string} {k}="{v}"'
                else:
                    search_string = f'{search_string} AND {k}="{v}"'
            # Append the final ;
            search_string = f"SELECT * FROM subscribers {search_string};"
            print(search_string, file=sys.stderr)

            subrs = execute(db_object, search_string)
            result = list(subrs.fetchall())
            final_list = list()
            for r in result:
                if r[7] == 0:
                    age = "N/A"
                else:
                    age = r[7]
                if len(r[8]) == 0:
                    gender = "N/A"
                else:
                    gender = r[8]
                final_list.append((r[0], r[1], r[2], r[3], r[4], r[5], age, gender))
            return render_template('subscribers.html', rows=result)
        except Exception as e:
            return render_template('error.html', e=e)


@app.route('/add-subscriber', methods=['GET', 'POST'])
def add_subscriber():
    db_object = connect_to_db()
    if request.method == 'GET':
        try:
            installs = execute(db_object, 'SELECT * FROM installations;')
            result = list(installs.fetchall())
            return render_template('add_subscriber_form.html', installations=result)
        except Exception as e:
            return render_template('error.html', e=e)
    elif request.method == 'POST':
        try:
            phone = request.form.get('phone-number')
            first_name = request.form.get('fname')
            last_name = request.form.get('lname')
            age = request.form.get('age')
            gender = request.form.get('gender')
            install = request.form.get('install')
            zip = request.form.get('zip')

            # Input checking.
            if phone is None or len(phone) < 1:
                msg = "Phone number is required."
                raise Exception(msg)
            if first_name is None or len(first_name) < 1:
                msg = "First name is required."
                raise Exception(msg)
            if last_name is None or len(last_name) < 1:
                msg = "Last name is required."
                raise Exception(msg)
            if install is None or len(install) < 1:
                msg = "Installation is required."
                raise Exception(msg)
            if zip is None or len(zip) < 1:
                msg = "Zip code is required."
                raise Exception(msg)

            print("AGE", age)
            if len(age) > 0:
                age = int(age)
            else:
                age = 0

            print("updated age", age)

            # Execute insert.
            query = "INSERT INTO `subscribers` " \
                    "(`first_name`, `last_name`, `phone_number`, `postal_code`, " \
                    "`installation_id`, `age`, `gender`) " \
                    "VALUES (\"%s\", \"%s\", \"%s\", %d, %d, %d, \"%s\");" % (first_name, last_name, phone, int(zip), int(install),
                                                              age, gender)
            execute(db_object, query)
            return render_template('tmp_base.html', page_name="Subscribers", redirect="subscribers")
        except Exception as e:
            return render_template('error.html', e=e)


@app.route('/update-subscriber/<int:subscriber_id>', methods=['GET', 'POST'])
def update_subscriber(subscriber_id):
    db_object = connect_to_db()
    if request.method == 'GET':
        return render_template('update_subscriber.html', subscriber_id=subscriber_id,
                               installations=sample_installations)

    elif request.method == 'POST':
        return render_template('tmp_base.html')


# ---- SUBSCRIPTIONS ----
@app.route('/subscriptions')
def subscriptions_home():
    db_object = connect_to_db()
    try:
        subs = execute(db_object, 'SELECT * FROM subscriptions;')
        result = list(subs.fetchall())
        final_list = list()
        for r in result:
            if r[7] == 0:
                rating = "N/A"
            else:
                rating = r[7]
            if r[6] == 0:
                prem = "False"
            else:
                prem = "True"
            final_list.append((r[0], r[1], r[2], r[3], r[4], r[5], prem, rating))
        return render_template('subscriptions.html', rows=final_list)
    except Exception as e:
        return render_template('error.html', e=e)


@app.route('/add-subscription', methods=['GET', 'POST'])
def add_subscription():
    db_object = connect_to_db()
    if request.method == 'GET':
        try:
            subrs = execute(db_object, 'SELECT * FROM subscribers;')
            result_subrs = list(subrs.fetchall())
            pkgs = execute(db_object, 'SELECT * FROM packages;')
            result_packages = list(pkgs.fetchall())
            return render_template('add_subscription_form.html', pkgs=result_packages, subrs=result_subrs)
        except Exception as e:
            return render_template('error.html', e=e)
    elif request.method == 'POST':
        try:
            package = request.form.get('package')
            subscriber = request.form.get('subscriber')
            start_date = request.form.get('start-date')
            renewal_date = request.form.get('renewal-date')
            status = request.form.get('status')
            rating = request.form.get('rating')
            premium = request.form.get('premium')

            # Input checking.
            if package is None:
                msg = "Package is required."
                raise Exception(msg)
            if len(rating) < 0 and (int(rating) > 5 or int(rating) <=0):
                msg = "Rating must between 0 and 5."
                raise Exception(msg)
            elif len(rating) < 0:
                rating = int(rating)
            if len(status) < 1:
                status = "New"

            # renewal = datetime.strptime(renewal_date[:-6], "%Y/%m/%d")
            # start = datetime.strptime(start_date[:-6], "%Y/%m/%d")
            # present = datetime.now()
            # if renewal.date() > start.date():
            #     msg = "Last renewal cannot occur before the start date."
            #     raise Exception(msg)
            # if renewal.date() > present.date():
            #     msg = "last renewal cannot be after today's date."
            #     raise Exception(msg)

            if premium is not None and premium == "true":
                premium = 1
            else:
                premium = 0

            if len(rating) > 0:
                rating = int(rating)
                query = "INSERT INTO `subscriptions` " \
                        "(`package_id`, `subscriber_id`, `time_start`, `last_renewed`, " \
                        "`subscription_status`, `premium`, `subscriber_rating`) " \
                        "VALUES (%d, %d, \"%s\", \"%s\", \"%s\", %d, %d);" % (int(package), int(subscriber), start_date,
                                                                          renewal_date, status, int(premium), rating)
            else:
                rating = None
                query = "INSERT INTO `subscriptions` " \
                        "(`package_id`, `subscriber_id`, `time_start`, `last_renewed`, " \
                        "`subscription_status`, `premium`, `subscriber_rating`) " \
                        "VALUES (%d, %d, \"%s\", \"%s\", \"%s\", %d, \"%s\");" % (int(package), int(subscriber), start_date,
                                                                              renewal_date, status, int(premium),
                                                                              rating)
            execute(db_object, query)
            return render_template('tmp_base.html', page_name="Subscriptions", redirect="subscriptions")
        except Exception as e:
            return render_template('error.html', e=e)


@app.route('/update-subscription/<int:subscription_id>', methods=['GET', 'POST'])
def update_subscription(subscription_id):
    db_object = connect_to_db()
    if request.method == 'GET':
        return render_template('update_subscription.html', subscription_id=subscription_id,
                               packages=sample_packages, subscribers=sample_subscribers)
    elif request.method == 'POST':
        return render_template('tmp_base.html')


# ---- PACKAGES ----
@app.route('/packages')
def packages_home():
    db_object = connect_to_db()
    try:
        pkgs = execute(db_object, 'SELECT * FROM packages;')
        result = list(pkgs.fetchall())
        return render_template('packages.html', rows=result)
    except Exception as e:
        return render_template('error.html', e=e)


@app.route('/add-package', methods=['GET', 'POST'])
def add_package():
    db_object = connect_to_db()
    if request.method == 'GET':
        try:
            return render_template('add_package_form.html')
        except Exception as e:
            return render_template('error.html', e=e)
    elif request.method == 'POST':
        try:
            package_name = request.form.get('package-name')
            standard_price = request.form.get('standard-price')
            premium_price = request.form.get('premium-price')

            # Input checking.
            if package_name is None or len(package_name) < 1:
                msg = "Package name is required."
                raise Exception(msg)
            if standard_price is None or len(standard_price) < 1:
                msg = "Standard price is required."
                raise Exception(msg)
            if premium_price is None or len(premium_price) < 1:
                msg = "Premium price is required."
                raise Exception(msg)

            query = "INSERT INTO `packages` (`package_name`, `standard_price`, `premium_price`) " \
                    "VALUES (\"%s\", %d, %d);" % (package_name, float(standard_price), float(premium_price))
            execute(db_object, query)
            return render_template('tmp_base.html', page_name="Packages", redirect="packages")
        except Exception as e:
            return render_template('error.html', e=e)


@app.route('/update-package/<int:package_id>', methods=['GET', 'POST'])
def update_package(package_id):
    db_object = connect_to_db()
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
        query = 'INSERT INTO channel_genres (genre_name, kid_friendly) VALUES (\"%s\", \"%s\")'
        data = (genre_name, kid_friendly)
        execute(db_object, query, data)
    return str(number_of_genres) + " genres have been populated to table channel_genres"


@app.route('/genres')
def genres_home():
    db_object = connect_to_db()
    try:
        genres = execute(db_object, 'SELECT * FROM channel_genres;')
        result = list(genres.fetchall())
        final_list = list()
        for r in result:
            if r[2] == 0:
                kf = "False"
            else:
                kf = "True"
            final_list.append((r[0], r[1], kf))
        return render_template('genres.html', rows=final_list)
    except Exception as e:
        return render_template('error.html', e=e)


@app.route('/add-genre', methods=['GET', 'POST'])
def add_genre():
    db_object = connect_to_db()
    if request.method == 'GET':
        try:
            return render_template('add_genre_form.html')
        except Exception as e:
            return render_template('error.html', e=e)
    elif request.method == 'POST':
        try:
            genre_name = request.form.get('genre-name')
            kid_friendly = request.form.get('kid-friendly')

            # Input checking.
            if genre_name is None or len(genre_name) < 1:
                msg = "Genre name is required."
                raise Exception(msg)

            if kid_friendly is not None and kid_friendly == "true":
                kid_friendly = 1
            else:
                kid_friendly = 0

            # Execute insert.
            query = "INSERT INTO `channel_genres` (`genre_name`, `kid_friendly`) " \
                    "VALUES (\"%s\", %d);" % (genre_name, int(kid_friendly))
            execute(db_object, query)
            return render_template('tmp_base.html', page_name="Genres", redirect="genres")
        except Exception as e:
            return render_template('error.html', e=e)


@app.route('/')
def home():
    db_object = connect_to_db()
    return render_template('home.html')


# ----- Testing purposes only below. ------
@app.route('/add-all-tables')
def add_all():
    db_object = connect_to_db()
    techs = "SET FOREIGN_KEY_CHECKS=0; DROP TABLE if EXISTS `technicians`; CREATE TABLE `technicians`(`technician_id` INT PRIMARY KEY " \
            "NOT NULL UNIQUE AUTO_INCREMENT, `first_name` VARCHAR(64) NOT NULL, `last_name` VARCHAR(64) NOT NULL, " \
            "`employer_id` VARCHAR(36) NOT NULL, `start_date` DATE NOT NULL);"
    curr = execute(db_object, techs)
    curr.close()

    db_object = connect_to_db()
    installs = "SET FOREIGN_KEY_CHECKS=0; DROP TABLE if EXISTS `installations`; CREATE TABLE `installations`(`installation_id` INT PRIMARY KEY " \
               "NOT NULL UNIQUE AUTO_INCREMENT, `technician_id` INT(11) NOT NULL, `installation_rating` INT(11) NULL, " \
               "`comments` VARCHAR(1096) NULL, `installation_date` DATE NOT NULL, FOREIGN KEY (`technician_id`) " \
               "REFERENCES `technicians`(`technician_id`) ON DELETE CASCADE);"
    curr = execute(db_object, installs)
    curr.close()

    db_object = connect_to_db()
    subrs = "SET FOREIGN_KEY_CHECKS=0; DROP TABLE if EXISTS `subscribers`; CREATE TABLE `subscribers`(`subscriber_id` INT PRIMARY KEY NOT NULL " \
            "UNIQUE AUTO_INCREMENT, `first_name` VARCHAR(64) NOT NULL, `last_name` VARCHAR(64) NOT NULL, `phone_number` " \
            "VARCHAR(16) NOT NULL, `postal_code` INT(11) NOT NULL, `installation_id` INT(11) NOT NULL, `active` boolean " \
            "NOT NULL DEFAULT 1,`age` INT(11) NULL, `gender` VARCHAR(32) NULL, FOREIGN KEY (`installation_id`) " \
            "REFERENCES `installations`(`installation_id`) ON UPDATE CASCADE ON DELETE CASCADE);"
    curr = execute(db_object, subrs)
    curr.close()

    db_object = connect_to_db()
    pkgs = "SET FOREIGN_KEY_CHECKS=0; DROP TABLE if EXISTS `packages`; CREATE TABLE `packages`(`package_id` INT PRIMARY KEY NOT NULL UNIQUE " \
           "AUTO_INCREMENT, `package_name` VARCHAR(64) NOT NULL UNIQUE, `standard_price` FLOAT(5,2) NOT NULL, " \
           "`premium_price` FLOAT(5,2) NOT NULL);"
    curr = execute(db_object, pkgs)
    curr.close()

    db_object = connect_to_db()
    subns = "SET FOREIGN_KEY_CHECKS=0; DROP TABLE if EXISTS `subscriptions`; CREATE TABLE `subscriptions`(`subscription_id` INT PRIMARY KEY " \
            "NOT NULL UNIQUE AUTO_INCREMENT, `package_id` INT(11) NOT NULL, `subscriber_id` INT(11) NOT NULL, " \
            "`time_start` DATETIME NOT NULL, `last_renewed` DATETIME NOT NULL, `subscription_status` VARCHAR(32) " \
            "NOT NULL DEFAULT \"New\",`premium` boolean NOT NULL DEFAULT 0,`subscriber_rating` INT(11) NULL, " \
            "FOREIGN KEY (`package_id`) REFERENCES `packages`(`package_id`) ON UPDATE CASCADE ON DELETE CASCADE, " \
            "FOREIGN KEY (`subscriber_id`) REFERENCES `subscribers`(`subscriber_id`) " \
            "ON UPDATE CASCADE ON DELETE CASCADE);"
    curr = execute(db_object, subns)
    curr.close()

    db_object = connect_to_db()
    genres = "SET FOREIGN_KEY_CHECKS=0; DROP TABLE if EXISTS `channel_genres`; CREATE TABLE `channel_genres`(`channel_genre_id` INT PRIMARY KEY " \
             "NOT NULL UNIQUE AUTO_INCREMENT, `genre_name` VARCHAR(32) NOT NULL UNIQUE, `kid_friendly` " \
             "boolean NOT NULL DEFAULT 0);"
    curr = execute(db_object, genres)
    curr.close()

    db_object = connect_to_db()
    channels = "SET FOREIGN_KEY_CHECKS=0; DROP TABLE if EXISTS `channels`; CREATE TABLE `channels`(`channel_id` INT PRIMARY KEY NOT NULL UNIQUE " \
               "AUTO_INCREMENT, `channel_name` VARCHAR(64) NOT NULL, `channel_number` INT(11) NULL UNIQUE, " \
               "`channel_genre_id` INT(11) NULL, FOREIGN KEY (`channel_genre_id`) REFERENCES " \
               "`channel_genres`(`channel_genre_id`) ON UPDATE CASCADE ON DELETE CASCADE);"
    curr = execute(db_object, channels)
    curr.close()

    db_object = connect_to_db()
    channel_pkgs = "SET FOREIGN_KEY_CHECKS=0; DROP TABLE if EXISTS `channel_packages`; CREATE TABLE `channel_packages`(`channel_package_id` INT " \
                   "PRIMARY KEY NOT NULL UNIQUE AUTO_INCREMENT, `package_id` INT(11) NOT NULL, `channel_id` INT(11) " \
                   "NOT NULL, FOREIGN KEY (`package_id`) REFERENCES `packages`(`package_id`) ON UPDATE CASCADE " \
                   "ON DELETE CASCADE, FOREIGN KEY (`channel_id`) REFERENCES `channels`(`channel_id`) " \
                   "ON UPDATE CASCADE ON DELETE CASCADE);"
    curr = execute(db_object, channel_pkgs)
    curr.close()
    return render_template('added_success.html')


@app.route('/pop-all-tables')
def populate_all():
    db_object = connect_to_db()
    techs = "INSERT INTO `technicians` (first_name, last_name, employer_id, start_date) VALUES (\"Sally\", \"Jones\", " \
            "\"e6fb2a3c-198d-49f0-a473-92283b9e2759\", \"2018-10-20\"), (\"Robert\", \"Smith\", " \
            "\"4d139544-d6dd-4d3d-80f8-34d96666f1fa\", \"2018-11-20\"), (\"Samuel\", \"Johnson\", " \
            "\"744d2a6e-1981-4c9f-ba17-7ae6a39bea12\", \"2019-10-20\"), (\"Lana\", \"Walker\", " \
            "\"045c1c03-7999-4b1a-a9a0-6047e32cc18b\", \"2018-10-23\");"
    curr = execute(db_object, techs)
    curr.close()

    db_object = connect_to_db()
    installs = "INSERT INTO `installations` (technician_id, installation_rating, installation_date, comments) VALUES " \
               "(1, NULL, \"2015-10-20\", NULL), (1, 4, \"2018-04-20\", " \
               "\"Refunded customer due to putting hole in wall.\"), (2, 5, \"2019-10-09\", NULL), " \
               "(3, NULL, \"2020-10-23\", \"Customer wants more information on premium packages.\");"
    curr = execute(db_object, installs)
    curr.close()

    db_object = connect_to_db()
    subrs = "INSERT INTO `subscribers` (first_name, last_name, phone_number, postal_code, installation_id, " \
            "monthly_watch_time, active, age, gender) VALUES (\"Sarah\", \"Stubbs\", 555-333-5356, 78739, 2, 6440, 1, " \
            "27, \"Female\"), (\"Richard\", \"Jackson\", 455-433-5256, 77335, 3, 9000, 1, 37, \"Male\"), (\"Brittney\", " \
            "\"Cardone\", 555-773-5006, 91210, 4, 1800, 1, 25, \"Female\"), (\"Joseph\", \"Smith\", 665-333-9356, 33094, " \
            "1, 900, 0, 60, NULL);"
    curr = execute(db_object, subrs)
    curr.close()

    db_object = connect_to_db()
    pkgs = "INSERT INTO `packages` (package_name, standard_price, premium_price) VALUES (\"Stars N More\", 3.49, 10.99), " \
           "(\"Sports All Day\", 4.79, 12.00), (\"News And Brews\", 1.50, 6.00);"
    curr = execute(db_object, pkgs)
    curr.close()

    db_object = connect_to_db()
    subns = "INSERT INTO `subscriptions` (package_id, subscriber_id, time_start, last_renewed, subscription_status) " \
            "VALUES (\"Sarah\", \"Stubbs\", 555-333-5356, 78739, 2, 6440, 1, 27, \"Female\"), (\"Richard\", \"Jackson\", " \
            "455-433-5256, 77335, 3, 9000, 1, 37, \"Male\"), \"Brittney\", \"Cardone\", 555-773-5006, 91210, 4, " \
            "1800, 1, 25, \"Female\"), (\"Joseph\", \"Smith\", 665-333-9356, 33094, 1, 900, 0, 60, NULL);"
    curr = execute(db_object, subns)
    curr.close()

    db_object = connect_to_db()
    genres = "INSERT INTO `packages` (genre_name, kid_friendly) VALUES (\"Adult Animation\", 0), (\"Sports\", 1), " \
             "(\"Reality TV\", 0), (\"Children Animation\", 1), (\"Educational\", 1);"
    curr = execute(db_object, genres)
    curr.close()

    db_object = connect_to_db()
    channels = "INSERT INTO `channels` (channel_name, channel_number, channel_genre_id) VALUES (\"MTV\", 70, 3), " \
               "(\"History\", 49, 5), (\"Disney\", 43, 4), (\"E!\", 66, 3), (\"ESPN\", 30, 2);"
    curr = execute(db_object, channels)
    curr.close()

    db_object = connect_to_db()
    channel_pkgs = "INSERT INTO `channel packages` (channel_id, package_id) " \
                   "VALUES (1, 1, 3), (2, 3), (3, 4), (5, 5), (4, 3);"
    curr = execute(db_object, channel_pkgs)
    curr.close()

    return render_template('tmp_base.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
