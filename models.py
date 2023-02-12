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
    
    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        pass


class RegisterUserForm(FlaskForm):
    """form for user info"""

    username = StringField("Username", validators=[Length(1, 20), InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email Address", validators=[Email(), InputRequired(),Length(max=50)])
    first_name = StringField("First Name", validators=[InputRequired(), Length(1,30)])
    lasts_name = StringField("Last Name", validators=[InputRequired(), Length(1,30)])

class LoginForm(FlaskForm):
    """login form"""

    username = StringField("Username", validators=[Length(1, 20), InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])