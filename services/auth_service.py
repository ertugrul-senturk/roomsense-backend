"""
Authentication service - Business logic layer
"""
import uuid
import random
import logging

from models.user import User
from models.verification import EmailVerification

logger = logging.getLogger(__name__)


class AuthService:
    """Service for handling authentication business logic"""

    def __init__(self, db, email_service):
        self.db = db
        self.email_service = email_service

    def generate_unique_number(self):
        """Generate a unique 10-digit number"""
        max_attempts = 100
        for _ in range(max_attempts):
            number = random.randint(1_000_000_000, 9_999_999_999)
            unique_number = str(number)
            if not User.find_by_unique_number(self.db, unique_number):
                return unique_number
        raise Exception("Failed to generate unique number")

    def register(self, email):
        """
        Register a new user and send verification email

        Args:
            email: User's email address

        Returns:
            dict: Response with success status and unique number
        """
        email = email.lower().strip()

        # Check if user already exists
        if User.exists_by_email(self.db, email):
            return {
                'success': False,
                'message': 'Email already registered. Please use login instead.'
            }

        # Generate unique number
        try:
            unique_number = self.generate_unique_number()
        except Exception as e:
            logger.error(f"Failed to generate unique number: {str(e)}")
            return {
                'success': False,
                'message': 'Registration failed. Please try again.'
            }

        # Create user (isActive will be False by default)
        user = User.create(self.db, email, unique_number)

        # Delete any existing verification tokens
        EmailVerification.delete_by_email(self.db, email)

        # Generate verification token
        verification_token = str(uuid.uuid4())

        # Create verification record
        EmailVerification.create(self.db, email, verification_token)

        # Send verification email
        try:
            self.email_service.send_verification_email(email, verification_token, unique_number)
            logger.info(f"New user registered: {email} with unique number: {unique_number}")
            return {
                'success': True,
                'message': 'Registration successful. Please check your email to verify your account.',
                'data': {
                    'email': email,
                    'uniqueNumber': unique_number
                }
            }
        except Exception as e:
            logger.error(f"Failed to send verification email: {str(e)}")
            # Clean up user if email fails
            User.delete_by_email(self.db, email)
            return {
                'success': False,
                'message': 'Failed to send verification email. Please try again.'
            }

    def login(self, email):
        """
        Initiate login by sending verification email

        Args:
            email: User's email address

        Returns:
            dict: Response with success status and unique number
        """
        email = email.lower().strip()

        # Check if user exists
        user = User.find_by_email(self.db, email)
        if not user:
            return {
                'success': False,
                'message': 'User not found. Please register first.'
            }

        # Delete any existing verification tokens
        EmailVerification.delete_by_email(self.db, email)

        # Generate verification token
        verification_token = str(uuid.uuid4())

        # Create verification record
        EmailVerification.create(self.db, email, verification_token)

        # Send verification email
        try:
            self.email_service.send_verification_email(email, verification_token, user['uniqueNumber'])
            logger.info(f"Login verification email sent to: {email}")
            return {
                'success': True,
                'message': 'Verification email sent. Please check your email.',
                'data': {
                    'email': email,
                    'uniqueNumber': user['uniqueNumber']
                }
            }
        except Exception as e:
            logger.error(f"Failed to send verification email: {str(e)}")
            return {
                'success': False,
                'message': 'Failed to send verification email. Please try again.'
            }

    def verify_email(self, token):
        """
        Verify email and activate user account

        Args:
            token: Verification token from email

        Returns:
            dict: Response with success status and user data
        """
        # Find verification record
        verification = EmailVerification.find_by_token(self.db, token)

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
        User.set_active_status(self.db, user['_id'], True)

        # Update last login
        User.update_last_login(self.db, user['_id'])

        logger.info(f"User logged in successfully: {user['email']}")

        return {
            'success': True,
            'message': 'Login successful',
            'data': {
                'email': user['email'],
                'uniqueNumber': user['uniqueNumber'],
                'isActive': True
            }
        }

    def check_login_status(self, email):
        """
        Check if user is logged in (active)

        Args:
            email: User's email address

        Returns:
            dict: Login status with user data if logged in
        """
        if not email:
            return {
                'loggedIn': False,
                'email': None,
                'uniqueNumber': None
            }

        email = email.lower().strip()

        # Find user
        user = User.find_by_email(self.db, email)

        if not user:
            return {
                'loggedIn': False,
                'email': None,
                'uniqueNumber': None
            }

        # Check if user is active
        is_active = user.get('isActive', False)

        if not is_active:
            return {
                'loggedIn': False,
                'email': user['email'],
                'uniqueNumber': user['uniqueNumber']
            }

        return {
            'loggedIn': True,
            'email': user['email'],
            'uniqueNumber': user['uniqueNumber']
        }

    def logout(self, email):
        """
        Logout user by setting isActive to False

        Args:
            email: User's email address

        Returns:
            dict: Response with success status
        """
        if not email:
            return {
                'success': False,
                'message': 'No email provided'
            }

        email = email.lower().strip()

        # Find user
        user = User.find_by_email(self.db, email)

        if not user:
            return {
                'success': False,
                'message': 'User not found'
            }

        # Set user as inactive
        User.set_active_status(self.db, user['_id'], False)

        logger.info(f"User logged out: {email}")

        return {
            'success': True,
            'message': 'Logout successful'
        }