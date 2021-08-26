import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request,abort

from Package import app, db, bcrypt, mail 
from Package.forms import (RegistrationForm, LoginForm, UpdateAccountForm,PostForm, 
                            RequestResetForm, ResetPasswordForm)
from Package.models import User,Post
from flask_login import login_user, current_user,logout_user,login_required
from flask_mail import Message 


@app.route("/")
@app.route("/home")
def home():
    # posts = Post.query.all()
    page = request.args.get("page",1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=7)
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


# --------------------------------------------------------------------
# specify what request does this route accepts(in case of signup we
# are making POST request to same route)
# --------------------------------------------------------------------


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash(f"You're already registered!")
        return redirect(url_for('home'))

    Register_form = RegistrationForm()

    if Register_form.validate_on_submit():
        # create the user into the database
        hashed_password = bcrypt.generate_password_hash(Register_form.password.data).decode('utf-8')
        user = User(username=Register_form.username.data, email= Register_form.email.data,
                    password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(
            f"Congatulations! { Register_form.username.data } You can Login now !",
            "success",
        )
        return redirect(url_for("login"))

    return render_template("register.html", title="Register", form=Register_form)


@app.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        flash(f"You're Logged in !")
        return redirect(url_for('home'))
        
    Login_form = LoginForm()
    if Login_form.validate_on_submit():
            user = User.query.filter_by(email=Login_form.email.data).first()

            if user and bcrypt.check_password_hash(user.password, Login_form.password.data) :
                login_user(user,remember = Login_form.remember.data)
                # check for account redirection
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else :
                flash(f"Login Unsuccessfull! Incorrect email & password combination", "danger")

    return render_template("login.html", title="Login", form=Login_form)

  # ----------------------------------------------
     # says a success kind of flash msg from flask(bootstrap class)
    # goto layout to display this flash alerts
    # ----------------------------------------------

@app.route('/logout')
def logout():
    logout_user()
    flash(f'logged out successfully!')

    return redirect(url_for('home'))


def save_picture(form_picture):
    
    random_hex = secrets.token_hex(8)
    f_name,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex+f_ext
    picture_path = os.path.join(app.root_path, 'static/images/profile_pics',picture_fn)
    
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    
    i.save(picture_path)

    return picture_fn



@app.route('/account',methods=["POST","GET"])
@login_required
def account():
    updateForm = UpdateAccountForm()
    if updateForm.validate_on_submit():
        # profile pic updation
        if updateForm.picture.data:

            picture_file = save_picture(updateForm.picture.data)
            current_user.image_file = picture_file
        # sqlalchemy allows it with ease just rename it
        current_user.username = updateForm.username.data
        current_user.email = updateForm.email.data
        db.session.commit()
        flash(f'Account updated !','success')
        return redirect(url_for('account')) # a get request rather than rendering again(post request)
        # conform from resubmission is avoided using redirection

    elif request.method == 'GET':
        updateForm.username.data = current_user.username
        updateForm.email.data = current_user.email
    
    image_file = url_for('static',filename='images/profile_pics/'+ current_user.image_file)
    return render_template('account.html',title='Account',image_file=image_file,form=updateForm) 
    

    # Pillow package is for resizing the images so that we dont send large
    # images to our site(makes sites slow) and no implicit resizing takes place

@app.route('/post/new',methods=["POST","GET"])
@login_required
def new_post():
    postform = PostForm()

    if postform.validate_on_submit():
        # add to database
         post = Post(title=postform.title.data, content =postform.content.data, author=current_user)
         db.session.add(post)
         db.session.commit()

         flash('Your Post has been created !','success')
         return redirect(url_for('home'))

    return render_template("create_post.html", title="New Post",
     form = postform, legend ='New Post')



@app.route('/post/<int:post_id>',methods=["POST","GET"])
def post(post_id):

    # post = Post.query.get(post_id)
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title,post=post)


@app.route('/post/<int:post_id>/update',methods=["POST","GET"])
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
        return redirect(url_for('post',post_id = post.id))
    elif request.method == 'GET':

        form.title.data = post.title
        form.content.data = post.content

    return render_template('create_post.html',title='Edit Post',
                form=form, legend ='Edit Post')


@app.route('/post/<int:post_id>/delete',methods=["POST"])
@login_required
def delete_post(post_id):
     post = Post.query.get_or_404(post_id)
     if post.author != current_user:
        abort(403)
     db.session.delete(post)
     db.session.commit()
     flash('Your Post has been deleted !','success')
     return redirect(url_for('home'))


@app.route("/user/<string:username>/")
def user_posts(username):
    page = request.args.get("page",1,type=int)
    user = User.query.filter_by(username=username).first_or_404()

    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=7)
    return render_template("user_posts.html", posts=posts,user = user)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', 
                    sender='noreply@gmail.com', 
                    recipients=[user.email])    
    msg.subject = "Reset Your Password"
    msg.body = f''' To reset the password visit the following link :
                {url_for('reset_token',token=token,_extenal=True)}

                If you didn't make this request simply ignore! No changes will be made 
                to your account!
                '''
    mail.send(msg)



@app.route('/reset_password',methods=["POST","GET"])
def reset_request():
    # make sure they are logged out while accessing this route
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instuctions to reset your password ! ','info')
        return redirect(url_for('login'))

    return render_template('reset_request.html', title='Reset Password',form=form)



@app.route('/reset_password/<token>',methods=["POST","GET"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    user = User.verify_reset_token(token)
    # if we don't a user here that means either token has expired
    # or user is invalid
    if user is None:
        flash('Invalid or Expired token','warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f"{ form.username.data } your Password has been updated!",
            "success",)
        return redirect(url_for("login"))

    return render_template('reset_token.html', title='Reset Password',form=form)

