from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Task

main_routes = Blueprint('main', __name__)

@main_routes.route('/')
def home():
    tasks = Task.query.all()
    return render_template('home.html', tasks=tasks)

@main_routes.route('/add-task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        new_task = Task(title=title, description=description)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('add_task.html')
