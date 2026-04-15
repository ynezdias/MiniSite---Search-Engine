import os
from crawler import Crawler, STOP_WORDS
from indexer import Indexer

class SearchEngine:
    def __init__(self, website_dir):
        self.website_dir = os.path.abspath(website_dir)
        self.crawler = None
        self.indexer = Indexer()
        self.is_indexed = False
        self.stats = {}

    def run_crawl_and_index(self):
        seed_page = os.path.join(self.website_dir, 'index.html')
        print(f"Starting crawl from: {seed_page}")
        
        self.crawler = Crawler(seed_page, STOP_WORDS)
        pages_data = self.crawler.crawl()
        
        print(f"Crawled {len(pages_data)} pages. Building index...")
        self.indexer.build_index(pages_data)
        self.is_indexed = True
        
        # Calculate stats
        unique_terms = len(self.indexer.postings_lists)
        self.stats = {
            'docs_crawled': len(pages_data),
            'unique_terms': unique_terms,
            'pages': [p['file'] for p in pages_data]
        }
        print("Indexing complete.")

    def search(self, query):
        if not self.is_indexed:
            return []
        
        # Pre-process query
        query = query.lower()
        # Remove punctuation
        import re
        query = re.sub(r'[^\w\s]', ' ', query)
        tokens = [t for t in query.split() if t not in STOP_WORDS]
        
        if not tokens:
            return []
            
        return self.indexer.search_all(tokens)

if __name__ == "__main__":
    # Local test
    engine = SearchEngine('../website')
    engine.run_crawl_and_index()
    results = engine.search("moon rocket")
    print(f"Search results for 'moon rocket':")
    for r in results:
        print(f"- {r['title']} (Score: {r['score']})")
