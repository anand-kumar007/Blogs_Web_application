import os 

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY_FLASK_SOCIOAPP')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_FLASK_SOCIOAPP')
    SQLALCHEMY_TRACK_MODIFICATIONS =False 
    
    # setting up the mail environment
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True 
    # using the enviornment variables for security reasons
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
