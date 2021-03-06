from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from FlaskBlog.config import Config
import smtplib



db = SQLAlchemy()
pass_encrypt=Bcrypt()
login_manager=LoginManager()
login_manager.login_view='users.login'
login_manager.login_message_category='info'
mail=smtplib.SMTP('smtp.gmail.com',587)
fromEmail="Your Email Address"
emailPassword="Your Password"


def createApp(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    pass_encrypt.init_app(app)
    login_manager.init_app(app)

    from FlaskBlog.users.routes import users
    from FlaskBlog.posts.routes import posts
    from FlaskBlog.main.routes import main

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    return app