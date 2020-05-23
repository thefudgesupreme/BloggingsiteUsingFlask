from flask import render_template, flash, redirect, url_for
from FlaskBlog.forms import RegistrationForm, LoginForm
from FlaskBlog import app
from FlaskBlog.models import User, Posts

posts = [
    {
        'author': "Vipul",
        'title': "About author",
        'date': "April 10, 2020"
    },
    {
        'author': "Vipul",
        'title': "First Post",
        'date': "April 12, 2020"
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title="  Home", posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title="About")


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account Created For  ==> {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('./register.html', title="Register", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data=="admin@blog.com" and form.password.data=="123":
            flash(f'Successful Login ', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Failed...Check Your Credentials...!!!', 'danger')
    return render_template('./login.html', title="Log Yourself In", form=form)
