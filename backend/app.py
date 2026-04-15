from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

# Add current directory to path so we can import from .
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from search_engine import SearchEngine

app = Flask(__name__)
CORS(app)

# Initialize search engine
# Assuming website is in ../website relative to this file
website_path = os.path.join(os.path.dirname(__file__), '..', 'website')
engine = SearchEngine(website_path)

# Perform initial crawl and index on startup
try:
    engine.run_crawl_and_index()
except Exception as e:
    print(f"Error during initial indexing: {e}")

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
