from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user

from teacher import app, db
from teacher.forms import CreateForm, UpdateForm, RegistrationForm, LoginForm
from teacher.models import Words, User


@app.route("/")
@app.route("/home")
def home_page():
    quantity = len(Words.query.all())
    return render_template("home.html", title="My English Teacher", quantity=quantity)



@app.route("/create", methods=["GET", "POST"])
def create():
    form = CreateForm()
    if form.validate_on_submit() and current_user.is_authenticated: #Check if the method post
        word_to_add = Words(word=form.word.data,
                            translation=form.translation.data,
                            user_id=current_user.id)
        db.session.add(word_to_add)
        db.session.commit()
        return redirect(url_for("read"))
    return render_template("create.html", form=form, title="My English Teacher - Create")


@app.route("/read")
def read():
    if current_user.is_authenticated:
        data = Words.query.filter_by(user_id=current_user.id)
        return render_template("read.html", data=data, title="My English Teacher - Read")
    else:
        flash("You are not authenticated!", category="danger")
        return render_template("read.html")




@app.route("/update", methods=["GET", "POST"])
def update():
    form = UpdateForm()
    if form.validate_on_submit():
        update_word = Words.query.filter_by(id=request.args.get("id")).first()
        update_word.word = form.new_word.data
        update_word.translation = form.new_translation.data
        db.session.commit()
        return redirect(url_for("read"))
    else:
        return render_template("update.html", form=form, id=request.args.get("id"), title="My English Teacher - Update")



@app.route("/delete", methods=["GET", "POST"])
def delete():
    id = request.args.get("id")
    del_word = Words.query.filter_by(id=id).first()
    db.session.delete(del_word)
    db.session.commit()
    return redirect(url_for("read"))

@app.route("/registration", methods=["GET", "POST"])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_to_create = User(login=form.username.data,
                              email=form.email_adress.data,
                              password_hash=form.password_1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for("home_page"))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"There is the following error - {err_msg}", category="danger")

    return render_template("registration.html", form=form, title="My English Teacher - Registration")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user=User.query.filter_by(login=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f"Success! You are logged in as: {attempted_user.login}", category="success")
            return redirect(url_for("read"))
        else:
            flash("Username and password are not match! Plese try again", category="danger")

    return render_template("login.html", form=form, title="My English Teacher - Login")


@app.route("/logout")
def logout():
    logout_user()
    flash("You are successfully have logged out!", category="info")
    return redirect(url_for("home_page"))
