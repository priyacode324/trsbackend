import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_cors import CORS
from server.python.database.db_manager import init_db
from server.python.routes import register_routes

# Define project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','..'))

# Initialize Flask app
app = Flask(__name__,
            template_folder=os.path.join(project_root, 'view/templates'),
            static_folder=os.path.join(project_root, 'view/static'))
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'supersecretkey')

# Enable CORS for all API routes
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

# Setup logging
LOGS_DIR = os.path.join(project_root, 'logs')
LOG_FILE = os.path.join(LOGS_DIR, 'task_reminder.log')
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        RotatingFileHandler(LOG_FILE, maxBytes=10*1024*1024, backupCount=5),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize database
try:
    init_db()
    logger.info("Database initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize database: {e}")
    raise

# Register routes
register_routes(app)

# Flask Port 
port=os.getenv('PORT', 7000)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(port))
