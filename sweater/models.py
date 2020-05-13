from flask_login import UserMixin

from sweater import db, manager


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)


class drugs_and_invertar(db.Model):
    __tablename__ = 'drugs_invertar'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=False)
    country = db.Column(db.String(128), nullable=False, unique=False)


class arrival_of_medicines(db.Model):
    __tablename__ = 'arrival_of_medicines'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Integer, nullable=False, unique=False)
    producer = db.Column(db.String(128), nullable=False, unique=False)
    date_arrival = db.Column(db.DATE, nullable=False, unique=False)
    units = db.Column(db.String(128), nullable=False, unique=False)
    price_per_piece = db.Column(db.Integer, nullable=False, unique=False)
    number = db.Column(db.Integer, nullable=False, unique=False)
    expiration_date = db.Column(db.DATE, nullable=False, unique=False)
    name = db.Column(db.String(128), nullable=False, unique=False)


class departments_of_hospital(db.Model):
    __tablename__ = 'departments_of_hospital'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(128), nullable=False, unique=False)


class hospitals(db.Model):
    __tablename__ = 'hospitals'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    hospital_name = db.Column(db.String(128), nullable=False, unique=False)
    street = db.Column(db.String(128), nullable=False, unique=False)
    boss = db.Column(db.String(128), nullable=False, unique=False)


class provider(db.Model):
    __tablename__ = 'provider'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    provider_name = db.Column(db.String(128), nullable=False, unique=False)
    location = db.Column(db.String(128), nullable=False, unique=False)


class units(db.Model):
    __tablename__ = 'units'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.String(128), nullable=False, unique=False)




@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)