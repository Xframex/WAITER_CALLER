from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate  # Import Flask-Migrate
from models import User, Table, Order
#from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = '_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate
bcrypt = Bcrypt(app)
#csrf = CSRFProtect(app)

users_bp = Blueprint('users', __name__)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.Integer, unique=True, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200), nullable=True)  # Ensure this column exists

    def __init__(self, table_number, status, description=None):
        self.table_number = table_number
        self.status = status
        self.description = description

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    table = db.relationship('Table', backref=db.backref('orders', lazy=True))

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'error')
        return redirect(url_for('login'))
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
            flash('Login successful.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address already exists', 'error')
            return redirect(url_for('register'))
        new_user = User(email=email, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. Please login.', 'success')
            return redirect(url_for('login'))
        except:
            flash('An error occurred. Please try again.', 'error')
            return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/manage_tables', methods=['GET', 'POST'])
def manage_tables():
    if 'user_id' not in session:
        flash('Please log in to manage tables.', 'error')
        return redirect(url_for('login'))
    if request.method == 'POST':
        table_number = request.form['table_number']
        status = request.form['status']
        description = request.form.get('description')
        new_table = Table(table_number=table_number, status=status, description=description)
        db.session.add(new_table)
        db.session.commit()
        flash('Table added successfully.', 'success')
        return redirect(url_for('manage_tables'))
    tables = Table.query.all()
    return render_template('manage_tables.html', tables=tables)

@app.route('/delete_table/<int:table_id>', methods=['POST'])
def delete_table(table_id):
    table = Table.query.get_or_404(table_id)
    # Update associated orders to set table_id to null
    Order.query.filter_by(table_id=table_id).update({'table_id': None})
    db.session.delete(table)
    db.session.commit()
    flash('Table deleted successfully.', 'success')
    return redirect(url_for('manage_tables'))






@app.route('/edit_table/<int:table_id>', methods=['GET', 'POST'])
def edit_table(table_id):
    table = Table.query.get_or_404(table_id)
    if request.method == 'POST':
        table.table_number = request.form['table_number']
        table.status = request.form['status']
        table.description = request.form.get('description')
        db.session.commit()
        flash('Table updated successfully.', 'success')
        return redirect(url_for('manage_tables'))
    return render_template('edit_table.html', table=table)

@app.route('/manage_orders', methods=['GET', 'POST'])
def manage_orders():
    if 'user_id' not in session:
        flash('Please log in to manage orders.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        table_id = request.form['table_id']
        description = request.form['description']
        new_order = Order(table_id=table_id, description=description, status='Pending')
        db.session.add(new_order)
        db.session.commit()
        flash('Order added successfully.', 'success')
        return redirect(url_for('manage_orders'))

    filter_status = request.args.get('filter_status')
    if filter_status:
        orders = Order.query.filter_by(status=filter_status).all()
    else:
        orders = Order.query.all()

    tables = Table.query.all()
    return render_template('manage_orders.html', orders=orders, tables=tables)

@app.route('/clear_tables', methods=['POST'])
def clear_tables():
    if 'user_id' not in session:
        flash('Please log in to perform this action.', 'error')
        return redirect(url_for('login'))
    
    # Check if there are any existing orders associated with tables
    existing_orders = Order.query.count()
    if existing_orders > 0:
        flash('Cannot clear tables with existing orders. Please resolve or delete all orders first.', 'error')
    else:
        # Drop all tables from the database
        db.drop_all()
        # Recreate all tables
        db.create_all()
        flash('All tables cleared successfully.', 'success')
    
    return redirect(url_for('manage_tables'))




@app.route('/resolve_order/<int:order_id>', methods=['POST'])
def resolve_order(order_id):
    new_status = request.form['status']
    order = Order.query.get(order_id)
    if order:
        order.status = new_status
        db.session.commit()
    return redirect(url_for('manage_orders'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.register_blueprint(users_bp)
    app.run(debug=True)
