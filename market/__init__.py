from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'cd640e6a07ee58320bfaf936'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

#packaging every flask element into a new directory

login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category='info'
from market import routes
