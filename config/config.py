"""
Application configuration
"""
import os

class Config:
    """Base configuration"""

    # MongoDB
    MONGO_URI = os.getenv('MONGO_URI')

    # Email (SMTP)
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
    FROM_EMAIL = os.getenv('FROM_EMAIL')

    # Application
    BASE_URL = os.getenv('BASE_URL')
    SECRET_KEY = os.getenv('SECRET_KEY')

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