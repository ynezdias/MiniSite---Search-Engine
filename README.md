# Space Exploration Search Engine - Technical Specification

A precision-engineered search engine for a structured corpus of space exploration data.

## Why this Architecture?

### 1. Compressed Trie (Radix Tree)
We chose a **Compressed Trie** over a standard Trie or a Hash Map for the term dictionary:
- **Prefix Compression**: In technical domains like space (rocket, rocketry, robotic), terms often share long prefixes. A compressed trie merges single-child nodes into single edges, drastically reducing node count and memory overhead.
- **Ordered Traversal**: Unlike Hash Maps, a Trie maintains alphabetical order and makes prefix-based searching ($O(k)$ where $k$ is term length) trivial.

### 2. External Occurrence Lists (Postings)
Occurrence lists are stored separately in a contiguous array rather than raw nodes:
- **Cache Locality**: Storing postings together improves performance during retrieval.
- **Sorted Intersections**: By keeping these lists sorted by Document ID, we can perform linear-time $O(n+m)$ intersections for multi-word queries.
- **Scalability**: This "Textbook Style" separation allows for future optimizations like delta-encoding or disk-based storage without affecting the dictionary lookup mechanism.

---

## The Query Pipeline: Step-by-Step

When you enter a search like **"The Moon!"**, the following process occurs:

1.  **Normalization & Tokenization**: 
    - The engine strips "The" (stop-word) and "!" (punctuation).
    - It lowercases the string.
    - Result: `['moon']`.

2.  **Dictionary Lookup (Trie)**:
    - The engine traverses the **Compressed Trie** for the sequence `m-o-o-n`.
    - It arrives at a terminal node containing a `postings_index` (e.g., `4`).

3.  **Posting Retrieval**:
    - The engine accesses the centralized `postings_lists[4]`.
    - This returns `[(1, 8), (7, 1), (0, 1), (6, 1)]` (tuples of `DocID` and `Frequency`).

4.  **Multi-Keyword Logic (Merging)**:
    - For queries like "Moon Rocket", the engine retrieves lists for both "moon" and "rocket".
    - It uses a **two-pointer merge algorithm** to find the intersection where both terms appear in the same document.

5.  **Ranking & Scoring**:
    - Each document is assigned a score: `Score = sum(Term Frequencies)`.
    - **Title Bonus**: If any query word appears in the document's `<title>`, a significant +5 bonus is added to emphasize relevancy.

6.  **Presentation**:
    - Results are sorted by score (descending) and returned with a snippet extracted from the original crawled HTML.

---

## How to Verify
Run `python backend/test_rigor.py` to see the engine handle boundary cases like:
- No-Match Queries
- Multi-word Intersections (AND logic)
- Stop-word filtering
- Punctuation/Case normalization