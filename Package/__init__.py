from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from Package.config import Config


# extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()

login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__, static_folder="static")
    app.config.from_object(Config)
    db.init_app(app) 
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app) 

    # blueprints
    from Package.users.routes import users 
    from Package.posts.routes import posts 
    from Package.main.routes import main 
    from Package.errors.handlers import errors  
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app 

# --------------------------------------------------------------
# secret key to protect against modifying cookies and cross-site
# request(since for remembering user we are using cookie) etc.