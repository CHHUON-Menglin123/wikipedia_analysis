# Wikipedia Category Word Cloud Analyzer

A web application that analyzes Wikipedia categories and generates interactive word clouds showing the frequency of non-common words across all pages in a category.

## Features

- Analyze any Wikipedia category to find most common words
- Interactive word cloud visualization using D3.js
- Multiple color schemes (Default, Pastel, Dark Theme, Nature-inspired, Time-based)
- Caching system for faster repeated queries
- Responsive web interface

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd wikipedia_analysis
```

2. Install dependencies (choose one method):

Using pip:
```bash
pip3 install -r requirements.txt
```

Using Conda:
```bash
conda create -n wiki_env python=3.9
conda activate wiki_env
pip install -r requirements.txt
```

## Usage

1. Start the Flask server:
```bash
python3 app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Enter a Wikipedia category name (e.g., "Large language models") and click Analyze

## Project Structure

```
wikipedia_analysis/
├── app.py                 # Flask application
├── cache_manager.py       # Cache management system
├── requirements.txt       # Python dependencies
├── static/
│   └── js/
│       └── colorPalettes.js  # Color schemes for word cloud
├── templates/
│   └── index.html        # Main web interface
└── README.md             # Project documentation
```

## Dependencies

- Flask: Web framework
- NLTK: Natural language processing
- Requests: HTTP client
- D3.js: Visualization library
- D3-Cloud: Word cloud layout

## Color Schemes

- Default: Professional and modern colors
- Pastel: Soft, muted colors
- Dark Theme: Vibrant colors on dark background
- Nature: Earth-toned colors
- Time-based: Colors that change based on time of day

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
