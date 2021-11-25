
"""Here we define the model schema of our database, create tables and neccessary data entries that we expect.
we are implementing sql alchemy database engine to interact with the database. We are using cloud based mysql server to host our mysql database."""
from extensions import db
from flask_login import UserMixin


class User(db.Model,UserMixin):
    """User table that contins three columns and relationship the a back reference to the Book table.
    This class inherits some methods from UserMixin class."""
    __tablename__="user"
    id=db.Column(db.Integer, primary_key=True,autoincrement=True)
    email=db.Column(db.String(255),unique=True)
    password=db.Column(db.String(255))
    #borrower=db.Column(db.Boolean,nullable=False,default=True)
    borrowed = db.relationship('Book',backref="user", lazy="dynamic")

    def __init__(self,email,password):
        """Capturing instances of entries to be stored in the database."""
        self.email=email
        self.password=password

    def create(self):
        """Adding data to the database."""
        db.session.add(self)
        db.session.commit()
        return self

class Book(db.Model):
    """Book table in the database and it contains four columns and  a relationship to the user."""
    __tablename__="book"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    tag=db.Column(db.String(8),unique=True)
    bookname=db.Column(db.String(100))
    borrow=db.Column(db.Boolean,nullable=False,default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__(self,tag,bookname):
        """Capture instances of data entries to be stored in the database."""
        self.tag=tag
        self.bookname=bookname

    def create(self):
        """Add data to the database"""
        db.session.add(self)
        db.session.commit()
        return self
