import sys
import requests
import nltk
import json
import os
from datetime import datetime, timedelta
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def download_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('punkt')
        nltk.download('stopwords')

def get_cache_path(category):
    # Create cache directory if it doesn't exist
    cache_dir = os.path.join(os.path.dirname(__file__), 'cache')
    os.makedirs(cache_dir, exist_ok=True)
    return os.path.join(cache_dir, f"{category.replace(' ', '_')}.json")

def load_cache(category):
    cache_path = get_cache_path(category)
    if not os.path.exists(cache_path):
        return None
        
    with open(cache_path, 'r', encoding='utf-8') as f:
        cache_data = json.load(f)
        
    # Check if cache is older than 24 hours
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
    # Tokenize and convert to lowercase
    tokens = word_tokenize(text.lower())
    
    # Remove stopwords and non-alphabetic tokens
    stop_words = set(stopwords.words('english'))
    words = [word for word in tokens if word.isalpha() and word not in stop_words]
    
    # Count frequencies
    return Counter(words)

def main():
    if len(sys.argv) != 2:
        print("Usage: python analyze_wiki_category.py 'category_name'")
        sys.exit(1)
    
    category = sys.argv[1]
    print(f"Analyzing category: {category}")
    
    # Check cache first
    cached_frequencies = load_cache(category)
    if cached_frequencies is not None:
        print("Using cached results...")
        total_frequencies = Counter(cached_frequencies)
    else:
        print("Cache not found or expired. Fetching fresh data...")
        # Download required NLTK data
        download_nltk_data()
        
        # Get all pages in the category
        pages = get_category_members(category)
        print(f"Found {len(pages)} pages in category")
        
        # Analyze each page
        total_frequencies = Counter()
        
        for page_title in pages:
            print(f"Processing: {page_title}")
            content = get_page_content(page_title)
            frequencies = analyze_text(content)
            total_frequencies.update(frequencies)
        
        # Save results to cache
        save_cache(category, total_frequencies)
    
    # Print top 50 most common words
    print("\nMost common words and their frequencies:")
    for word, count in total_frequencies.most_common(50):
        print(f"{word}: {count}")

if __name__ == "__main__":
    main()
