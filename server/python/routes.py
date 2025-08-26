from flask import request, jsonify

# OR to be more explicit:
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

from server.python.database.db_manager import (
    load_tasks,
    add_task,
    update_task,
    delete_task,
    mark_task
)
from server.python.database.model import (
    validate_task_description,
    validate_priority
)

def register_routes(app):
    @app.route("/api/v1/tasks", methods=["GET"])
    def get_tasks():
        tasks = load_tasks()
        return jsonify(tasks)

    @app.route("/api/v1/add/tasks", methods=["POST"])
    def add():
        data = request.json
        description = data.get("description")
        priority = data.get("priority", "low")

        if not validate_task_description(description):
            return jsonify({"status": "error", "message": "Invalid task description"}), 400

        if not validate_priority(priority):
            return jsonify({"status": "error", "message": "Invalid priority"}), 400

        task_id = add_task(description, priority)
        return jsonify({"status": "success", "task_id": task_id})

    @app.route("/api/v1/update/<int:task_id>", methods=["PUT"])
    def update(task_id):
        data = request.json
        description = data.get("description")
        priority = data.get("priority", "Medium")

        if not validate_task_description(description):
            return jsonify({"status": "error", "message": "Invalid task description"}), 400

        if not validate_priority(priority):
            return jsonify({"status": "error", "message": "Invalid priority"}), 400

        updated = update_task(task_id, description, priority)
        if updated:
            return jsonify({"status": "success"})
        return jsonify({"status": "error", "message": "Task not found"}), 404

    @app.route("/api/v1/delete/<int:task_id>", methods=["DELETE"])
    def delete(task_id):
        deleted = delete_task(task_id)
        if deleted:
            return jsonify({"status": "success"})
        return jsonify({"status": "error", "message": "Task not found"}), 404

    @app.route("/api/v1/complete/<int:task_id>", methods=["PUT"])
    def complete(task_id):
        marked = mark_task(task_id, True)
        if marked:
            return jsonify({"status": "success"})
        return jsonify({"status": "error", "message": "Task not found"}), 404

    @app.route("/api/v1/incomplete/<int:task_id>", methods=["PUT"])
    def incomplete(task_id):
        marked = mark_task(task_id, False)
        if marked:
            return jsonify({"status": "success"})
        return jsonify({"status": "error", "message": "Task not found"}), 404
