"""
Authentication routes
"""
from flask import Blueprint, jsonify, request, render_template, session

import logging

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def init_auth_routes(auth_service):
    """Initialize auth routes with service dependency"""

    @auth_bp.route('/options')
    def get_options():
        """Get user data by session id"""
        session_id = request.args.get('sessionId')
        try:
            if not session_id:
                return jsonify({
                    'success': False,
                    'message': 'Session id is required'
                }), 400

            result = auth_service.get_user(session_id)

            if result['options']:
                return jsonify(result['options']), 200
            else:
                return jsonify(result), 400

        except Exception as e:
            logger.error(f"Options cannot be retrieved error: {str(e)}")
            return jsonify({
                'message': 'Options cannot be retrieved'
            }), 500

    @auth_bp.route('/options', methods=['POST'])
    def save_options():
        try:
            session_id = request.args.get('sessionId')
            data = request.get_json()

            if not session_id:
                return jsonify({
                    'success': False,
                    'message': 'SessionId is required'
                }), 400

            result = auth_service.save_options(session_id, data)

            if result['success']:
                return jsonify(result), 200
            else:
                return jsonify(result), 400

        except Exception as e:
            logger.error(f"Options cannot be saved error: {str(e)}")
            return jsonify({
                'message': 'Options cannot be saved'
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
            session_id = data.get('sessionId')
            
            if not email:
                return jsonify({
                    'success': False,
                    'message': 'Email is required'
                }), 400
            
            result = auth_service.login(email, session_id)
            
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



        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Login failed'
            }), 500

    @auth_bp.route('/authorize', methods=['POST'])
    def authorize():
        """
        Initiate login process by sending verification email
        POST /auth/login
        Body: {"email": "user@example.com"}
        """
        try:
            data = request.get_json()
            session_id = data.get('sessionId')
            ar_session_id = data.get('arSessionId')

            if not session_id or not ar_session_id:
                return jsonify({
                    'success': False,
                    'message': 'Session id and arSessionId is required'
                }), 400

            result = auth_service.authorize(session_id, ar_session_id)

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
        session_id = request.args.get('sessionId')

        if not session_id:
            return render_template('auth/verification_failed.html',
                                   reason='No verification token provided')

        # Call auth service
        result = auth_service.verify_email(session_id)

        if result['success']:
            # Store user data in session
            session['email'] = result['data']['email']
            session['isActive'] = True

            return render_template('auth/verification_success.html',
                                   email=result['data']['email'])
        else:
            # Handle different error cases
            if result.get('redirect') == 'verification-expired':
                return render_template('auth/verification_expired.html',
                                       message=result['message'])
            else:
                return render_template('auth/verification_failed.html',
                                       reason=result['message'])

    @auth_bp.route('/status', methods=['POST'])
    def check_login_status():
        try:
            data = request.get_json()
            session_id = data.get('sessionId')

            if not session_id:
                return jsonify({
                    'loggedIn': False,
                    'email': None,
                }), 200

            result = auth_service.check_login_status(session_id)

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
        Body: { "email": "user@example.com" }
        """
        try:
            data = request.get_json()
            sessionId = data.get('sessionId') if data else None

            if not sessionId:
                return jsonify({
                    'success': False,
                    'message': 'Session id is required'
                }), 400

            result = auth_service.logout(sessionId)

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
