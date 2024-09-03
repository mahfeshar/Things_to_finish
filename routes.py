from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Task

main_routes = Blueprint('main', __name__)

@main_routes.route('/')
def home():
    return render_template('home.html')

@main_routes.route('/pending-tasks')
def pending_tasks():
    tasks = Task.query.filter_by(completed=False).all()
    return render_template('pending_tasks.html', tasks=tasks)

@main_routes.route('/completed-tasks')
def completed_tasks():
    tasks = Task.query.filter_by(completed=True).all()
    return render_template('completed_tasks.html', tasks=tasks)

@main_routes.route('/add-task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        new_task = Task(title=title, description=description)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('main.pending_tasks'))
    return render_template('add_task.html')

@main_routes.route('/complete-task/<int:task_id>')
def complete_task(task_id):
    task = Task.query.get(task_id)
    task.completed = not task.completed  # Toggle the completed status
    db.session.commit()
    return redirect(url_for('main.pending_tasks'))
