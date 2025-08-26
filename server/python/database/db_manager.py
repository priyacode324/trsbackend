import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "tasks.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                priority TEXT DEFAULT 'Medium',
                completed INTEGER DEFAULT 0
            )
        """)
        conn.commit()

def load_tasks():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, description, priority, completed FROM tasks")
        rows = cursor.fetchall()
        return [{"id": r[0], "description": r[1], "priority": r[2], "completed": bool(r[3])} for r in rows]

def add_task(description, priority="Medium"):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (description, priority) VALUES (?, ?)", (description, priority))
        conn.commit()
        return cursor.lastrowid

def update_task(task_id, description, priority):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET description=?, priority=? WHERE id=?", (description, priority, task_id))
        conn.commit()
        return cursor.rowcount > 0

def delete_task(task_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        return cursor.rowcount > 0

def mark_task(task_id, completed: bool):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET completed=? WHERE id=?", (1 if completed else 0, task_id))
        conn.commit()
        return cursor.rowcount > 0
