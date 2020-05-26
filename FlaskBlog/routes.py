import os
import secrets

from PIL import Image
from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import login_user, current_user, logout_user, login_required

from FlaskBlog import app, db, pass_encrypt
from FlaskBlog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from FlaskBlog.models import User, Posts


@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', default=1, type=int)
    posts = Posts.query.order_by(Posts.date_posted.desc()).paginate(page=page, per_page=5)
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
                next_page = request.args.get('next')
                if next_page:
                    flash(next_page, 'info')
                return redirect(url_for(next_page[1:])) if next_page else redirect(url_for('home'))
            else:
                flash('Login Failed....Wrong Password', 'danger')
        else:
            flash('Login Failed...User don\'t Exist', 'danger')
    return render_template('./login.html', title="Log Yourself In", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_pic(form_pic):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pic.filename)
    pic_filename = random_hex + f_ext
    pic_path = os.path.join(app.root_path, 'static/profiles', pic_filename)
    form_pic.save(pic_path)

    output_size = (125, 125)
    i = Image.open(form_pic)
    i.thumbnail(output_size)
    i.save(pic_path)
    return pic_filename


@app.route('/account', methods=['GET', 'POST'])
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
        return redirect(url_for('account'))
    elif request.method=='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    user_profile = url_for('static', filename='profiles/' + current_user.img_file)
    return render_template('account.html', title="Account Page", img_file=user_profile, form=form)


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        posts = Posts(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(posts)
        db.session.commit()
        flash('Post created Successfully', 'success')
        return redirect(url_for('home'))
    return render_template('createPost.html', title="New Post", form=form, legend='New post')


@app.route("/post/<int:postId>")
def post(postId):
    post = Posts.query.get_or_404(postId)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:postId>/update", methods=['GET', 'POST'])
@login_required
def postUpdate(postId):
    post = Posts.query.get_or_404(postId)
    if post.author!=current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash(f'Post Updated to {post.title}', 'success')
        return redirect(url_for('post', postId=post.id))
    elif request.method=='GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('createPost.html', title="Update Post", form=form, legend="Update Post")


@app.route("/post/<int:postId>/delete", methods=['POST'])
@login_required
def postDelete(postId):
    post = Posts.query.get_or_404(postId)
    if post.author!=current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post has been deleted successfully', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def userPost(username):
    page = request.args.get('page', default=1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Posts.query.filter_by(author=user) \
        .order_by(Posts.date_posted.desc()) \
        .paginate(page=page, per_page=5)
    return render_template('userPost.html', title="  Home", posts=posts, user=user)
