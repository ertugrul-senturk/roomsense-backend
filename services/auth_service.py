"""
Authentication service - Business logic layer
"""
import logging

from models.user import User
from models.verification import EmailVerification

logger = logging.getLogger(__name__)


class AuthService:
    """Service for handling authentication business logic"""

    def __init__(self, db, email_service):
        self.db = db
        self.email_service = email_service

    def login(self, email, session_id):
        email = email.lower().strip()
        session_id = session_id.strip()

        # Check if user exists
        user = User.find_by_email(self.db, email)
        if not user:
            user = User.create(self.db, email)
        user.get("pendingSessionIds", []).append(session_id)
        User.update_user(self.db, user)

        # Delete any existing verification tokens
        EmailVerification.delete_by_email(self.db, email)

        # Create verification record
        EmailVerification.create(self.db, email, session_id)

        # Send verification email
        try:
            self.email_service.send_verification_email(email, session_id)
            logger.info(f"Login verification email sent to: {email}")
            return {
                'success': True,
                'message': 'Verification email sent. Please check your email.',
                'data': {
                    'email': email,
                }
            }
        except Exception as e:
            logger.error(f"Failed to send verification email: {str(e)}")
            return {
                'success': False,
                'message': 'Failed to send verification email. Please try again.'
            }

    def get_user(self, session_id):
        session_id = session_id.strip()
        user =  User.find_by_active_session(self.db, session_id)
        if not user:
            return {'message': 'No user found',
                    'success': False}
        return {
            'success': True,
            'email': user['email'],
            'options': user['options']
        }

    def save_options(self, session_id, data):
        session_id = session_id.strip()
        user = User.find_by_active_session(self.db, session_id)
        if not user:
            return {'message': 'No user found',
                    'success': False}

        user['options'] = data
        User.update_user(self.db, user)
        return {
            'success': True
        }


    def authorize(self, session_id, ar_session_id):
        session_id = session_id.strip()
        ar_session_id = ar_session_id.strip()

        # Check if user exists
        user = User.find_by_active_session(self.db, session_id)
        if not user:
            return {
                'success': False,
                'message': 'Given session id was not active.'
            }
        user.get("activeSessionIds", []).append(ar_session_id)
        User.update_user(self.db, user)
        return {
            'success': True,
            'message': 'AR session was authorized.',
        }

    def verify_email(self, session_id):

        # Find verification record
        verification = EmailVerification.find_by_token(self.db, session_id)

        if not verification:
            return {
                'success': False,
                'message': 'Invalid or expired verification token'
            }

        # Check if expired
        if EmailVerification.is_expired(verification):
            return {
                'success': False,
                'message': 'Verification token has expired. Please request a new login link.'
            }

        # Find user
        user = User.find_by_email(self.db, verification['email'])
        if not user:
            return {
                'success': False,
                'message': 'User not found'
            }

        # Mark verification as verified
        EmailVerification.mark_as_verified(self.db, verification['_id'])

        # Set user as active
        User.activate_session(self.db, user['_id'], session_id)


        logger.info(f"User logged in successfully: {user['email']}")

        return {
            'success': True,
            'message': 'Login successful',
            'data': {
                'email': user['email'],
            }
        }

    def is_session_alive(self, session_id):
        user = User.find_by_active_session(self.db, session_id)
        return session_id in user.get('activeSessionIds', [])


    def check_login_status(self, session_id):
        if not session_id:
            return {
                'loggedIn': False,
                'email': None,
                'sessionId': None
            }

        session_id = session_id.strip()

        # Find user by session token
        user = User.find_by_active_session(self.db, session_id)

        if not user:
            return {
                'loggedIn': False,
                'email': None,
                'sessionId': None
            }

        is_active = session_id in user.get('activeSessionIds', [])
        if not is_active:
            return {
                'loggedIn': False,
            }

        if not is_active:
            return {
                'loggedIn': False,
                'email': user['email'],
                'sessionId': session_id
            }

        return {
            'loggedIn': True,
            'email': user['email'],
            'sessionId': session_id
        }

    def logout(self, session_id):

        if not session_id:
            return {
                'success': False,
                'message': 'No email provided'
            }

        session_id = session_id.strip()

        # Find user
        user = User.find_by_active_or_pending_session(self.db, session_id)

        if not user:
            return {
                'success': False,
                'message': 'User not found'
            }

        # Set user as inactive
        User.inactivate_session(self.db, user['_id'], session_id)

        logger.info(f"User logged out: {user['email']}")

        return {
            'success': True,
            'message': 'Logout successful'
        }