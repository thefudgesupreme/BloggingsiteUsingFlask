from flask import (Blueprint,render_template,url_for,flash,redirect,request,abort)
from flask_login import current_user,login_required
from FlaskBlog import db
from FlaskBlog.models import Posts
from FlaskBlog.posts.forms import PostForm


posts = Blueprint('posts', __name__)

@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        posts = Posts(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(posts)
        db.session.commit()
        flash('Post created Successfully', 'success')
        return redirect(url_for('main.home'))
    return render_template('createPost.html', title="New Post", form=form, legend='New post')


@posts.route("/post/<int:postId>")
def post(postId):
    post = Posts.query.get_or_404(postId)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:postId>/update", methods=['GET', 'POST'])
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
        return redirect(url_for('posts.post', postId=post.id))
    elif request.method=='GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('createPost.html', title="Update Post", form=form, legend="Update Post")


@posts.route("/post/<int:postId>/delete", methods=['POST'])
@login_required
def postDelete(postId):
    post = Posts.query.get_or_404(postId)
    if post.author!=current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post has been deleted successfully', 'success')
    return redirect(url_for('main.home'))
