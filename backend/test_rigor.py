import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from search_engine import SearchEngine

def run_test(engine, query, description):
    print(f"--- TEST: {description} ---")
    print(f"Input: '{query}'")
    results = engine.search(query)
    print(f"Results Count: {len(results)}")
    for i, res in enumerate(results[:3]):
        print(f"  {i+1}. {res['title']} (Score: {res['score']})")
    print(f"--- END TEST ---\n")
    return results

if __name__ == "__main__":
    # Initialize engine
    website_path = os.path.join(os.path.dirname(__file__), '..', 'website')
    engine = SearchEngine(website_path)
    engine.run_crawl_and_index()

    print("RIGOROUS BOUNDARY CASE TESTING\n" + "="*30 + "\n")

    # 1. Empty Query
    run_test(engine, "", "Empty Query")

    # 2. Stop words only
    run_test(engine, "the and or in", "Only Stop Words")

    # 3. Nonexistent term
    run_test(engine, "xenomorph", "Nonexistent Term")

    # 4. Single Match
    run_test(engine, "telescope", "Single Keyword Match")

    # 5. Multi-keyword Intersection (AND logic)
    run_test(engine, "Mars Starship", "Multi-keyword Intersection (Matches Both)")

    # 6. Multi-keyword No Intersection
    run_test(engine, "Moon Voyager", "Multi-keyword No Intersection (Terms exist separately, but not together)")

    # 7. Query with punctuation (Should be handled by normalization)
    run_test(engine, "Mars!", "Query with Punctuation")

    # 8. Extra whitespace
    run_test(engine, "   rocket   ", "Excessive Whitespace")

    # 9. Case sensitivity
    run_test(engine, "mOOn", "Case Insensitivity Check")
