from flask import (render_template,url_for, flash, redirect, request, abort, Blueprint)

from flask_login import current_user, login_required 

from Package import db 
from Package.models import Post 
from Package.posts.forms import PostForm 



posts = Blueprint('posts',__name__)


@posts.route('/post/new',methods=["POST","GET"])
@login_required
def new_post():
    postform = PostForm()

    if postform.validate_on_submit():
        # add to database
         post = Post(title=postform.title.data, content =postform.content.data, author=current_user)
         db.session.add(post)
         db.session.commit()

         flash('Your Post has been created !','success')
         return redirect(url_for('main.home'))

    return render_template("create_post.html", title="New Post",
     form = postform, legend ='New Post')



@posts.route('/post/<int:post_id>',methods=["POST","GET"])
def post(post_id):

    # post = Post.query.get(post_id)
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title,post=post)


@posts.route('/post/<int:post_id>/update',methods=["POST","GET"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your Post has been updated !','success')
        return redirect(url_for('posts.post',post_id = post.id))
    elif request.method == 'GET':

        form.title.data = post.title
        form.content.data = post.content

    return render_template('create_post.html',title='Edit Post',
                form=form, legend ='Edit Post')


@posts.route('/post/<int:post_id>/delete',methods=["POST"])
@login_required
def delete_post(post_id):
     post = Post.query.get_or_404(post_id)
     if post.author != current_user:
        abort(403)
     db.session.delete(post)
     db.session.commit()
     flash('Your Post has been deleted !','success')
     return redirect(url_for('main.home'))
