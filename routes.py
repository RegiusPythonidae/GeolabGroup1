from flask import Flask, render_template, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from os import path

from forms import AddProductForm, RegisterForm, LoginForm
from extensions import app, db
from models import Product, ProductCategory, User


@app.route("/")
def home():
    products = Product.query.paginate(per_page=8, page=1)
    return render_template("index.html", products=products)


@app.route("/page/<int:page_id>")
def page(page_id):
    products = Product.query.paginate(per_page=3, page=page_id)
    return render_template("index.html", products=products, page_id=page_id)

@app.route("/category/<int:category_id>")
def category(category_id):
    products = Product.query.filter(Product.category_id == category_id).all()
    return render_template("index.html", products=products)


@app.route("/search/<string:name>")
def search(name):
    products = Product.query.filter(Product.name.ilike(f"%{name}%"))
    return render_template("search_results.html", products=products)


@app.route("/view_product/<int:product_id>")
def view_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return render_template("404.html")
    return render_template("product.html", product=product)


@app.route("/add_product", methods=["GET", "POST"])
@login_required
def add_product():
    if current_user.role != "admin":
        return redirect("/")

    form = AddProductForm()

    if form.validate_on_submit():
        file = form.img.data
        filename = file.filename
        file.save((path.join(app.root_path, 'static', filename)))

        new_product = Product(name=form.name.data, price=form.price.data, img=filename)
        new_product.create()

        flash("პროდუქტი დაემატა")
        return redirect("/")

    return render_template("add_product.html", form=form)


@app.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    if current_user.role != "admin":
        return redirect("/")

    product = Product.query.get(product_id)
    if not product:
        return render_template("404.html")

    form = AddProductForm(name=product.name, price=product.price, img=product.img)
    if form.validate_on_submit():
        file = form.img.data
        filename = file.filename
        file.save((path.join(app.root_path, 'static', filename)))

        product.name = form.name.data
        product.price = form.price.data
        product.img = filename

        db.session.commit()

    return render_template("add_product.html", form=form)


@app.route("/delete_product/<int:product_id>")
@login_required
def delete_product(product_id):
    if current_user.role != "admin":
        return redirect("/")

    product = Product.query.get(product_id)
    if not product:
        return render_template("404.html")

    product.delete()

    flash("პროდუქტი წაიშალა")
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        existing_user = User.query.filter(User.username == form.username.data).first()
        if existing_user:
            flash("სახელი უკვე გამოყენებულია")
        else:
            user = User(username=form.username.data, password=form.password.data)
            user.create()
            flash("თქვენ წარმატებით გაიარეთ რეგისტრაცია")
            return redirect("/")
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    # form.username.data
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("თქვენ წარმატებით გაიარეთ ავტორიზაცია")
            return redirect("/")
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash("წარმატებულად გამოხვედით აქოუნტიდან")
    return redirect("/")


@app.route("/about_us")
def about():
    return render_template("about.html")