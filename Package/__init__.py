import os 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__, static_folder="static")
app.config["SECRET_KEY"] = "7fbd502c8e9cbe75145444150d96627431180a5a343890"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False 
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
 #for Prohibiting accessing the account url 
 # directyly(redirect  to login page with a good looking msg )
login_manager.login_message_category = 'info'
 #bootstrap class' msgs we are using insted of default one 
# to avoid circular import error we need to 

# setting up the mail environment
app.config['MAIL_SERVER'] = 'smtp.google.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True 
# using the enviornment variables for security reasons
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
# intialize the mail extension
mail = Mail(app)


# import here
from Package import route 





# --------------------------------------------------------------
# secret key to protect against modifying cookies and cross-site
# request(since for remembering user we are using cookie) etc.

# uri for database
# /// tells realtive path (current directory)
# so a site.db must get created once we run it
# create an instance of sqlalchemy database
# ---------------------------------------------------------------
# place where we initialize our application and 
# gather different components
