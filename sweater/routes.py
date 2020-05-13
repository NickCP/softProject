from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, logout_user
from werkzeug.security import generate_password_hash
from sweater import db

from models import User, arrival_of_medicines
from models import drugs_and_invertar, units
from sweater import app


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    from functions import login_check
    response = login_check()
    if response is None:
        return render_template('login.html')
    return response


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    from functions import login_check
    login_check()
    return render_template('login.html')


@app.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    from functions import generate_nick, register
    new_username = generate_nick()
    if register():
        password = register()
        hash_password = generate_password_hash(password)
        new_user = User(login=new_username, password=hash_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Ви зареєстрували користувача із Username: {0}'.format(new_username))
    return render_template('add_user.html', new_username=new_username)


@app.route('/add_data', methods=['GET', 'POST'])
@login_required
def add_data():
    items_drugs_and_invertar = drugs_and_invertar.query.all()
    items_units = units.query.all()
    items_action = []
    items = []
    for item in items_drugs_and_invertar:
        items.append(item.name)

    for item2 in items_units:
        items_action.append(item2.unit)

    if request.method == 'POST':
        name = request.form.get('name_med')
        num = int(request.form['num'])
        number = int(request.form['box_number'])
        producer = request.form['producer']
        date_arrival = request.form['date']
        price_per_piece = request.form['price']
        expiration_date = request.form['expiration_date']
        units_value = request.form.get("units")
        new_drugs = arrival_of_medicines(num=num, producer=producer, date_arrival=date_arrival,\
                                         price_per_piece=price_per_piece, number=number, units=units_value,\
                                         expiration_date=expiration_date, name=name)
        db.session.add(new_drugs)
        db.session.commit()

    #     sql_add_data(name, country)
    # items = get_data_database_drugs()
    # items_action = get_data_unit()

    return render_template('add_data.html', items=items, items_action=items_action)


@app.route('/user_panel')
@login_required
def user_panel():
    return render_template('user_panel.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_page'))


@app.route('/prescribe', methods=['GET', 'POST'])
@login_required
def prescribe():
    items_drugs_and_invertar = drugs_and_invertar.query.all()
    items_units = units.query.all()
    items_action = []
    items = []
    rows = arrival_of_medicines.query.all()
    for item in items_drugs_and_invertar:
        items.append(item.name)

    for item2 in items_units:
        items_action.append(item2.unit)
    return render_template('prescribe.html', items=items, items_action=items_action, rows=rows)


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)
    return response
