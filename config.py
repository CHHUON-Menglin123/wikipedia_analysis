import os

class Config:
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() in ('true', '1', 't')
    
    # Cache Configuration
    CACHE_DIR = os.path.join(os.path.dirname(__file__), 'cache')
    CACHE_EXPIRATION_HOURS = 24
    
    # Wikipedia API Configuration
    WIKI_API_URL = "https://en.wikipedia.org/w/api.php"
    WIKI_API_LIMIT = 500  # Maximum number of articles to fetch per category
    
    # Word Cloud Configuration
    MAX_WORDS = 50  # Maximum number of words to show in cloud
    MIN_WORD_LENGTH = 3  # Minimum length of words to include
    
    # Development/Production Configs
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
    # Add production-specific settings here

class TestingConfig(Config):
    TESTING = True
    # Use separate cache directory for tests
    CACHE_DIR = os.path.join(os.path.dirname(__file__), 'test_cache')

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
