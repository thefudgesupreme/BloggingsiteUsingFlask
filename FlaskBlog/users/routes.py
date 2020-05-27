from flask import (Blueprint,render_template,url_for,flash,request,redirect)
from flask_login import current_user, logout_user, login_required, login_user
from FlaskBlog import db, pass_encrypt
from FlaskBlog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                                        RequestResetForm, ResetPasswordForm)
from FlaskBlog.models import User, Posts
from FlaskBlog.users.utils import save_pic,sendResetEmail


users = Blueprint('users', __name__)


@users.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        encrypted_password = pass_encrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=encrypted_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Created Successfully, Head Over to Login Page...!!!!', 'success')
        return redirect(url_for('main.home'))
    return render_template('./register.html', title="Register", form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        curr_password = form.password.data
        if user:
            check_password = pass_encrypt.check_password_hash(user.password, curr_password)
            if check_password:
                flash('Login Successful', 'success')
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                if next_page:
                    flash(next_page, 'info')
                return redirect(url_for(next_page[1:])) if next_page else redirect(url_for('main.home'))
            else:
                flash('Login Failed....Wrong Password', 'danger')
        else:
            flash('Login Failed...User don\'t Exist', 'danger')
    return render_template('./login.html', title="Log Yourself In", form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.pic.data:
            pic_file = save_pic(form.pic.data)
            current_user.img_file = pic_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account Info Updated', 'success')
        return redirect(url_for('users.account'))
    elif request.method=='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    user_profile = url_for('static', filename='profiles/' + current_user.img_file)
    return render_template('account.html', title="Account Page", img_file=user_profile, form=form)


@users.route("/user/<string:username>")
def userPost(username):
    page = request.args.get('page', default=1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Posts.query.filter_by(author=user) \
        .order_by(Posts.date_posted.desc()) \
        .paginate(page=page, per_page=5)
    return render_template('userPost.html', title="  Home", posts=posts, user=user)


@users.route("/resetPassword", methods=['GET', 'POST'])
def resetRequest():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        sendResetEmail(user)
        flash('Email has been send with instruction', 'warning')
        return redirect(url_for('users.login'))
    return render_template('resetRequest.html', title='Reset Password', form=form)


@users.route("/resetPassword/<token>", methods=['GET', 'POST'])
def resetToken(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verifyResetToken(token=token)
    if not user:
        flash('That is an expired/invalid token', 'warning')
        return redirect(url_for('users.resetRequest'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        encrypted_password = pass_encrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = encrypted_password
        db.session.commit()
        flash(f'Your password has been updated...!!!!', 'success')
        return redirect(url_for('users.login'))
    return render_template('resetToken.html', title='Reset Password', form=form)
