class TrieNode:
    def __init__(self, prefix=""):
        self.prefix = prefix
        self.children = {} # char -> TrieNode
        self.postings_index = -1 # -1 if not a terminal for a word

class CompressedTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, postings_index):
        node = self.root
        i = 0
        while i < len(word):
            char = word[i]
            if char not in node.children:
                # Simple case: create new edge
                node.children[char] = TrieNode(word[i:])
                node.children[char].postings_index = postings_index
                return
            
            child = node.children[char]
            prefix = child.prefix
            j = 0
            # Find common prefix between edge and word remainder
            while j < len(prefix) and i + j < len(word) and prefix[j] == word[i + j]:
                j += 1
            
            if j < len(prefix):
                # Split existing edge
                new_child = TrieNode(prefix[:j])
                old_child = child
                old_child.prefix = prefix[j:]
                
                # Update parent to point to new intermediate node
                node.children[char] = new_child
                # Update intermediate node to point to old child
                new_child.children[old_child.prefix[0]] = old_child
                
                # Check if we still have word left to insert
                if i + j < len(word):
                    # Create new branch from split point
                    new_branch = TrieNode(word[i+j:])
                    new_branch.postings_index = postings_index
                    new_child.children[word[i+j]] = new_branch
                else:
                    # The word ends at this split point
                    new_child.postings_index = postings_index
                return
            else:
                # Full prefix match, continue down
                i += j
                node = child
        
        # Exact match of an existing path segment
        node.postings_index = postings_index

    def search(self, word):
        node = self.root
        i = 0
        while i < len(word):
            char = word[i]
            if char not in node.children:
                return -1
            
            child = node.children[char]
            prefix = child.prefix
            if word[i:i+len(prefix)] == prefix:
                i += len(prefix)
                node = child
            else:
                return -1
        
        return node.postings_index

class Indexer:
    def __init__(self):
        self.trie = CompressedTrie()
        self.postings_lists = [] # Array of [(doc_id, freq)]
        self.word_to_list_index = {} # Map word -> index in postings_lists
        self.doc_map = {} # doc_id -> metadata (title, file)

    def build_index(self, pages_data):
        # 1. Map documents to IDs
        for i, page in enumerate(pages_data):
            self.doc_map[i] = {
                'file': page['file'],
                'title': page['title'],
                'content': page['content']
            }
        
        # 2. Count term frequencies per document
        # temp_index[word] = { doc_id: freq }
        temp_index = {}
        for doc_id, page in enumerate(pages_data):
            for token in page['tokens']:
                if token not in temp_index:
                    temp_index[token] = {}
                temp_index[token][doc_id] = temp_index[token].get(doc_id, 0) + 1
        
        # 3. Build the sorted postings lists and Trie
        words = sorted(temp_index.keys())
        for word in words:
            # Sort occurrences by document ID (required for merge intersection)
            occurrences = sorted(temp_index[word].items())
            
            list_index = len(self.postings_lists)
            self.postings_lists.append(occurrences)
            self.trie.insert(word, list_index)

    def get_postings(self, word):
        list_idx = self.trie.search(word.lower())
        if list_idx != -1:
            return self.postings_lists[list_idx]
        return []

    def intersect(self, list1, list2):
        # Merge-style intersection for AND query
        result = []
        i, j = 0, 0
        while i < len(list1) and j < len(list2):
            doc1, freq1 = list1[i]
            doc2, freq2 = list2[j]
            
            if doc1 == doc2:
                result.append((doc1, freq1 + freq2))
                i += 1
                j += 1
            elif doc1 < doc2:
                i += 1
            else:
                j += 1
        return result

    def search_all(self, query_tokens):
        if not query_tokens:
            return []
        
        # Start with the first word's postings
        res_list = self.get_postings(query_tokens[0])
        
        # Intersect with subsequent words (AND logic)
        for i in range(1, len(query_tokens)):
            next_list = self.get_postings(query_tokens[i])
            res_list = self.intersect(res_list, next_list)
            if not res_list:
                break
        
        # Rank the results
        # Score = sum(frequencies) + title bonus
        final_results = []
        for doc_id, freq_sum in res_list:
            doc_info = self.doc_map[doc_id]
            score = freq_sum
            
            # Substantial title bonus if any of the query words appear in the title
            title_lower = doc_info['title'].lower()
            for token in query_tokens:
                if token in title_lower:
                    score += 5 # Title bonus
            
            # Simple snippet (first 160 chars)
            snippet = doc_info['content'][:160] + "..."
            
            final_results.append({
                'title': doc_info['title'],
                'file': doc_info['file'],
                'score': score,
                'snippet': snippet
            })
            
        # Sort by score descending
        return sorted(final_results, key=lambda x: x['score'], reverse=True)
