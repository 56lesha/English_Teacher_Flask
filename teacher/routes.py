from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user

from teacher import app, db
from teacher.forms import RegistrationForm, LoginForm, CreateCollectionForm, CreateWordForm
from teacher.models import Words, User, Collection


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html", title="My English Teacher")


@app.route("/create_collection", methods=["POST", "GET"])
def create_collection():
    form = CreateCollectionForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        category_to_add = Collection(name=form.name.data,
                                     description=form.description.data,
                                     user_id=current_user.id)

        db.session.add(category_to_add)
        db.session.commit()
        return redirect(url_for("read_collection"))
    return render_template("create_collection.html", form=form)


@app.route("/read_collection")
def read_collection():
    if current_user.is_authenticated:
        data = Collection.query.filter_by(user_id=current_user.id)
        return render_template("read_collection.html", data=data)
    else:
        flash("You are not authenticated!", category="danger")
        return render_template("read_collection.html")


@app.route("/update_collection", methods=["GET", "POST"])
def update_collection():
    form = CreateCollectionForm()
    if form.validate_on_submit():
        collection_to_update = Collection.query.filter_by(id=request.args.get("id")).first()
        collection_to_update.name = form.name.data
        collection_to_update.description = form.description.data
        db.session.commit()
        return redirect(url_for("read_collection"))
    collection_to_update = Collection.query.filter_by(id=request.args.get("id")).first()
    return render_template("update_collection.html", form=form, id=request.args.get("id"),
                           collection_to_update=collection_to_update)


@app.route("/delete_collection")
def delete_collection():
    words = db.session.query(Words).join(Collection, Words.collection_id == Collection.id). \
        filter(Collection.id == request.args.get("id"))
    [db.session.delete(word) for word in words]
    collection_to_delete = Collection.query.filter_by(id=request.args.get("id")).first()
    db.session.delete(collection_to_delete)
    db.session.commit()
    return redirect(url_for("read_collection"))


@app.route("/read_word/<id>")
def read_word(id):
    data = Words.query.filter_by(collection_id=id)
    return render_template("read_word.html", data_words=data, collection_id=id)


@app.route("/create_word", methods=["GET", "POST"])
def create_word():
    form = CreateWordForm()
    if form.validate_on_submit():
        collection_id = request.args.get("collection_id")
        word_to_add = Words(word=form.word.data,
                            translation=form.translation.data,
                            collection_id=collection_id)
        db.session.add(word_to_add)
        db.session.commit()
        return redirect(url_for("read_word", id=collection_id))
    return render_template("create_word.html", form=form, collection_id=request.args.get("collection_id"))


@app.route("/update_word/", methods=["GET", "POST"])
def update_word():
    form = CreateWordForm()
    if form.validate_on_submit():
        word_to_update = Words.query.filter_by(id=request.args.get("id")).first()
        word_to_update.word = form.word.data
        word_to_update.translation = form.translation.data
        db.session.commit()
        return redirect(url_for("read_word", id=request.args.get("collection_id")))
    word_to_update = Words.query.filter_by(id=request.args.get("id")).first()
    return render_template("update_word.html", form=form, id=request.args.get("id"),
                           collection_id=request.args.get("collection_id"), word_to_update=word_to_update)


@app.route("/delete_word", methods=["GET", "POST"])
def delete_word():
    id = request.args.get("id")
    collection_id = request.args.get("collection_id")
    del_word = Words.query.filter_by(id=id).first()
    db.session.delete(del_word)
    db.session.commit()
    return redirect(url_for("read_word", id=collection_id))


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
        attempted_user = User.query.filter_by(login=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f"Success! You are logged in as: {attempted_user.login}", category="success")
            return redirect(url_for("read_collection"))
        else:
            flash("Username and password are not match! Plese try again", category="danger")

    return render_template("login.html", form=form, title="My English Teacher - Login")


@app.route("/logout")
def logout():
    logout_user()
    flash("You are successfully have logged out!", category="info")
    return redirect(url_for("home_page"))
