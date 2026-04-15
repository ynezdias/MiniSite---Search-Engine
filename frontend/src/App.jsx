import { useState, useEffect } from 'react'
import axios from 'axios'
import { Search, Rocket, Microscope, Globe, Loader2, Database, List } from 'lucide-react'

const API_BASE = 'http://localhost:5000/api'

function App() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(false)
  const [hasSearched, setHasSearched] = useState(false)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API_BASE}/stats`)
      setStats(response.data)
    } catch (err) {
      console.error('Error fetching stats:', err)
    }
  }

  const handleSearch = async (e) => {
    e?.preventDefault()
    if (!query.trim()) {
      setResults([]);
      setHasSearched(false);
      return;
    }

    setLoading(true)
    try {
      const response = await axios.get(`${API_BASE}/search?q=${encodeURIComponent(query)}`)
      setResults(response.data.results)
      setStats(response.data.stats)
      setHasSearched(true)
    } catch (err) {
      console.error('Search error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>Cosmos Search</h1>
      
      <div className="glass" style={{ marginBottom: '2rem' }}>
        <form onSubmit={handleSearch} className="search-container">
          <input 
            type="text" 
            placeholder="Search planets, rockets, missions..." 
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button type="submit" disabled={loading}>
            {loading ? <Loader2 className="loader" /> : 'Search Now'}
          </button>
        </form>

        {stats && (
          <div className="stats-grid">
            <div className="stat-card glass">
              <Database className="stat-label" size={16} />
              <div className="stat-value">{stats.docs_crawled}</div>
              <div className="stat-label">Pages Crawled</div>
            </div>
            <div className="stat-card glass">
              < Microscope className="stat-label" size={16} />
              <div className="stat-value">{stats.unique_terms}</div>
              <div className="stat-label">Indexed Terms</div>
            </div>
            <div className="stat-card glass" style={{ gridColumn: 'span 2' }}>
              <List className="stat-label" size={16} />
              <div className="stat-label" style={{ marginBottom: '5px' }}>Discovered Pages</div>
              <div className="crawl-links">
                {stats.pages.map((p, i) => (
                  <span key={i} className="link-pill">{p}</span>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="results-list">
        {loading ? (
          <div style={{ textAlign: 'center', padding: '3rem' }}>
            <Rocket className="loader" size={48} style={{ marginBottom: '1rem', color: '#60a5fa' }} />
            <p>Scanning the galaxy...</p>
          </div>
        ) : results.length > 0 ? (
          results.map((res, index) => (
            <div key={index} className="result-item" style={{ animationDelay: `${index * 0.1}s` }}>
              <div className="glass result-card">
                <div className="result-header">
                  <h3 className="result-title">{res.title}</h3>
                  <span className="result-score">Score: {res.score.toFixed(1)}</span>
                </div>
                <div className="result-file">{res.file}</div>
                <p className="result-snippet">{res.snippet}</p>
              </div>
            </div>
          ))
        ) : hasSearched ? (
          <div className="glass" style={{ textAlign: 'center', padding: '3rem' }}>
            <Rocket size={48} style={{ marginBottom: '1rem', opacity: 0.2 }} />
            <p>No signals found for "{query}". Try different coordinates.</p>
          </div>
        ) : (
          <div className="glass" style={{ textAlign: 'center', padding: '3rem', opacity: 0.6 }}>
            <Search size={48} style={{ marginBottom: '1rem' }} />
            <p>Start your journey by entering a search term above.</p>
            <div style={{ display: 'flex', gap: '0.5rem', justifyContent: 'center', marginTop: '1rem' }}>
              <span className="link-pill" style={{ cursor: 'pointer' }} onClick={() => { setQuery('Moon'); handleSearch(); }}>Try "Moon"</span>
              <span className="link-pill" style={{ cursor: 'pointer' }} onClick={() => { setQuery('Mars rocket'); handleSearch(); }}>Try "Mars rocket"</span>
              <span className="link-pill" style={{ cursor: 'pointer' }} onClick={() => { setQuery('Voyager'); handleSearch(); }}>Try "Voyager"</span>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
