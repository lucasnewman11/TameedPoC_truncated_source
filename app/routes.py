from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, db
from app.forms import *
from app.models import *
import doc_api, tameed_steps, json
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime
from icecream import ic
from tameed_steps import *
import pickle
import uuid
import time

DAPI = doc_api.DocApi()
DATA = load_data()
ORDERS = DATA["ORDERS"]
CURRENT_USER_EMAIL = None

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/index')
@app.route('/home')
# @login_required
def home():
    if not CURRENT_USER_EMAIL:
        logout_user()
    
    if current_user.is_authenticated:
        nav_item_tuples = [         ("Dashboard", url_for("dashboard")),
         ("About", "#about"),
         ("Logout", url_for('logout'))]
    else:
        nav_item_tuples = [("About", "#about"),
                           ("Login", url_for('login'))]

    return render_template("tameed_home.html",
                           title='Tameed Home',
                           nav_item_tuples=nav_item_tuples)

@app.route('/login', methods=['GET', 'POST'])
def login(no_such_user=False, wrong_password=False, invalid_login=False):
    global CURRENT_USER_EMAIL
    nav_item_tuples = [("Home", url_for('home'))]
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            ic(user)
            if user is None:
                print("THIS")
                return redirect(url_for('login', no_such_user=True))
            elif not user.check_password(form.password.data):
                return redirect(url_for('login', wrong_password=True))
            else:
                login_user(user, remember=form.remember_me.data)
                CURRENT_USER_EMAIL = form.email.data
                return redirect(url_for('dashboard'))
        else:
            invalid_login = True
    app.jinja_env.globals.update(getattr=getattr, type=type, print=print, ic=ic)
    if request.args.get('wrong_password'):
        wrong_password = request.args.get('wrong_password')
    elif request.args.get('no_such_user'):
        no_such_user = request.args.get('no_such_user')

    return render_template('login.html', no_such_user=no_such_user, wrong_password=wrong_password, title='Sign In', form=form, nav_item_tuples=nav_item_tuples, invalid_login=invalid_login)

@app.route('/register', methods=['GET', 'POST'])
def register():
    global CURRENT_USER_EMAIL
    global DATA
    nav_item_tuples = [("Home", "/home"),
                       ("Login", url_for('login'))]

    if current_user.is_authenticated:
        logout()
    form = RegistrationForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()
        if user:
            return redirect(url_for('login', invalid_user=True))

        CURRENT_USER_EMAIL = form.email.data
        user = User(email=form.email.data)
        company = CompanyW(company_name = form.company_name.data,
                          commercial_registry_number = form.commercial_registry_number.data,
                          building_number = form.building_number.data,
                          secondary_number = form.secondary_number.data,
                          street_name = form.street_name.data,
                          district = form.district.data,
                          city = form.city.data,
                          country = form.country.data,
                          zip_code = form.zip_code.data,
                          phone_number = form.phone_number.data,
                          email = form.email.data,
                          iban = form.iban.data,
                           uuid = str(uuid.uuid1()))
        user.cuuid = company.uuid
        user.set_password(form.password.data)
        db.session.add(user, company)
        db.session.commit()
        DATA["COMPANIES"][user.cuuid] = company
        persist_data(DATA)
        logout_user()
        login_user(user, remember=True)
        CURRENT_USER_EMAIL = user.email
        return redirect(url_for('dashboard'))                
        
    app.jinja_env.globals.update(getattr=getattr, type=type, print=print, ic=ic)
    return render_template('registration.html', title='Register', form=form, nav_item_tuples=nav_item_tuples)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    ic(form)
    ic(form.all_fields)
    if request.method == 'POST':
        for i in form.all_fields:
            if i not in ("submit", 'password', 'password2'):
                setattr(current_user.company,  i, getattr(form, i).data)
                ic(i, getattr(current_user.company, i), getattr(form, i).data)
        if form.password.data:
            current_user.set_password(form.password.data)
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        for i in form.all_fields:
            if i not in ("submit", 'password', 'password2'):
                getattr(form, i).data = getattr(current_user.company, i)
                ic(i, getattr(form, i).data, getattr(current_user.company, i))
    nav_item_tuples = [("Home", url_for('home')), ("Dashboard", url_for('dashboard')), ('Logout', url_for('logout'))]
    app.jinja_env.globals.update(getattr=getattr, type=type, print=print, ic=ic)
    return render_template('registration.html', title='Edit Profile',
                           form=form, nav_item_tuples=nav_item_tuples)

