from flask import Blueprint, render_template, request
from FlaskBlog.models import Posts


main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', default=1, type=int)
    posts = Posts.query.order_by(Posts.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', title="  Home", posts=posts)


@main.route('/about')
def about():
    return render_template('about.html', title="About")