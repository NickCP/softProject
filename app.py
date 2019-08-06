from flask import Flask, render_template, request
import psycopg2
from contextlib import closing
from psycopg2 import sql
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URL'] = 'postgres://postgres:admin@localhost:5432/hospital_med'

db = SQLAlchemy(app)


class Hospital(db.Model):
    __tablename__ = 'example'
    hospital_id = db.Column('hospital_id', db.Integer, primary_key=True)


class Form(FlaskForm):
            hospital = StringField('username')


# def Sql_get_data():
#     with closing(psycopg2.connect(dbname='hospital_med', user='postgres',
#                                   password='admin', host='localhost')) as conn:
#         with conn.cursor() as cursor:
#             conn.autocommit = True
#             cursor.execute('SELECT name FROM hospital LIMIT 20')
#             values = []
#             for row in cursor:
#                 values.append(row)
#             print(values)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    form = Form()
    return render_template('Login.html', form=form)


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        name = request.form['username']
        date_pord = request.form['date_pord']
        date_expiration = request.form['date_expiration']
        sql_add_data(name, date_pord, date_expiration)
    return render_template('index.html')


def sql_add_data(name, pord_date, expiration_date):
    with closing(psycopg2.connect(dbname='hospital_med', user='postgres',
                                  password='admin', host='localhost')) as conn:
        with conn.cursor() as cursor:
            conn.autocommit = True
            values = [(name, pord_date, expiration_date), ]
            insert = sql.SQL('insert into medicine (name,production_date,expiration_date) values {}').format(
                sql.SQL(',').join(map(sql.Literal, values)))
            cursor.execute(insert)
            cursor.execute('SELECT * FROM medicine LIMIT 5')
            for row in cursor:
                print(row)


if __name__ == '__main__':
    app.run()
