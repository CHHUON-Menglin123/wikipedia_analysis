import unittest
import json
import os
from app import app
from cache_manager import CacheManager
from config import TestingConfig

class WikiAnalyzerTests(unittest.TestCase):
    def setUp(self):
        app.config.from_object(TestingConfig)
        self.app = app.test_client()
        self.cache_manager = CacheManager(
            cache_dir=app.config['CACHE_DIR'],
            expiration_hours=app.config['CACHE_EXPIRATION_HOURS']
        )

    def tearDown(self):
        # Clean up test cache directory
        if os.path.exists(app.config['CACHE_DIR']):
            for file in os.listdir(app.config['CACHE_DIR']):
                os.remove(os.path.join(app.config['CACHE_DIR'], file))
            os.rmdir(app.config['CACHE_DIR'])

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Wikipedia Category Word Cloud Analyzer', response.data)

    def test_analyze_empty_category(self):
        response = self.app.post('/analyze', 
                               data=json.dumps({'category': ''}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_analyze_valid_category(self):
        response = self.app.post('/analyze',
                               data=json.dumps({'category': 'Large language models'}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('frequencies', data)

    def test_cache_operations(self):
        # Test cache setting
        test_data = {'test': 'data'}
        self.cache_manager.set('test_key', test_data)
        
        # Test cache retrieval
        cached_data = self.cache_manager.get('test_key')
        self.assertEqual(cached_data, test_data)
        
        # Test cache deletion
        self.cache_manager.delete('test_key')
        self.assertIsNone(self.cache_manager.get('test_key'))

if __name__ == '__main__':
    unittest.main()
