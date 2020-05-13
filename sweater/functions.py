import random
import string
from sweater import db

# functions for generate username for new user
from flask import request

from flask import flash
from flask_login import login_user
from werkzeug.security import check_password_hash
from werkzeug.utils import redirect

from models import User


def generate_nick():
    number = random.randrange(1000, 9999)
    prefix_letter = random.choice(string.ascii_lowercase)
    username = prefix_letter + str(number)
    return username


def register():
    password = request.form.get('password')
    password_retype = request.form.get('password_retype')
    if request.method == 'POST':
        if not password:
            flash('Заповніть поле "Пароль"')
            return False
        elif not password_retype:
            flash('Заповніть полe "Повторити пароль"')
            return False
        elif password != password_retype:
            flash('Паролі не співпадають')
            return False
    return password


def login_check():
    login = request.form.get('login')
    password = request.form.get('password')
    if login and password:
        user = User.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            if next_page is None:
                next_page = '/user_panel'
            return redirect(next_page)
        else:
            flash('Логін та пароль хибні')
    else:
        flash('Введіть логін та пароль')