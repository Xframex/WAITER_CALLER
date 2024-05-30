# Waiter Caller

Waiter Caller is a Flask web application designed to help manage tables and orders in a restaurant. The application allows users to register, log in, and manage tables and orders effectively.

## Features

- **User Authentication**: Registration and login functionality with hashed passwords.
- **Table Management**: View and update the status of tables.
- **Order Management**: Add and resolve orders, associate orders with tables.

## Requirements

- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-Bcrypt

## Setup Instructions

### Clone the Repository

```bash
git clone https://github.com/yourusername/waWAITER_CALLER.git
cd WAITER_CALLER

# Create and Activate a Virtual Environment
python -m venv venv

source venv/bin/activate   # On Windows use `venv\Scripts\activate`

pip install -r requirements.txt

# Set Up the Database

flask db init
flask db migrate -m "Initial migration"
flask db upgrade
flask run


Application Structure
app.py: The main Flask application file where routes and application logic are defined.
models.py: Contains SQLAlchemy models for the application.
templates/: Directory containing HTML templates for rendering views.
static/: Directory for static files like CSS, JavaScript, and images.
Usage
User Authentication
Register: Navigate to /register to create a new user account.
Login: Navigate to /login to log into an existing account.
Dashboard: Once logged in, users can access the dashboard at /dashboard.
Table Management
Manage Tables: Navigate to /manage_tables to view and update table statuses, and to add new tables.
Order Management
Manage Orders: Navigate to /manage_orders to view, add, and resolve orders.
Resolve Order: Change the status of an order from 'Pending' to 'Completed'.
Code Overview
Models
User: Represents a user with an email and hashed password.
Table: Represents a table with a number, status, and optional description.
Order: Represents an order associated with a table, containing a description and status.
Routes
/: Home page.
/dashboard: Dashboard for logged-in users.
/login: User login page.
/register: User registration page.
/manage_tables: Page to manage tables.
/manage_orders: Page to manage orders.
/resolve_order/<int:order_id>: Endpoint to resolve an order.
Templates
base.html: Base template extended by other templates.
home.html: Home page template.
login.html: Login page template.
register.html: Registration page template.
dashboard.html: Dashboard template for logged-in users.
manage_tables.html: Template for managing tables.
manage_orders.html: Template for managing orders.



