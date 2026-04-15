import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

class Crawler:
    def __init__(self, seed_file, stop_words=None):
        self.seed_file = seed_file
        self.visited = set()
        self.pages_data = [] # List of dicts: {url, title, content, tokens}
        self.stop_words = stop_words or set()
        
    def is_internal(self, url):
        # For local files, we just check if it's an .html file in the same directory
        return url.endswith('.html') and not url.startswith('http')

    def clean_text(self, text):
        # Lowercase, remove punctuation
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        return text

    def tokenize(self, text):
        raw_tokens = text.split()
        # Filter stop words and numbers, and single characters
        tokens = [t for t in raw_tokens if t not in self.stop_words and len(t) > 1]
        return tokens

    def crawl(self):
        queue = [os.path.basename(self.seed_file)]
        self.visited = set()
        base_dir = os.path.dirname(os.path.abspath(self.seed_file))

        while queue:
            current_page = queue.pop(0)
            if current_page in self.visited:
                continue
            
            file_path = os.path.join(base_dir, current_page)
            if not os.path.exists(file_path):
                continue
                
            self.visited.add(current_page)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
                
                # Extract title
                title = soup.title.string if soup.title else current_page
                
                # Extract visible text
                for script_or_style in soup(['script', 'style']):
                    script_or_style.decompose()
                
                visible_text = soup.get_text(separator=' ')
                cleaned_text = self.clean_text(visible_text)
                tokens = self.tokenize(cleaned_text)
                
                # Store data
                self.pages_data.append({
                    'file': current_page,
                    'title': title,
                    'content': visible_text.strip(),
                    'tokens': tokens
                })
                
                # Find links
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if self.is_internal(href):
                        if href not in self.visited:
                            queue.append(href)
                            
        return self.pages_data

# Standard stop words
STOP_WORDS = {
    'a', 'an', 'the', 'and', 'or', 'in', 'on', 'at', 'to', 'for', 'with', 'by', 'about', 'as', 
    'is', 'are', 'was', 'were', 'be', 'been', 'being', 'it', 'its', 'of', 'this', 'that', 'from',
    'has', 'have', 'had', 'which', 'who', 'whom', 'where', 'when', 'why', 'how', 'all', 'any',
    'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only',
    'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'
}

if __name__ == "__main__":
    # Test run
    seed = os.path.join(os.getcwd(), '..', 'website', 'index.html')
    crawler = Crawler(seed, STOP_WORDS)
    results = crawler.crawl()
    print(f"Crawled {len(results)} pages.")
    for res in results:
        print(f"Page: {res['file']} - Tokens: {len(res['tokens'])}")
