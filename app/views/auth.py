from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import login_required, login_user, logout_user, current_user
from app.models import db, User, OAuth
from app.forms import RegisterForm, LoginForm, SetPasswordForm


blueprint = Blueprint("auth", __name__)


@blueprint.route("/register", methods=("GET", "POST"))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = form.create_user()
        if user:
            login_user(user)
            flash("Account created")
            return redirect(url_for("main.index"))
    return render_template("register.j2", form=form)


@blueprint.route("/login", methods=("GET", "POST"))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.get_user()
        if user:
            login_user(user)
            flash("You have logged in")
            return redirect(url_for("main.index"))
    return render_template("login.j2", form=form)


@blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for("main.index"))


@blueprint.route("/set_password", methods=("GET", "POST"))
@login_required
def set_password():
    form = SetPasswordForm()
    if form.validate_on_submit():
        current_user.password = form.password.data
        db.session.add(current_user)
        db.session.commit()
        flash("Password set successfully")
        return redirect(url_for("main.index"))
    return render_template("set_password.j2", form=form)


@blueprint.route("/merge", methods=("GET", "POST"))
@login_required
def merge():
    form = LoginForm(data={"username": request.args.get("username")})
    if form.validate_on_submit():
        user = form.get_user()
        if user:
            if user != current_user:
                merge_users(current_user, user)
                flash(
                    "User {username} has been merged into your account".format(
                        username=user.username
                    )
                )
                return redirect(url_for("main.index"))
            else:
                form.username.errors.append("Cannot merge with yourself")
    return render_template("merge.j2", form=form)


def merge_users(merge_into, merge_from):
    assert merge_into != merge_from
    OAuth.query.filter_by(user=merge_from).update({OAuth.user: merge_into})
    db.session.delete(merge_from)
    db.session.commit()
    return merge_into
