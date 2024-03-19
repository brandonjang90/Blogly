"""Blogly application."""
from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "itsasecret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def root():
    """Homepage of most recent posts."""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("homepage.html", posts=posts)

# User route
@app.route('/users')
def users_index():
    """Show a page with info on all users"""

    users = User.query.all()
    return render_template('users/index.html', users=users)


@app.route('/users/form', methods=["GET"])
def users_new_form():
    """Show a form to create a new user"""

    return render_template('users/form.html')


@app.route("/users/form", methods=["POST"])
def users_new():
    """Handle form submission for creating a new user"""

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>')
def users_detail(user_id):
    """Show the user detail page"""

    user = User.query.get_or_404(user_id)
    return render_template('users/detail.html', user=user)


@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """Show a form to edit an existing user"""

    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_delete(user_id):
    """Handle form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


#Part 2 Post Routes#

@app.route('/users/<int:user_id>/posts/form')
def post_new(user_id):
    """Show a form to create a post by the user"""

    user = User.query.get_or_404(user_id)
    return render_template('posts/form.html', user=user)

@app.route('/users/<int:user_id>/posts/form', methods=["POST"])
def posts_new(user_id):
    """Handle form submission for post"""

    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'], 
                    user=user)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def post_detail(post_id):
    """Show the post detail page"""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/detail.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    """Show a form to edit an existing post"""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Handle form submission for updating an existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post.id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    """Handle form submission for deleting an existing post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")


