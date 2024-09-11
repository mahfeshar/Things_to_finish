from flask import Blueprint, render_template, redirect, url_for, request, flash
from models import db, User, Task
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Blueprints
main_routes = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)

# Home route
@main_routes.route('/')
def home():
    return render_template('index.html')

# Pending tasks route (requires user to be logged in)
@main_routes.route('/pending-tasks')
@login_required
def pending_tasks():
    tasks = Task.query.filter_by(completed=False, user_id=current_user.id).all()
    return render_template('pending_tasks.html', tasks=tasks)

# Completed tasks route (requires user to be logged in)
@main_routes.route('/completed-tasks')
@login_required
def completed_tasks():
    tasks = Task.query.filter_by(completed=True, user_id=current_user.id).all()
    return render_template('completed_tasks.html', tasks=tasks)

# Add task route (requires user to be logged in)
@main_routes.route('/add-task', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        
        # Create the new task with the current user's id
        new_task = Task(title=title, description=description, user_id=current_user.id)
        
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully.')
        return redirect(url_for('main.pending_tasks'))
    
    return render_template('add_task.html')

# Complete task (toggle task completion)
@main_routes.route('/complete-task/<int:task_id>')
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)  # Ensure task exists
    if task.user_id != current_user.id:
        flash('You are not authorized to complete this task.')
        return redirect(url_for('main.pending_tasks'))

    task.completed = not task.completed  # Toggle the completed status
    db.session.commit()
    flash('Task updated successfully.')
    return redirect(url_for('main.pending_tasks'))

# Register route
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if the username or email already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists. Please choose a different one.')
            return redirect(url_for('auth.register'))
        
        # If username and email are unique, create a new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

# Login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user is None or not user.check_password(password):
            flash('Invalid email or password.')
            return redirect(url_for('auth.login'))

        login_user(user)
        return redirect(url_for('main.home'))  # Redirect to the home page
    
    return render_template('login.html')

# Logout route
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))
