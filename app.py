from flask import Flask, render_template, request, redirect, url_for, session, abort
from flask_sqlalchemy import SQLAlchemy
import hashlib
import os
from db import db
from db.models import User, Product, Cart
from os import path

app = Flask(__name__)


app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

if app.config['DB_TYPE'] == 'postgres':
    db_name = 'rgz_db_orm'
    db_user = 'rgz_db_orm'
    db_password = '123'
    host_ip = '127.0.0.1'
    host_port = 5432

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "rgz_db_orm.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db.init_app(app)


# Вспомогательная функция для проверки авторизации
def get_current_user():
    if 'user_id' not in session:
        abort(403)  # Доступ запрещен
    return User.query.get(session['user_id'])


@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.password == hash_password(password):
            session['user_id'] = user.id
            return redirect(url_for('index'))

        return render_template('login.html', error='Неверное имя пользователя или пароль')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            return render_template('register.html', error='Пользователь с таким именем уже существует')

        user = User(username=username, password=hash_password(password))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route('/cart')
def cart():
    user = get_current_user()
    cart_items = db.session.query(Cart, Product).join(Product).filter(Cart.user_id == user.id).all()
    return render_template('cart.html', cart_items=cart_items)


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    user = get_current_user()
    cart_item = Cart.query.filter_by(user_id=user.id, product_id=product_id).first()

    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = Cart(user_id=user.id, product_id=product_id, quantity=1)
        db.session.add(cart_item)

    db.session.commit()
    return redirect(url_for('cart'))


@app.route('/remove_from_cart/<int:cart_item_id>', methods=['POST'])
def remove_from_cart(cart_item_id):
    user = get_current_user()
    cart_item = Cart.query.filter_by(id=cart_item_id, user_id=user.id).first()

    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()

    return redirect(url_for('cart'))


@app.route('/checkout')
def checkout():
    user = get_current_user()
    cart_items = Cart.query.filter_by(user_id=user.id).all()
    total = sum(Product.query.get(item.product_id).price * item.quantity for item in cart_items)

    Cart.query.filter_by(user_id=user.id).delete()
    db.session.commit()

    return render_template('checkout.html', total=total)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


if __name__ == '__main__':
    app.run(debug=True, port=5001)
