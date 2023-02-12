from flask import Flask, redirect, render_template, session, flash, request
from flask_bcrypt import Bcrypt
from models import db, User, RegisterUserForm, LoginForm


bcrypt = Bcrypt()

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
        pw_hash_utf8 = bcrypt.generate_password_hash(form.data['password']).decode("utf8")
        email = form.data['email']
        first_name = form.data['first_name']
        last_name = form.data['last_name']

        new_user = User(username = username,
                        password = pw_hash_utf8,
                        email = email,
                        first_name = first_name,
                        last_name = last_name)
        db.session.add(new_user)
        db.session.commit()

        return redirect(f'/users/{username}')
    else:
        return render_template('register.html', form = form)
    
@app.route('/login', methods=['GET','POST'])
def show_login_page():
    """Show Login Form"""

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(username = form.data['username']).first()

        if user and bcrypt.check_password_hash(user.password, form.data['password']):
            session['username'] = user.username
            flash(f"Welcome, {user.username}")
            return redirect(f'/users/{user.username}')
        elif not bcrypt.check_password_hash(user.password, form.data['password']):
            flash('Login Failed')
            return redirect('/login')

    else:
        if request.method=='POST':
            flash('Login Failed')
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
        return render_template('user_info.html', user = user)
    else:
        return redirect('/')