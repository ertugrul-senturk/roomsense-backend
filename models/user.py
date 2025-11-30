"""
User Model - MongoDB implementation for passwordless authentication
"""
from datetime import datetime


class User:
    """
    User model for passwordless authentication system
    """

    @staticmethod
    def create(db, email):
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
            'createdAt': datetime.utcnow(),
            'activeSessionIds': [],
            'pendingSessionIds': [],
            'inactiveSessionIds': [],
            'options': {
                'name': 'Lecturer',
                'individualEngagement': True,
                'acceptQueries': True,
                'displayTimeline': True,
                'displayNotes': True
            }
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
    def find_by_active_session(db, session_id):
        """
        Find user by active session ID

        Args:
            db: Database connection
            session_id: Session ID to search for

        Returns:
            dict: User document or None if not found
        """
        return db.users.find_one({'activeSessionIds': session_id})

    @staticmethod
    def find_by_active_or_pending_session(db, session_id):
        """
        Find user by active or pending session ID

        Args:
            db: Database connection
            session_id: Session ID to search for

        Returns:
            dict: User document or None if not found
        """
        return db.users.find_one({
            '$or': [
                {'activeSessionIds': session_id},
                {'pendingSessionIds': session_id}
            ]
        })

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
    def update_user(db, user):
        if '_id' not in user:
            raise ValueError("User object must contain '_id'")

        # Make a copy and ensure _id is not updated
        user_id = user['_id']
        update_data = {k: v for k, v in user.items() if k != '_id'}

        # Always update lastLogin as well
        update_data['lastLogin'] = datetime.utcnow()

        result = db.users.update_one(
            {'_id': user_id},
            {'$set': update_data}
        )

        return result.modified_count > 0 or result.matched_count > 0


    @staticmethod
    def activate_session(db, _id, session_id):
        user = db.users.find_one({'_id': _id})
        if not user:
            return {"success": False, "message": "User not found"}

        active = user.get('activeSessionIds', [])
        pending = user.get('pendingSessionIds', [])
        inactive = user.get('inactiveSessionIds', [])

        # Already active
        if session_id in active:
            return {"success": False, "message": "Session is already active"}

        # Was active before but now inactive → outdated
        if session_id in inactive:
            return {"success": False, "message": "Session is outdated"}

        # Must be in pending to activate
        if session_id not in pending:
            return {"success": False, "message": "Session not found"}

        # Move from pending → active
        db.users.update_one(
            {'_id': _id},
            {
                '$pull': {'pendingSessionIds': session_id},
                '$addToSet': {'activeSessionIds': session_id}
            }
        )

        return {"success": True, "message": "Session activated"}

    @staticmethod
    def inactivate_session(db, _id, session_id):
        user = db.users.find_one({'_id': _id})
        if not user:
            return {"success": False, "message": "User not found"}

        active = user.get('activeSessionIds', [])
        pending = user.get('pendingSessionIds', [])
        inactive = user.get('inactiveSessionIds', [])

        # Already inactive
        if session_id in inactive:
            return {"success": False, "message": "Session already inactive"}

        # Not found anywhere
        if session_id not in active and session_id not in pending:
            return {"success": False, "message": "Session not found"}

        # Move active → inactive, pending → inactive
        db.users.update_one(
            {'_id': _id},
            {
                '$pull': {
                    'activeSessionIds': session_id,
                    'pendingSessionIds': session_id
                },
                '$addToSet': {'inactiveSessionIds': session_id}
            }
        )

        return {"success": True, "message": "Session inactivated"}

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