"""This file manages the administrators page. We define the administrator models here."""
from extensions import admin,db
from models import User, Book
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask import Blueprint, redirect, url_for,request,render_template, flash
from views import routes
from flask_login import current_user, login_user


bp=Blueprint("admin_bp",__name__)#Creating route for this accesspoint.

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return redirect(url_for("admin_bp.Manage"))

class UserModelView(ModelView):
    column_list=["email"]


@bp.route("/Manage", methods=["GET","POST"])
def Manage():
    """Administrators route. admin can register new books and enable registered users borrow books"""
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.get('admin@gmail.com')
        if user==email:
            if user.password==password:
                flash("Logged in successfully!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('admin'))
            else:
                """Password did not match the hash, access is denied with error message"""
                flash("Incorrect details. Try again.", category='error')
        else:
            """Email does not belong to the admin"""
            flash("You are not admin",category="error")
    return render_template("administrator.html",user=current_user)
admin.add_view(UserModelView(User,db.session))
admin.add_view(ModelView(Book,db.session))