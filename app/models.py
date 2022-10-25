import json
from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from icecream import ic
from copy import copy

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))
    cuuid = db.Column(db.String(120))

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

company_order = db.Table('CompanyOrder',
    db.Column('Company_id', db.Integer, db.ForeignKey('company.id')),
    db.Column('Order_id', db.Integer, db.ForeignKey('order.id')))
    
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(120))
    commercial_registry_number = db.Column(db.String(120))
    building_number = db.Column(db.String(120))
    secondary_number = db.Column(db.String(120))
    street_name = db.Column(db.String(120))
    district = db.Column(db.String(120))
    city = db.Column(db.String(120))
    country = db.Column(db.String(120))
    zip_code = db.Column(db.String(120))
    phone_number = db.Column(db.String(120))
    email = db.Column(db.String(120))
    iban =  db.Column(db.String(120))
    orders = db.relationship('Order', secondary=company_order, backref='companies')

    def __repr__(self):
        return '<Company {}>'.format(self.company_name)

    @property
    def json(self):
        dct = self.__dict__
        dct.pop('_sa_instance_state')
        ic(dct)
        return json.dumps(dct)

    @property
    def dct(self):
        dct = copy(self.__dict__)
        dct.pop('_sa_instance_state')
        return dct
                         
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_of_project = db.Column(db.String(120))
    po_contract_number  = db.Column(db.String(120))
    date_of_po = db.Column(db.DateTime, default=datetime.utcnow)
    value_of_po = db.Column(db.String(120))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    purchaser = db.Column(db.Integer, db.ForeignKey('company.id'))
    financier = db.Column(db.Integer, db.ForeignKey('company.id'))
    issuer = db.Column(db.Integer, db.ForeignKey('company.id'))
    step = db.Column(db.String(120))
    status = db.Column(db.String(120))
    awaiting = db.Column(db.Integer, db.ForeignKey('company.id'))
    current_step = db.Column(db.String(120))
    documents = db.relationship('Document', backref='order')

    def __repr__(self):
        return '<Order {}>'.format(self.po_contract_number)

    @property
    def json(self):
        dct = copy(self.__dict__)
        dct.pop('_sa_instance_state')
        ic(dct)
        return json.dumps(dct)

    @property
    def dct(self):
        dct = copy(self.__dict__)
        dct.pop('_sa_instance_state')
        return dct

class Document(db.Model):
    pid = db.Column(db.String(120), primary_key=True)
    template_id = db.Column(db.Integer, db.ForeignKey('template.pid'))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    status = db.Column(db.String(120))

    def __repr__(self):
        return '<Document {}>'.format(self.pid)

    @property
    def dct(self):
        dct = copy(self.__dict__)
        dct.pop('_sa_instance_state')
        return dct


class Template(db.Model):
    pid = db.Column(db.String(120), primary_key=True)
    folder_pid = db.Column(db.String(120))
    name = db.Column(db.String(120))
    documents = db.relationship('Document', backref='template')

    def __repr__(self):
        return '<Template {}>'.format(self.pid)

class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    step_number = db.Column(db.String(120))
    name = db.Column(db.String(120))
    date_activated = db.Column(db.DateTime, default=datetime.utcnow)
    date_terminated = db.Column(db.DateTime, default=datetime.utcnow)
    company = db.Column(db.String(120))
    role = db.Column(db.String(120))
    status = db.Column(db.String(120))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))

# user_channel = db.Table('AB',
#     db.Column('A_id', db.Integer, db.ForeignKey('A.id')),
#     db.Column('B_id', db.Integer, db.ForeignKey('B.id'))
# )

# class A(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20))
#     following = db.relationship('B', secondary=user_channel, backref='followers')

#     def __repr__(self):
#         return f'<User: {self.name}>'

# class B(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20))

#     def __repr__(self):
#         return f'<Channel: {self.name}>'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
#################################
