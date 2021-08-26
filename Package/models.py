from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from Package import db, login_manager,app
from flask_login import UserMixin

 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




# for holding our users(a model we're creating)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)
    # backref allows us to access full info about the user who created the post
    # how our object is presented whenver it is printed

    def get_reset_token(self,expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    # The static method cannot access the class attributes or the instance attributes.
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try :
            user_id = s.loads(token)['user_id']
        except:
            return None 
        return User.query.get(user_id)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}','{self.image_file}')"

# for holding our posts
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self): 
        return f"Post('{self.title}', '{self.date_posted}')"


# --------------------------------------------------------------
# creates classes for each db items inheriting from model class
# set required constraints and bheaviour according to needs
# has a relation to Post model and backref is like adding another column to {Post} model
# backref allows us to access the author from a given post
# lazy says the sqlalchemy will load the data from the database in one go (in lazy format)
# --------------------------------------------------------------

 # in foreign key we are referencing the tablename and columname so in lowercase letters
    # so usrname model has automatically this table name is lowercase letters 
    # similary a Post model will have it's table name set to post (ie in smaller case letters)
    