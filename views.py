"""This file contains end points to access the library system through the web via sending various requests.
"""

import json
from flask import Blueprint,render_template, request, flash,redirect, url_for
from extensions import encrypt
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user,login_required,logout_user,current_user
from extensions import db
from models import User, Book


routes=Blueprint('routes',__name__)#Creating instance of url routes blueprint



@routes.route("/")
@routes.route("/login", methods=["POST","GET"])
def login():
    """Login route to enable registered user access the library system anywhere."""
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')


        user = User.query.filter_by(email=email).first()#Fetching email from the database.
        borr=Book.query.filter(Book.borrow==True)
        #books =User.query.filter(User.borrowed.any(Book.borrow==False))
        books=Book.query.filter(Book.borrow==False)
        if user:
            if check_password_hash(user.password,password):
                flash("Logged in successfully!", category='success')
                login_user(user, remember=True)
                return render_template("home.html",user=current_user,borr=borr,books=books)
            else:
                """Password did not match the hash, access is denied with error message"""
                flash("Incorrect details. Try again.", category='error')
        else:
            """Email was not found the database, the user is not registered."""
            flash("Email does not exist.", category="error")

    return render_template('index.html',user=current_user)

@routes.route("/sign_up",methods=["GET","POST"])
def sign_up():
    """This route register new users to the database of the library system by creating an account to the system."""
    if request.method == 'POST':
        email=request.form.get('email')
        password1=request.form.get('password1')
        password2=request.form.get('password2')

        user=User.query.filter_by(email=email).first()
        borr=Book.query.filter(Book.borrow==True) #to display borrowed books
        books=Book.query.filter(Book.borrow==False)#to diplay all books in the library
        if user:
            flash("Email exists.", category='error')
        elif len(email)<4:
            flash("Email must be greater than 4 characters.", category="error")
        elif len(password1)<7:
            flash("Password must contain more than 7 characters.", category="error")
        elif ('!' or '@' or '#' or '$' or '^' or '&' or'*') not in set(password1):
            flash("Password is weak, include @,#,$,! characters",category='error')
        elif password1 != password2:
            flash("Passwords do not match.", category="error")
        else:
            new_user = User(email=email,password=(generate_password_hash(password1)))
            db.session.add(new_user)
            db.session.commit()
            login_user(user=new_user, remember=True)

            flash("Account created!", category="success")
            return render_template("home.html",user=current_user,borr=borr, books=books)
    return render_template('sign_up.html',user=current_user)

@routes.route('/logout')
def logout():
    """Logs out the user from the session. after he is done."""
    logout_user()
    return redirect(url_for('routes.login'))

