import json
from flask import Blueprint,render_template, request, flash,redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,login_required,logout_user,current_user
from extensions import db
from models import User


routes=Blueprint('routes',__name__)#Creating instance of url routes blueprint

"""Displaying all results of borrowed books. 
Books that borrow columns are marked true in the database."""
def borrowed_books(user=User):
    selection=db.select(user).where(user.borrow==True)
    selected_data=json.dump(selection)
    display_data=json.load(selected_data)
    return  dispaly_data

@routes.route("/", methods=["POST","GET"])
@routes.route("/login/")
def login():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password,password):
                flash("Logged in successfully!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('home.html'))
            else:
                flash("Incorrect details. Try again.", category='error')
        else:
            flash("Email does not exist.", category="error")

    return render_template('index.html',user=current_user)

@routes.route("/sign_up",methods=["GET","POST"])
def sign_up():
    if request.method == 'POST':
        email=request.form.get('email')
        password1=request.form.get('password1')
        password2=request.form.get('password2')

        user=User.query.filter_by(email=email).first()
        if user:
            flash("Email exists.", category='error')
        elif len(email)<4:
            flash("Email must be greater than 4 characters.", category="error")
        elif len(password1)<7:
            flash("Password must contain more than 7 characters.", category="error")
        elif {'!','@','#','$','^','&','*'} | set(password1)==False:
            flash("Password is weak, include @,#,$,! characters",category='error')
        elif password1 != password2:
            flash("Passwords do not match.", category="error")
            '''elif user_name in User.query.filter_by(user_name=user_name):
            flash('Username already exists.',category='error')'''
        else:
            new_user = User(email=email,password=(generate_password_hash(password1,method='sha256')))
            db.session.add(new_user)
            db.session.commit()
            login_user(user=new_user, remember=True)

            flash("Account created!", category="success")
            return redirect(url_for('home.html'))
    return render_template('sign_up.html',user=current_user)

@routes.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('routes.login'))

@routes.route("/home",methods=["GET"])
def home():
    return render_template("home.html",user=current_user)

@routes.route("/admin", methods=["GET","POST"])
def admin():
    if request.method=='POST':
        usern=request.form.get('usern')
        bookn=request.form.get('bookn')
        borr=request.form.get('borr')
        tag=request.form.get('tag')
        bookname=request.form.get('bookname')

        user=User.query.filter_by(usern=usern).first()
        book=Book.query.filter_by(bookn=bookn).first()
        if not user | book:
            flash("Details do not exist", category="error")
        elif not borr==True:
            flash("Check if borrowed",category="error")
        elif (tag | bookname) =="":
            flash("Enter details",category="error")
        else:
            new_entry=Book(tag,bookname)
            db.session.add(new_entry)
            db.session.commit()
            return render_template("admin.html",user=current_user)
    return render_template('admin.html', user=current_user)