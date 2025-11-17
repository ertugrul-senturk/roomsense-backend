"""
Email verification model and data access
"""
from datetime import datetime, timedelta


class EmailVerification:
    """Email verification model"""
    
    @staticmethod
    def create(db, email, verification_token, minutes=15):
        """Create a new email verification"""
        verification = {
            'email': email,
            'verificationToken': verification_token,
            'createdAt': datetime.utcnow(),
            'expiresAt': datetime.utcnow() + timedelta(minutes=minutes),
            'isVerified': False
        }
        result = db.email_verifications.insert_one(verification)
        verification['_id'] = result.inserted_id
        return verification
    
    @staticmethod
    def find_by_token(db, token):
        """Find unverified token"""
        return db.email_verifications.find_one({
            'verificationToken': token,
            'isVerified': False
        })
    
    @staticmethod
    def mark_as_verified(db, verification_id):
        """Mark verification as verified"""
        return db.email_verifications.update_one(
            {'_id': verification_id},
            {'$set': {'isVerified': True}}
        )
    
    @staticmethod
    def delete_by_email(db, email):
        """Delete all verifications for an email"""
        return db.email_verifications.delete_many({'email': email})
    
    @staticmethod
    def is_expired(verification):
        """Check if verification is expired"""
        return verification['expiresAt'] < datetime.utcnow()
