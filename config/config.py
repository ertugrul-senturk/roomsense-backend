"""
Application configuration
"""
import os


class Config:
    """Base configuration"""
    
    # MongoDB
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://esenturk:Test_123@roomsense.mncac3o.mongodb.net/roomsense')
    
    # Email (SMTP)
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY', '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')
    FROM_EMAIL = os.getenv('FROM_EMAIL','esenturk@ur.rochester.edu')

    # Application
    BASE_URL = os.getenv('BASE_URL', 'https://roomsense-backend.onrender.com/')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Session
    SESSION_EXPIRY_DAYS = int(os.getenv('SESSION_EXPIRY_DAYS', 7))
    VERIFICATION_EXPIRY_MINUTES = int(os.getenv('VERIFICATION_EXPIRY_MINUTES', 15))


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env=None):
    """Get configuration based on environment"""
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
