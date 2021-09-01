
import os 
import secrets
from PIL import Image 
from flask import url_for,current_app
from flask_mail import Message
from Package import mail


def save_picture(form_picture):
    
    random_hex = secrets.token_hex(8)
    f_name,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex+f_ext
    picture_path = os.path.join(current_app.root_path, 'static/images/profile_pics',picture_fn)
    
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    
    i.save(picture_path)

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', 
                    sender='anandk8873@gmail.com', 
                    recipients=[user.email])    
    msg.subject = "Reset Your Password"
    msg.body = f'''To reset the password visit the following link :
                {url_for('users.reset_token',token=token,_extenal=True)}
                If you didn't make this request simply ignore! No changes will be made to your account!'''
    mail.send(msg)

