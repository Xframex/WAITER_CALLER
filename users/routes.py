from flask import Blueprint, render_template, request, redirect, url_for, session

users_bp = Blueprint('users', __name__)

# Dummy user data (replace with database integration)
users = {
    'test@example.com': {'password': 'password123', 'role': 'manager'}
}

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email]['password'] == password:
            # Set session variables
            session['email'] = email
            session['role'] = users[email]['role']
            return redirect(url_for('users.dashboard'))
        else:
            error = 'Invalid email or password'
            return render_template('login.html', error=error)
    return render_template('login.html')

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email not in users:
            # Add new user to the dictionary
            users[email] = {'password': password, 'role': 'patron'}
            # Set session variables
            session['email'] = email
            session['role'] = 'patron'
            return redirect(url_for('users.dashboard'))
        else:
            error = 'Email already exists'
            return render_template('register.html', error=error)
    return render_template('register.html')

@users_bp.route('/dashboard')
def dashboard():
    if 'email' in session:
        email = session['email']
        user = users[email]
        if user['role'] == 'patron':
            # Retrieve patron-specific data (e.g., current orders, table status)
            # Render template with patron-specific data
            return render_template('patron_dashboard.html', user=user)
        elif user['role'] == 'manager':
            # Retrieve manager-specific data (e.g., analytics, employee management tools)
            # Render template with manager-specific data
            return render_template('manager_dashboard.html', user=user)
    else:
        return redirect(url_for('users.login'))

@users_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('users.login'))
