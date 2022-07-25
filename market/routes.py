from market import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db
from wtforms import widgets
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if purchase_form.validate_on_submit():
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object and current_user.can_purchase(p_item_object):
            p_item_object.buy(current_user)
            flash("You purchased " + p_item_object.name + " for " + str(p_item_object.price) + '.', category='success')
        else:
            flash('You do not have enough money to purchase this item', category='danger')
    if selling_form.validate_on_submit():
        sold_item = request.form.get('sell_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash("You sold {} for {}".format(s_item_object.name, s_item_object.price), category='success')
            else:
                flash("Something went wrong with selling".format(s_item_object.name, s_item_object.price), category='danger')
        return redirect(url_for('market_page'))
    if request.method == 'GET':
        owned_items = Item.query.filter_by(owner=current_user.id)
        items = Item.query.filter_by(owner=None)
        return render_template('market.html', items=items, purchase_form=purchase_form, selling_form=selling_form, owned_items=owned_items)

@app.route('/show-database-html')
def display_db():
    items = Item.query.all()
    return render_template('raw_database.html', items=items)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                            email_address=form.email_address.data,
                            password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash('Success. Account created as:  ' + user_to_create.username, category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}:
        error_list = form.errors.values()
        for err_msg in error_list:
            flash("Your error is: {}".format(err_msg), category='danger')
        error_list = [] 
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash('Success. Logged in as: ' + attempted_user.username, category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password are not matched. Please try again', category='danger')
    return render_template('login.html', form=form) 

@app.route('/logout')
def logout_page():
    logout_user()
    flash('Successfully logged out', category='info')
    return redirect(url_for('home_page'))