@app.route('/createpo', methods=['GET', 'POST'])
@login_required
def create_po():
    global DATA
    form = CreatePurchaseOrderForm()
    ic(DATA["COMPANIES"][current_user.cuuid])
    if request.method == "POST":
        order = step_zero(form, DAPI, DATA)
        while DAPI.doc_status(order.aop.pid)['status'] in ('document.draft', 'document.uploaded'):
            DAPI.send_document(order.aop.pid)
        while DAPI.doc_status(order.bcover.pid)['status'] in ('document.draft', 'document.uploaded'):
            DAPI.send_document(order.bcover.pid)
        while DAPI.doc_status(order.ccover.pid)['status'] in ('document.draft', 'document.uploaded'):
            DAPI.send_document(order.ccover.pid)

        return redirect(url_for('dashboard')) 
    nav_item_tuples = [("Home", url_for("home")),
                       ("Dashboard", url_for("dashboard")),
                       ("Logout", url_for('logout'))]
    app.jinja_env.globals.update(getattr=getattr, type=type, print=print, ic=ic)
    return render_template('createpo_flask.html',
                           title='Create Purchase Order',
                           form=form,
                           company=DATA["COMPANIES"][current_user.cuuid],
                           nav_item_tuples=nav_item_tuples)

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    if not CURRENT_USER_EMAIL:
        return redirect(url_for('home'))
    user_orders = [o for o in ORDERS if CURRENT_USER_EMAIL in (o.purchaser.email, o.financier.email, o.issuer.email)]
    update_state(user_orders, DAPI, DATA)
    nav_item_tuples = [("Home", url_for("home")),
                                              ("Logout", url_for('logout'))]
    app.jinja_env.globals.update(getattr=getattr,
                                  type=type,
                                  print=print,
                                 str=str,
                                  ic=ic,
                                  OrderW=OrderW,
                                  CompanyW=CompanyW,
                                  DocumentW=DocumentW,
                                  User=User)
    if request.args:
        for o in ORDERS:
            if o.po_contract_number == request.args["no"]:
                order = o
        if request.args["result"] == "approve":
            o.step = "COMPLETE"
        if request.args["result"] == "reject":
            o.step = "FAILED"
    return render_template('dashboard2_flask.html', nav_item_tuples = nav_item_tuples, orders=ORDERS, user_email=CURRENT_USER_EMAIL)

@app.route('/order_view')
def order_view():
    update_state(ORDERS, DAPI, DATA)
    if request.method == 'GET':
        for o in ORDERS:
            if o.po_contract_number == request.args['no']:
                order = o

        aop_url= DAPI.embed_link(order.aop.pid, CURRENT_USER_EMAIL)
        bcover_url= DAPI.embed_link(order.bcover.pid, CURRENT_USER_EMAIL) if CURRENT_USER_EMAIL in (order.financier.email, order.issuer.email) else None
        ccover_url= DAPI.embed_link(order.ccover.pid, CURRENT_USER_EMAIL) if CURRENT_USER_EMAIL in (order.purchaser.email, order.issuer.email) else None

        if order.purchaser.email == CURRENT_USER_EMAIL:
            role = "Purchaser"
        elif order.financier.email == CURRENT_USER_EMAIL:
            role = "Bank/FinTech"
        else:
            role = "Issuer"

        ic(order.step, order.issuer.email, CURRENT_USER_EMAIL)
        return render_template('order_view.html', order=order, aop_url = aop_url, bcover_url = bcover_url, ccover_url = ccover_url, role=role, current_user_email=CURRENT_USER_EMAIL)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# FETCHES
@app.route('/fetch_company_names', methods = ['GET'])
def fetch_company_names():
    company_names = [DATA["COMPANIES"][i].company_name for i in DATA["COMPANIES"] if DATA["COMPANIES"][i].company_name]
    return jsonify(tuple(company_names))

@app.route('/fetch_company_data', methods = ['GET'])
def fetch_company_data():

    return jsonify([i for i in DATA["COMPANIES"].values() if i.company_name == request.args.get('company_name')][0].__dict__)



