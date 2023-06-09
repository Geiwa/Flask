from flask import Flask, render_template, request, flash, redirect, url_for, current_app
from flask_sqlalchemy import SQLAlchemy
import os 
from flask import Flask
from flask_login import logout_user, login_required, LoginManager, login_user, UserMixin, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nfkjdngkjnewlkngrewlkgu438u59843u59843u985u93htjfknsfkjdsnfkjes'

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
    

# Определение модели User
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

    def repr(self):
        return self.username

# Определение модели Product
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
   

# Определение формы для создания продукта


# with app.app_context():
#     db.create_all()
    


@app.route('/')
def index():
    # product = Product.query.order_by(Product.id).all()
    product = Product.query.all()

    return render_template('blog/index.html', data=product)

@app.route('/about')
def about():
    return render_template('blog/about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Проверяем логин и пароль
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)

            flash('Вход выполнен успешно!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неверный логин или пароль', 'danger')

    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']


        hash = generate_password_hash(password=password)
        # Проверяем, не занят ли выбранный логин

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash('Логин уже занят', 'danger')
        else:
            # Создаем нового пользователя
            new_user = User(username=username, password=hash)
            db.session.add(new_user)
            db.session.flush()
            db.session.commit()
            flash('Регистрация успешна. Вы можете войти.', 'success')
            return redirect(url_for('login'))

    return render_template('auth/register.html')

@app.route('/create_product', methods=['GET', 'POST'])
def create_product():
    if request.method == 'POST':
        try:
            # if form.validate_on_submit():
                name = request.form.get('name')
                description = request.form.get('description')
                price = request.form.get("price")
             
                product = Product(name=name, description=description, price=price)
                db.session.add(product)
                db.session.flush()
                db.session.commit()
                flash('Продукт успешно создан', 'success')
                return redirect(url_for('index'))  # Redirect to the home page
        except:
            db.session.rollback()
            print("Error")

    return render_template('logic/create_product.html')
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")
@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('blog/products.html', products=products)












