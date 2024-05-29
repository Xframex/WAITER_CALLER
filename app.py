from flask import Flask, render_template, request, redirect, url_for, Blueprint

app = Flask(__name__)
users_bp = Blueprint('users', __name__)

users = {
    'test@example.com': 'password123'
}

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email] == password:
            # Dummy authentication (replace with proper authentication logic)
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid email or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Dummy registration (replace with proper registration logic)
        users[email] = password
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/manage_tables')
def manage_tables():
    # Your view function logic here
    return render_template('manage_tables.html')

@app.route('/manage_orders')
def manage_orders():
    # Your logic here
    return render_template('manage_orders.html')

@app.route('/logout')
def logout():
    # Logic to logout the user
    return redirect(url_for('home'))  # Redirect to the home page after logout


if __name__ == '__main__':
    app.register_blueprint(users_bp)  # Register the users Blueprint
    app.run(debug=True)
