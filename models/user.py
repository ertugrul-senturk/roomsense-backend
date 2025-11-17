"""
User Model - MongoDB implementation for passwordless authentication
"""
from datetime import datetime


class User:
    """
    User model for passwordless authentication system
    """

    @staticmethod
    def create(db, email, unique_number):
        """
        Create a new user with isActive set to False by default

        Args:
            db: Database connection
            email: User's email address
            unique_number: Generated unique 10-digit number

        Returns:
            dict: Created user document
        """
        user_document = {
            'email': email,
            'uniqueNumber': unique_number,
            'isActive': False,  # Inactive until email verification
            'createdAt': datetime.utcnow(),
            'lastLogin': None
        }

        result = db.users.insert_one(user_document)
        user_document['_id'] = result.inserted_id

        return user_document

    @staticmethod
    def exists_by_email(db, email):
        """
        Check if user exists by email

        Args:
            db: Database connection
            email: User's email address

        Returns:
            bool: True if user exists, False otherwise
        """
        return db.users.find_one({'email': email}) is not None

    @staticmethod
    def find_by_email(db, email):
        """
        Find user by email

        Args:
            db: Database connection
            email: User's email address

        Returns:
            dict: User document or None
        """
        return db.users.find_one({'email': email})

    @staticmethod
    def find_by_unique_number(db, unique_number):
        """
        Find user by unique number

        Args:
            db: Database connection
            unique_number: User's unique 10-digit number

        Returns:
            dict: User document or None
        """
        return db.users.find_one({'uniqueNumber': unique_number})

    @staticmethod
    def set_active_status(db, user_id, is_active):
        """
        Set user's isActive status

        Args:
            db: Database connection
            user_id: User's MongoDB ObjectId
            is_active: Boolean flag to set

        Returns:
            bool: True if successful
        """
        result = db.users.update_one(
            {'_id': user_id},
            {'$set': {'isActive': is_active}}
        )
        return result.modified_count > 0 or result.matched_count > 0

    @staticmethod
    def update_last_login(db, user_id):
        """
        Update user's last login timestamp

        Args:
            db: Database connection
            user_id: User's MongoDB ObjectId

        Returns:
            bool: True if successful
        """
        result = db.users.update_one(
            {'_id': user_id},
            {'$set': {'lastLogin': datetime.utcnow()}}
        )
        return result.modified_count > 0 or result.matched_count > 0

    @staticmethod
    def delete_by_email(db, email):
        """
        Delete user by email (used for cleanup if email sending fails)

        Args:
            db: Database connection
            email: User's email address

        Returns:
            bool: True if successful
        """
        result = db.users.delete_one({'email': email})
        return result.deleted_count > 0