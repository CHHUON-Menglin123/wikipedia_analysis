from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import nltk
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json
import os
from datetime import datetime
from cache_manager import CacheManager

app = Flask(__name__, static_url_path='/static', static_folder='static')
CORS(app)

# Initialize cache manager
cache_manager = CacheManager(cache_dir='cache', expiration_hours=24)

@app.route('/cache/stats')
def get_cache_stats():
    """Get cache statistics."""
    return jsonify(cache_manager.get_stats())

@app.route('/cache/cleanup')
def cleanup_cache():
    """Clean up expired cache entries."""
    cleaned = cache_manager.cleanup()
    return jsonify({
        'cleaned_entries': cleaned,
        'stats': cache_manager.get_stats()
    })

def download_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('punkt')
        nltk.download('stopwords')

def get_cache_path(category):
    cache_dir = os.path.join(os.path.dirname(__file__), 'cache')
    os.makedirs(cache_dir, exist_ok=True)
    return os.path.join(cache_dir, f"{category.replace(' ', '_')}.json")

def load_cache(category):
    cache_path = get_cache_path(category)
    if not os.path.exists(cache_path):
        return None
        
    with open(cache_path, 'r', encoding='utf-8') as f:
        cache_data = json.load(f)
        
    cache_time = datetime.fromisoformat(cache_data['timestamp'])
    if datetime.now() - cache_time > timedelta(hours=24):
        return None
        
    return cache_data['frequencies']

def save_cache(category, frequencies):
    cache_path = get_cache_path(category)
    cache_data = {
        'timestamp': datetime.now().isoformat(),
        'frequencies': frequencies
    }
    
    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(cache_data, f, ensure_ascii=False, indent=2)

def get_category_members(category):
    S = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"
    
    PARAMS = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": f"Category:{category}",
        "cmlimit": "500",
        "format": "json"
    }
    
    response = S.get(url=URL, params=PARAMS)
    data = response.json()
    return [page['title'] for page in data['query']['categorymembers'] if page['ns'] == 0]

def get_page_content(title):
    S = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"
    
    PARAMS = {
        "action": "query",
        "prop": "extracts",
        "exlimit": "1",
        "titles": title,
        "explaintext": "1",
        "format": "json"
    }
    
    response = S.get(url=URL, params=PARAMS)
    data = response.json()
    page = next(iter(data['query']['pages'].values()))
    return page.get('extract', '')

def analyze_text(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    words = [word for word in tokens if word.isalpha() and word not in stop_words]
    return Counter(words)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    category = request.json.get('category')
    if not category:
        return jsonify({'error': 'Category is required'}), 400

    # Check cache first
    cached_data = cache_manager.get(category)
    if cached_data is not None:
        return jsonify({
            'frequencies': cached_data,
            'cached': True,
            'cache_stats': cache_manager.get_stats()
        })

    try:
        # Download required NLTK data
        download_nltk_data()
        
        # Get all pages in the category
        pages = get_category_members(category)
        if not pages:
            return jsonify({'error': 'No pages found in category'}), 404
        
        # Analyze each page
        total_frequencies = Counter()
        processed_pages = []
        
        for page_title in pages:
            content = get_page_content(page_title)
            frequencies = analyze_text(content)
            total_frequencies.update(frequencies)
            processed_pages.append(page_title)
        
        # Convert Counter to dict for JSON serialization
        result = dict(total_frequencies)
        
        # Save to cache
        cache_manager.set(category, result)
        
        return jsonify({
            'frequencies': result,
            'processed_pages': processed_pages,
            'cached': False
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
