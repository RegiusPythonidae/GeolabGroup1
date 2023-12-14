from extensions import db, app, login_manager
from random import randint

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class BaseModel:
    def create(self):
        db.session.add(self)
        db.session.commit()

    def save(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class User(db.Model, BaseModel, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String)

    def __init__(self, username, password, role="guest"):
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role

    def check_password(self, password):
        return check_password_hash(self.password, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Product(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.ForeignKey("product_category.id"))
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    img = db.Column(db.String)

    category = db.relationship("ProductCategory")


class ProductCategory(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    products = db.relationship("Product")


if __name__ == "__main__":
    products = [
        {"name": "Playstation 5", "price": 1600, "img": "PS5.jpg", "id": 0},
        {"name": "HP Omen", "price": 1200, "img": "laptop3.jpg", "id": 1},
        {"name": "Lenovo", "price": 1400, "img": "laptop2.jpg", "id": 2},
        {"name": "Microsoft Surface", "price": 1500, "img": "laptop.jpg", "id": 3},
        {"name": "Playstation 5", "price": 1600, "img": "PS5.jpg", "id": 0},
        {"name": "HP Omen", "price": 1200, "img": "laptop3.jpg", "id": 1},
        {"name": "Lenovo", "price": 1400, "img": "laptop2.jpg", "id": 2},
        {"name": "Microsoft Surface", "price": 1500, "img": "laptop.jpg", "id": 3},
        {"name": "Playstation 5", "price": 1600, "img": "PS5.jpg", "id": 0},
        {"name": "HP Omen", "price": 1200, "img": "laptop3.jpg", "id": 1},
        {"name": "Lenovo", "price": 1400, "img": "laptop2.jpg", "id": 2},
        {"name": "Microsoft Surface", "price": 1500, "img": "laptop.jpg", "id": 3},
        {"name": "Playstation 5", "price": 1600, "img": "PS5.jpg", "id": 0},
        {"name": "HP Omen", "price": 1200, "img": "laptop3.jpg", "id": 1},
        {"name": "Lenovo", "price": 1400, "img": "laptop2.jpg", "id": 2},
        {"name": "Microsoft Surface", "price": 1500, "img": "laptop.jpg", "id": 3},
        {"name": "Playstation 5", "price": 1600, "img": "PS5.jpg", "id": 0},
        {"name": "HP Omen", "price": 1200, "img": "laptop3.jpg", "id": 1},
        {"name": "Lenovo", "price": 1400, "img": "laptop2.jpg", "id": 2},
        {"name": "Microsoft Surface", "price": 1500, "img": "laptop.jpg", "id": 3},
    ]
    with app.app_context():
        db.create_all()

        for product in products:
            new_product = Product(name=product["name"] + str(randint(1, 100000)), price=product["price"], img=product["img"], category_id=1)
            new_product.create()

        admin_user = User(username="admin_user", password="password123", role="admin")
        admin_user.create()
