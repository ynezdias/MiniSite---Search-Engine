# Space Exploration Search Engine

A simplified search engine built for a mini-website (5-10 pages) using React.js for the frontend and Python for the backend.

## Project Structure
- `backend/`: Python Flask server, Crawler, Indexer, and Ranked Search.
- `website/`: Local HTML pages on the theme of Space Exploration.
- `README.md`: This file.
- `sample_runs.txt`: Output of boundary case testing.

## Algorithms and Data Structures

### 1. Web Crawler
- **Discovery**: Starts from `website/index.html`. Uses BFS to follow all internal `.html` links.
- **Extraction**: Uses `BeautifulSoup` to extract visible text from HTML content, excluding scripts and styles.
- **Normalization**: Converts text to lowercase, removes punctuation, and filters out common stop words (e.g., "the", "and", "is").

### 2. Compressed Trie (Radix Tree)
- **Concept**: A memory-efficient Trie where nodes with only one child are merged with their parents. This reduces the number of nodes by storing substrings on edges.
- **Implementation**: The terms (unique words) are stored in the Compressed Trie. Each terminal node stores an integer `postings_index` instead of the postings list itself.
- **Efficiency**: Allows for fast $O(k)$ lookups where $k$ is the length of the search term.

### 3. Inverted Index (Textbook Style)
- **Occurrence Lists**: Stored separately in a central array. Each list contains tuples of `(document_reference, frequency)`.
- **Sorting**: Occurrence lists are sorted by `document_reference` to allow for efficient intersection.
- **Mapping**: Terminal nodes in the Compressed Trie point to the index of their corresponding occurrence list in the central array.

### 4. Search and Ranking
- **Single Keywords**: Fetches the occurrence list from the Trie for the given term.
- **Multi-Keyword Query**: Performs a **merge-style intersection** (AND logic) of two sorted lists in $O(n+m)$ time.
- **Scoring**: 
  - `Base Score`: Sum of term frequencies in the document.
  - `Bonus`: A significant bonus (+5) is added if the query term appears in the page title.
- **Ranking**: Results are returned in descending order of their total score.

## How to Run
1. Ensure Python 3.x and Pip are installed.
2. Install dependencies: `pip install beautifulsoup4 flask flask-cors`
3. Start the server: `python backend/app.py`
4. Open your browser to `http://127.0.0.1:5000` to access the search interface.