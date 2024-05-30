from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from models import User, Table, Order


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

users_bp = Blueprint('users', __name__)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.Integer, unique=True, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Available')

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'error')
        return redirect(url_for('login'))
    
    # Fetch the current user from the database based on the user_id stored in the session
    user = User.query.get(session['user_id'])
    
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful.', 'success')  # Add success message
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')  # Add error message
            return redirect(url_for('login'))
    return render_template('login.html')




@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Check if the email already exists in the database
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address already exists', 'error')  # Add error message
            return redirect(url_for('register'))

        # Create a new user and add it to the database
        new_user = User(email=email, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. Please login.', 'success')  # Add success message
            return redirect(url_for('login'))
        except:
            flash('An error occurred. Please try again.', 'error')  # Add error message
            return redirect(url_for('register'))
    
    return render_template('register.html')


@app.route('/manage_tables', methods=['GET', 'POST'])
def manage_tables():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        table_number = request.form['table_number']
        status = request.form['status']
        new_table = Table(table_number=table_number, status=status)
        db.session.add(new_table)
        db.session.commit()
        return redirect(url_for('manage_tables'))
    
    tables = Table.query.all()
    return render_template('manage_tables.html', tables=tables)

@app.route('/manage_orders', methods=['GET', 'POST'])
def manage_orders():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        table_id = request.form['table_id']
        description = request.form['description']
        new_order = Order(table_id=table_id, description=description)
        db.session.add(new_order)
        db.session.commit()
        return redirect(url_for('manage_orders'))
    
    orders = Order.query.all()
    for order in orders:
        order.table = Table.query.get(order.table_id)  # Fetch the associated table for each order
    tables = Table.query.all()
    return render_template('manage_orders.html', orders=orders, tables=tables)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.register_blueprint(users_bp)
    app.run(debug=True)
