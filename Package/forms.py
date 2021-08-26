
from flask_wtf import FlaskForm 
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField 
from wtforms.validators import DataRequired, Length,Email,EqualTo, ValidationError
from Package.models import User

# class that'll inherit from FlaskForm
class RegistrationForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired(),Length(min=2,max=15)])
    email = StringField("Email",validators=[DataRequired(),Email()])    
    password = PasswordField("Password",validators=[DataRequired(),Length(min=4,max=20)])
    confirm_password = PasswordField("Confirm Password",validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')

    # validation for existing username
    
    def validate_username(self,username) :
        user = User.query.filter_by(username= username.data).first()
        if user:
            raise ValidationError('username already taken !')

    def validate_email(self,email) :
        user = User.query.filter_by(email= email.data).first()
        if user:
            raise ValidationError('Account already exists with this mail id !')



# login form
class LoginForm(FlaskForm):
    
    email = StringField("Email",validators=[DataRequired(),Email()])

    password = PasswordField("Password",validators=[DataRequired(),Length(min=4,max=20)])
    remember = BooleanField('Remember Me')    
    submit = SubmitField('Login')


# -------------------------------------------------
# add a custom validation or do a check if the newly 
# registering user exists in the database 

class UpdateAccountForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired(),Length(min=2,max=15)])
    email = StringField("Email",validators=[DataRequired(),Email()])    
    
    picture = FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png','gif'])])
    submit = SubmitField('Update')

    # user may submit this form without even updating anything
    # validate only when data entered is diffent curr_user info needed
    
    def validate_username(self,username) :
            if username.data != current_user.username :
                user = User.query.filter_by(username= username.data).first()
                if user:
                    raise ValidationError('username already taken !')
       

    def validate_email(self,email) :
            if email.data != current_user.email :
                user = User.query.filter_by(email= email.data).first()
                if user:
                    raise ValidationError('Account already exists with this mail id !')


class PostForm(FlaskForm):
    title = StringField("Title",validators=[DataRequired()])
    content = TextAreaField('Content',validators=[DataRequired()])
    submit = SubmitField('Post..')


class RequestResetForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(),Email()])    
    submit = SubmitField('Request Password Reset ')

    def validate_email(self,email) :
        user = User.query.filter_by(email= email.data).first()
        if user is None:
            raise ValidationError('There is No Account with that email ! You must register first !')
        

class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password",validators=[DataRequired(),Length(min=4,max=20)])
    confirm_password = PasswordField("Confirm Password",validators=[DataRequired(),EqualTo('password')])
    
    submit = SubmitField('Reset Password')

