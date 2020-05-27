import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import smtplib

app = Flask(__name__)

app.config['SECRET_KEY'] = '03bfb5deb425a988ac645295df924ed6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
pass_encrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'
# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT']=587
# app.config['MAIL_USE_TLS']=True
# app.config['MAIL_USERNAME']='Vipul.rt99@gmail.com'
# app.config['MAIL_USERNAME']='PrincessLeia'
# mail=Mail(app)

# mail=smtplib.SMTP('smtp.gmail.com:587')
# mail.ehlo()
# mail.login("vipul.rt99@gmail.com","PrincessLeia")


from FlaskBlog import routes
