from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from FlaskBlog import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    img_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    posts = db.relationship('Posts', backref="author", lazy=True)

    def getResetToken(self,expireSec=1800):
        s=Serializer(app.config['SECRET_KEY'],expireSec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verifyResetToken(token):
        s=Serializer(app.config['SECRET_KEY'])
        try:
            user_id=s.loads(token)['user_id']
        except:
            return  None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.img_file}')"


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Posts('{self.title}','{self.date_posted}')"
