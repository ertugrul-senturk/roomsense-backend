"""
Authentication routes
"""
from flask import Blueprint, jsonify, request, render_template, session

import logging

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def init_auth_routes(auth_service):
    """Initialize auth routes with service dependency"""
    
    @auth_bp.route('/register', methods=['POST'])
    def register():
        """
        Register a new user
        POST /auth/register
        Body: {"email": "user@example.com"}
        """
        try:
            data = request.get_json()
            email = data.get('email')
            
            if not email:
                return jsonify({
                    'success': False,
                    'message': 'Email is required'
                }), 400
            
            result = auth_service.register(email)
            
            if result['success']:
                return jsonify(result), 201
            else:
                return jsonify(result), 400
                
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Registration failed'
            }), 500
    
    
    @auth_bp.route('/login', methods=['POST'])
    def login():
        """
        Initiate login process by sending verification email
        POST /auth/login
        Body: {"email": "user@example.com"}
        """
        try:
            data = request.get_json()
            email = data.get('email')
            
            if not email:
                return jsonify({
                    'success': False,
                    'message': 'Email is required'
                }), 400
            
            result = auth_service.login(email)
            
            if result['success']:
                return jsonify(result), 200
            else:
                return jsonify(result), 400
                
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Login failed'
            }), 500

    @auth_bp.route('/verify')
    def verify():
        """Handle email verification from link"""
        token = request.args.get('token')

        if not token:
            return render_template('auth/verification_failed.html',
                                   reason='No verification token provided')

        # Call auth service
        result = auth_service.verify_email(token)

        if result['success']:
            # Store user data in session
            session['email'] = result['data']['email']
            session['uniqueNumber'] = result['data']['uniqueNumber']
            session['isActive'] = True

            return render_template('auth/verification_success.html',
                                   email=result['data']['email'],
                                   unique_number=result['data']['uniqueNumber'])
        else:
            # Handle different error cases
            if result.get('redirect') == 'verification-expired':
                return render_template('templates/auth/verification_expired.html',
                                       message=result['message'])
            else:
                return render_template('templates/auth/verification_failed.html',
                                       reason=result['message'])
    
    
    @auth_bp.route('/status', methods=['GET'])
    def check_login_status():
        """
        Check if user is logged in
        GET /auth/status
        Header: Authorization: Bearer {sessionToken}
        """
        try:
            auth_header = request.headers.get('Authorization')
            
            session_token = None
            if auth_header and auth_header.startswith('Bearer '):
                session_token = auth_header[7:]
            
            result = auth_service.check_login_status(session_token)
            
            return jsonify(result), 200
            
        except Exception as e:
            logger.error(f"Status check error: {str(e)}")
            return jsonify({
                'loggedIn': False,
                'email': None,
                'uniqueNumber': None
            }), 200
    
    
    @auth_bp.route('/logout', methods=['POST'])
    def logout():
        """
        Logout user
        POST /auth/logout
        Header: Authorization: Bearer {sessionToken}
        """
        try:
            auth_header = request.headers.get('Authorization')
            
            session_token = None
            if auth_header and auth_header.startswith('Bearer '):
                session_token = auth_header[7:]
            
            result = auth_service.logout(session_token)
            
            if result['success']:
                return jsonify(result), 200
            else:
                return jsonify(result), 400
                
        except Exception as e:
            logger.error(f"Logout error: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Logout failed'
            }), 500
    
    return auth_bp
