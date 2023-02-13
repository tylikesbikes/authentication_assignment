from flask import Flask, redirect, render_template, session, flash, request
from models import db, User, RegisterUserForm, LoginForm, FeedbackForm, Feedback

app = Flask(__name__)

app.config['SECRET_KEY'] = 'keeta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///authentication'


db.app = app
db.init_app(app)
app.app_context().push()

db.create_all()


@app.route('/', methods=['GET'])
def base_route():
    """Base route, redirect to /register"""

    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def show_register_page():
    """Show register form"""

    

    form = RegisterUserForm()

    if form.validate_on_submit():
        username = form.data['username']
        User.register(form.data['username'],
                      form.data['password'],
                      form.data['email'],
                      form.data['first_name'],
                      form.data['last_name'])
        session['username'] = username

        return redirect(f'/users/{username}')
    elif session.get('username', None):
        return redirect(f"/users/{session['username']}")
    else:
        return render_template('register.html', form = form)
    
@app.route('/login', methods=['GET','POST'])
def show_login_page():
    """Show Login Form"""

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(username = form.data['username']).first()


        if User.authenticate_user(user.username, form.data['password']):
            session['username'] = user.username
            flash(f"Welcome, {user.username}")
            return redirect(f'/users/{user.username}')

        else:
            flash('Login Failed')
            return redirect('/login')

    elif request.method=='POST':
        flash('Login Failed')
        return render_template('login.html', form = form)
    else:
        if session.get('username',None):
            return redirect(f"/users/{session['username']}")
        return render_template('login.html', form = form)
    
@app.route('/logout', methods=['GET'])
def logout():
    """Log User Out"""

    session.pop('username')
    flash("You have successfully logged out")
    return redirect('/')

@app.route('/users/<string:username>')
def logged_in(username):
    """For a logged in user, show user details.
    If not logged in, redirect to /"""
    
    if session.get('username',None):
        user = User.query.filter_by(username = username).first()
        feedback = user.feedback_posts
        return render_template('user_info.html', user = user, feedback = feedback)
    else:
        return redirect('/')
    
@app.route('/feedback/<int:feedback_id>/update', methods=['GET','POST'])
def update_feedback(feedback_id):
    """show form to edit feedback"""

    feedback = Feedback.query.get_or_404(feedback_id)
    feedback_creator = feedback.username
    user = User.query.filter_by(username = feedback_creator)
    if session['username'] != feedback_creator:
        flash("You don't have permission to edit this post")
        return redirect('/')
    
    form = FeedbackForm(obj=feedback)
    

    if form.validate_on_submit(): #update existing feedback
        feedback.title = form.data['title']
        feedback.content = form.data['content']

        db.session.add(feedback)
        db.session.commit()

        return redirect(f'/users/{feedback_creator}')
    
    return render_template('edit_feedback.html', form = form, user = user, feedback = feedback)

@app.route('/users/<string:username>/feedback/add', methods=['GET','POST'])
def add_feedback(username):
    """Show form to delete this user or add feedback"""

    user = User.query.filter_by(username = username).first()
    logged_in_user = session.get('username', None)

    if user.username != logged_in_user:
        flash("You don't have permission to add feedback for that user")
        return redirect(f'/users/{user.username}')
    else:
        form = FeedbackForm()

        if form.validate_on_submit():
            new_feedback=Feedback(title = form.data['title'],
                                  content = form.data['content'],
                                  username = user.username)
            db.session.add(new_feedback)
            db.session.commit()

            return redirect(f'/users/{username}'), 201
        else:
            return render_template('add_feedback.html', form = form, user = user)

@app.route('/users/<string:username>/delete', methods=['POST'])
def delete_user(username):
    """delete user if correct user is logged in"""

    user = User.query.filter_by(username = username).first()
    if user.username and user.username == session['username']:
        db.session.delete(user)
        db.session.commit()

        session.pop('username')
        flash("User Deleted")

        return redirect('/')
    else:
        flash("Either you don't have permission to delete this user, or the given username doesn't exist")
        return redirect('/')
    
@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    """Delete feedback and redirect to the page of its original creator"""

    feedback = Feedback.query.get_or_404(feedback_id)
    logged_in_user = session['username']
    if logged_in_user == feedback.username:
        db.session.delete(feedback)
        db.session.commit()

        flash("Successfully deleted")

        return redirect(f'/users/{logged_in_user}')

    else:
        flash("You don't have permission to delete that")
        return redirect('/')