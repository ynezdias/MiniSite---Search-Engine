from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import sys

# Add current directory to path so we can import from .
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from search_engine import SearchEngine

app = Flask(__name__, template_folder='templates')
CORS(app)

# Initialize search engine
# Assuming website is in ../website relative to this file
base_dir = os.path.dirname(os.path.abspath(__file__))
website_path = os.path.join(base_dir, '..', 'website')
engine = SearchEngine(website_path)

# Perform initial crawl and index on startup
try:
    engine.run_crawl_and_index()
except Exception as e:
    print(f"Error during initial indexing: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify({
            'results': [],
            'message': 'Empty query',
            'stats': engine.stats
        })
    
    results = engine.search(query)
    return jsonify({
        'results': results,
        'stats': engine.stats
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    return jsonify(engine.stats)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
