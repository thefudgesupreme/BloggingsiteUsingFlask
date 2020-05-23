from flask import render_template, flash, redirect, url_for,request
from FlaskBlog import app, db, pass_encrypt
from FlaskBlog.forms import RegistrationForm, LoginForm
from FlaskBlog.models import User
from flask_login import login_user, current_user, logout_user,login_required

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        encrypted_password = pass_encrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=encrypted_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Created Successfully, Head Over to Login Page...!!!!', 'success')
        return redirect(url_for('home'))
    return render_template('./register.html', title="Register", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        curr_password = form.password.data
        if user:
            check_password = pass_encrypt.check_password_hash(user.password, curr_password)
            if check_password:
                flash('Login Successful', 'success')
                login_user(user, remember=form.remember.data)
                next_page=request.args.get('next')
                if next_page:
                    flash(next_page , 'info')
                return redirect(url_for(next_page[1:])) if next_page  else redirect(url_for('home'))
            else:
                flash('Login Failed....Wrong Password', 'danger')
        else:
            flash('Login Failed...User don\'t Exist', 'danger')
    return render_template('./login.html', title="Log Yourself In", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title="Account Page")
