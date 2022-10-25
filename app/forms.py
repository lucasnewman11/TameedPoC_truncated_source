from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField, DateField, DecimalField, FormField, SelectField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User
from ordered_set import OrderedSet
from icecream import ic


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

    @property
    def all_fields(self):
        names = list(OrderedSet([k for k in type(self).__dict__]) - OrderedSet(['__module__', '__doc__', '_unbound_fields', '_wtforms_meta', 'all_fields', 'base_fields', 'first_fields', 'second_fields', 'validate_username', 'validate_email']))
        return names


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    company_name = StringField("Company Name", validators=[DataRequired()])
    commercial_registry_number = StringField("Commercial Registry Number", validators=[DataRequired()])
    building_number = StringField("Building Number", validators=[DataRequired()])
    secondary_number = StringField("Secondary Number", validators=[DataRequired()])
    street_name = StringField("Street Name", validators=[DataRequired()])
    district = StringField("District", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    country = StringField("Country", validators=[DataRequired()])
    zip_code = StringField("Zip Code", validators=[DataRequired()])
    phone_number = StringField("Phone Number", validators=[DataRequired()])
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    iban =  StringField('IBAN Number:', validators=[DataRequired()])

    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

    @property
    def all_fields(self):
        names = list(OrderedSet([k for k in type(self).__dict__]) - OrderedSet(['__module__', '__doc__', '_unbound_fields', '_wtforms_meta', 'all_fields', 'base_fields', 'first_fields', 'second_fields', 'validate_username', 'validate_email']))
        return names

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    company_name = StringField("Company Name", validators=[DataRequired()])
    commercial_registry_number = StringField("Commercial Registry Number", validators=[DataRequired()])
    building_number = StringField("Building Number", validators=[DataRequired()])
    secondary_number = StringField("Secondary Number", validators=[DataRequired()])
    street_name = StringField("Street Name", validators=[DataRequired()])
    district = StringField("District", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    country = StringField("Country", validators=[DataRequired()])
    zip_code = StringField("Zip Code", validators=[DataRequired()])
    phone_number = StringField("Phone Number", validators=[DataRequired()])
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    iban =  StringField('IBAN Number:', validators=[DataRequired()])

    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

    @property
    def all_fields(self):
        names = list(OrderedSet([k for k in type(self).__dict__]) - OrderedSet(['__module__', '__doc__', '_unbound_fields', '_wtforms_meta', 'all_fields', 'base_fields', 'first_fields', 'second_fields', 'validate_username', 'validate_email']))
        return names

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(\
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    company_name = StringField("Company Name", validators=[DataRequired()])
    commercial_registry_number = StringField("Commercial Registry Number", validators=[DataRequired()])
    building_number = StringField("Building Number", validators=[DataRequired()])
    secondary_number = StringField("Secondary Number", validators=[DataRequired()])
    street_name = StringField("Street Name", validators=[DataRequired()])
    district = StringField("District", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    country = StringField("Country", validators=[DataRequired()])
    zip_code = StringField("Zip Code", validators=[DataRequired()])
    phone_number = StringField("Phone Number", validators=[DataRequired()])
    iban =  StringField('IBAN Number:', validators=[DataRequired()])

    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

    @property
    def all_fields(self):
        names = list(OrderedSet([k for k in type(self).__dict__]) - OrderedSet(['__module__', '__doc__', '_unbound_fields', '_wtforms_meta', 'all_fields', 'base_fields', 'first_fields', 'second_fields', 'validate_username', 'validate_email']))
        return names

class EditProfileForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[])
    password2 = PasswordField(\
        'Repeat Password', validators=[EqualTo('password')])
    company_name = StringField("Company Name", validators=[DataRequired()])
    commercial_registry_number = StringField("Commercial Registry Number", validators=[DataRequired()])
    building_number = StringField("Building Number", validators=[DataRequired()])
    secondary_number = StringField("Secondary Number", validators=[DataRequired()])
    street_name = StringField("Street Name", validators=[DataRequired()])
    district = StringField("District", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    country = StringField("Country", validators=[DataRequired()])
    zip_code = StringField("Zip Code", validators=[DataRequired()])
    phone_number = StringField("Phone Number", validators=[DataRequired()])
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    iban =  StringField('IBAN Number:', validators=[DataRequired()])

    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

    @property
    def all_fields(self):
        names = list(OrderedSet([k for k in type(self).__dict__]) - OrderedSet(['__module__', '__doc__', '_unbound_fields', '_wtforms_meta', 'all_fields', 'base_fields', 'first_fields', 'second_fields', 'validate_username', 'validate_email']))
        return names
    
class CreatePurchaseOrderForm(FlaskForm):
    name_of_project = StringField('Name of Project', validators=[DataRequired()])
    po_contract_number  = StringField('PO/Contract Number', validators=[DataRequired()])
    date_of_po = DateField('Date of PO', validators=[DataRequired()])
    value_of_po = StringField("Value of PO", validators=[DataRequired()])
    po_issuer = StringField("PO Issuer Email", validators=[DataRequired()])
    first_company_name = StringField("Company Name", validators=[DataRequired()])
    first_commercial_registry_number = StringField("Commercial Registry Number", validators=[DataRequired()])
    first_building_number = StringField("Building Number", validators=[DataRequired()])
    first_secondary_number = StringField("Secondary Number", validators=[DataRequired()])
    first_street_name = StringField("Street Name", validators=[DataRequired()])
    first_district = StringField("District", validators=[DataRequired()])
    first_city = StringField("City", validators=[DataRequired()])
    first_country = StringField("Country", validators=[DataRequired()])
    first_zip_code = StringField("Zip Code", validators=[DataRequired()])
    first_phone_number = StringField("Phone Number", validators=[DataRequired()])
    first_email = StringField("Email Address", validators=[DataRequired()])
    first_iban =  StringField('IBAN Number:', validators=[DataRequired()])
    second_company_name = StringField("Company Name", validators=[DataRequired()])
    second_commercial_registry_number = StringField("Commercial Registry Number", validators=[DataRequired()])
    second_building_number = StringField("Building Number", validators=[DataRequired()])
    second_secondary_number = StringField("Secondary Number", validators=[DataRequired()])
    second_street_name = StringField("Street Name", validators=[DataRequired()])
    second_district = StringField("District", validators=[DataRequired()])
    second_city = StringField("City", validators=[DataRequired()])
    second_country = StringField("Country", validators=[DataRequired()])
    second_zip_code = StringField("Zip Code", validators=[DataRequired()])
    second_phone_number = StringField("Phone Number", validators=[DataRequired()])
    second_email = StringField("Email Address", validators=[DataRequired()])
    second_iban =  StringField('IBAN Number:', validators=[DataRequired()])
    submit = SubmitField('Submit')

    @property
    def all_fields(self):
        names = list(OrderedSet([k for k in type(self).__dict__]) - OrderedSet(['__module__', '__doc__', '_unbound_fields', '_wtforms_meta', 'all_fields', 'base_fields', 'first_fields', 'second_fields']))
        return names

    @property
    def base_fields(self):
        return ['name_of_project',
        'po_contract_number',
        'date_of_po',
        'value_of_po',
        'po_issuer',]

    @property
    def first_fields(self):
        first = [name for name in self.all_fields if name[:5] == "first"]
        return first

    @property
    def second_fields(self):
        second = [name for name in self.all_fields if name[:6] == "second"]
        return second


                                     

