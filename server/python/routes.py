import logging
from flask import render_template, request, redirect, url_for, flash, jsonify
from server.python.database.db_manager import load_tasks, add_task, update_task, delete_task, mark_task
from server.python.database.model import validate_task_description, validate_priority

logger = logging.getLogger(__name__)

def register_routes(app):
    """Register all Flask routes with the app."""

    @app.route('/')
    def index():
        logger.info("Rendering index page")
        try:
            tasks = load_tasks()
            return render_template('index.html', tasks=tasks)
        except Exception as e:
            logger.error(f"Error loading tasks: {e}")
            flash('An error occurred while loading tasks.', 'error')
            return render_template('index.html', tasks=[])

    @app.route('/add', methods=['POST'])
    def add():
        description = request.form.get('description')
        priority = request.form.get('priority', 'Medium')  # Default to Medium

        # Validate description
        is_valid, error_message = validate_task_description(description)
        if not is_valid:
            logger.warning(f"Invalid task description: {error_message}")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'message': error_message, 'status': 'error'})
            flash(error_message, 'error')
            return redirect(url_for('index'))

        # Validate priority
        if not validate_priority(priority):
            logger.warning("Invalid priority provided, defaulting to Medium")
            priority = 'Medium'

        try:
            task_id = add_task(description, priority)
            message = f'Task added: {description} (ID: {task_id}, Priority: {priority})'
            status = 'success'
        except Exception as e:
            logger.error(f"Error adding task: {e}")
            message = 'Failed to add task. Please try again.'
            status = 'error'
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'message': message, 'status': status})
        flash(message, status)
        return redirect(url_for('index'))

    @app.route('/update/<int:task_id>', methods=['POST'])
    def update(task_id):
        new_description = request.form.get('description')
        new_priority = request.form.get('priority')

        # Validate description
        is_valid, error_message = validate_task_description(new_description)
        if not is_valid:
            logger.warning(f"Invalid task description: {error_message}")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'message': error_message, 'status': 'error'})
            flash(error_message, 'error')
            return redirect(url_for('index'))

        # Validate priority
        if not validate_priority(new_priority):
            logger.warning("Invalid priority provided, defaulting to Medium")
            new_priority = 'Medium'

        try:
            if update_task(task_id, new_description, new_priority):
                message = f'Task updated: {new_description} (ID: {task_id}, Priority: {new_priority})'
                status = 'success'
            else:
                message = f'Task ID {task_id} not found.'
                status = 'error'
        except Exception as e:
            logger.error(f"Error updating task ID {task_id}: {e}")
            message = 'Failed to update task. Please try again.'
            status = 'error'
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'message': message, 'status': status})
        flash(message, status)
        return redirect(url_for('index'))

    @app.route('/delete/<int:task_id>')
    def delete(task_id):
        try:
            if delete_task(task_id):
                message = f'Task ID {task_id} deleted.'
                status = 'success'
            else:
                message = f'Task ID {task_id} not found.'
                status = 'error'
        except Exception as e:
            logger.error(f"Error deleting task ID {task_id}: {e}")
            message = 'Failed to delete task. Please try again.'
            status = 'error'
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'message': message, 'status': status})
        flash(message, status)
        return redirect(url_for('index'))

    @app.route('/complete/<int:task_id>')
    def complete(task_id):
        try:
            if mark_task(task_id, completed=True):
                message = f'Task ID {task_id} marked as completed.'
                status = 'success'
            else:
                message = f'Task ID {task_id} not found.'
                status = 'error'
        except Exception as e:
            logger.error(f"Error marking task ID {task_id} as complete: {e}")
            message = 'Failed to mark task as complete. Please try again.'
            status = 'error'
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'message': message, 'status': status})
        flash(message, status)
        return redirect(url_for('index'))

    @app.route('/incomplete/<int:task_id>')
    def incomplete(task_id):
        try:
            if mark_task(task_id, completed=False):
                message = f'Task ID {task_id} marked as incomplete.'
                status = 'success'
            else:
                message = f'Task ID {task_id} not found.'
                status = 'error'
        except Exception as e:
            logger.error(f"Error marking task ID {task_id} as incomplete: {e}")
            message = 'Failed to mark task as incomplete. Please try again.'
            status = 'error'
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'message': message, 'status': status})
        flash(message, status)
        return redirect(url_for('index'))
