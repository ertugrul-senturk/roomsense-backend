"""
RoomSense Flask Application
Main application entry point with modular architecture
"""
from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask_mail import Mail
from flask_cors import CORS
from datetime import datetime
import logging
import os
from dotenv import load_dotenv
load_dotenv()


from config import get_config
from services.auth_service import AuthService
from services.email_service import EmailService
from services.lecture_service import LectureService
from routes.auth_routes import init_auth_routes
from routes.lecture_routes import init_lecture_routes
from services.sessions_service import SessionsService

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def create_app(config_name='development'):
    """
    Application factory pattern
    
    Args:
        config_name: Configuration environment (development, production, testing)
    
    Returns:
        Flask application instance
    """
    # Initialize Flask app
    app = Flask(__name__)
    
    # Load configuration
    config = get_config(config_name)
    app.config.from_object(config)
    
    # Initialize extensions
    mongo = PyMongo(app)
    mail = Mail(app)
    CORS(app)
    
    # Initialize services
    email_service = EmailService(app.config)
    auth_service = AuthService(mongo.db, email_service)
    sessions_service = SessionsService(mongo.db)
    lecture_service = LectureService(mongo.db)
    
    # Register blueprints (routes)
    auth_blueprint = init_auth_routes(auth_service)
    app.register_blueprint(auth_blueprint)
    lecture_blueprint = init_lecture_routes(lecture_service)
    app.register_blueprint(lecture_blueprint)
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        """Application health check"""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def index():
        """API root endpoint"""
        return jsonify({
            'message': 'RoomSense API',
            'version': '2.0',
            'endpoints': {
                'auth': {
                    'register': '/auth/register',
                    'login': '/auth/login',
                    'verify': '/auth/verify',
                    'status': '/auth/status',
                    'logout': '/auth/logout'
                },
                'lectures': {
                    'create': 'POST /api/lectures/',
                    'getByLecturer': 'GET /api/lectures/lecturer/<lecturer_id>',
                    'getById': 'GET /api/lectures/<lecture_id>',
                    'update': 'PUT /api/lectures/<lecture_id>',
                    'delete': 'DELETE /api/lectures/<lecture_id>',
                    'updateDay': 'PUT /api/lectures/<lecture_id>/day/<day_id>',
                    'createQuestion': 'POST /api/lectures/<lecture_id>/questions',
                    'getQuestions': 'GET /api/lectures/<lecture_id>/questions',
                    'unansweredCount': 'GET /api/lectures/lecturer/<lecturer_id>/questions/unanswered/count'
                },
                'health': '/health'
            }
        }), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return jsonify({
            'success': False,
            'message': 'Endpoint not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        logger.error(f"Internal error: {str(error)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500
    
    logger.info(f"Application started in {config_name} mode")
    
    return app


# Create application instance
app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8061, debug=True)
