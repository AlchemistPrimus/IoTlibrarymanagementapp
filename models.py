from extensions import db 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length
from flask_login import UserMixin
from sqlalchemy.sql import func

class Book(db.Model):
    __tablename__="book"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    tag=db.Column(db.String(8),unique=True)
    bookname=db.Column(db.String(20))
    borrow=db.Column(db.Boolean,nullable=False,default=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))

    def __init__(self,tag,bookname):
        self.tag=tag
        self.bookname=bookname

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

class User(db.Model,UserMixin):
    __tablename__="user"
    id=db.Column(db.Integer, primary_key=True,autoincrement=True)
    email=db.Column(db.String(20),unique=True)
    password=db.Column(db.String(20))
    borrowed=db.relationship('Book')

    def __init__(self,email,password):
        self.email=email
        self.password=password

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class RegisterForms(FlaskForm):
    email=StringField("Enter email",validators=[InputRequired("Enter email"),Length(max=20,message="email cannot be more than 20 characters")])
    password=PasswordField('Enter password',validators=[InputRequired('Enter password'),Length(min=8, message="password cannot be less than 8 characters")])

