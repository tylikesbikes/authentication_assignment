from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, Length, InputRequired

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(20),
                         primary_key = True,
                         unique = True)
    
    password = db.Column(db.Text,
                         nullable = False)
    
    email = db.Column(db.String(50),
                      nullable = False,
                      unique = True)
    
    first_name = db.Column(db.String(30),
                           nullable = False)
    
    last_name = db.Column(db.String(30),
                          nullable = False)
    
    feedback_posts = db.relationship('Feedback', backref='user')
    
    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Plan to add this as a class method later"""
        pass

    class Feedback(db.Model):
        __tablename__ = 'feedback'

        id = db.Column(db.Integer, autoincrement=True, primary_key = True)
        title = db.Column(db.String(100), nullable = False)
        content = db.Column(db.Text, nullable = False)
        username = db.Column(db.Text, db.ForeignKey('users.username'))




class RegisterUserForm(FlaskForm):
    """form for user info"""

    username = StringField("Username", validators=[Length(1, 20), InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email Address", validators=[Email(), InputRequired(),Length(max=50)])
    first_name = StringField("First Name", validators=[InputRequired(), Length(1,30)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(1,30)])

class LoginForm(FlaskForm):
    """login form"""

    username = StringField("Username", validators=[Length(1, 20), InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    """form for user feedback submission"""