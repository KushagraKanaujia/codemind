import { useState } from 'react'
import { searchCode, SearchResponse, SEARCH_MODE } from '../services/api'
import SearchBar from '../components/SearchBar'
import SearchResults from '../components/SearchResults'
import './SearchPage.css'

const EXAMPLES = [
  'binary search algorithm',
  'debounce function',
  'linked list',
  'jwt authentication middleware',
  'react custom hook',
]

function SearchPage() {
  const [results, setResults] = useState<SearchResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [query, setQuery] = useState('')

  const handleSearch = async (query: string, criteria: string[], language?: string) => {
    if (!query.trim()) {
      setError('Please enter a search query')
      return
    }

    setLoading(true)
    setError(null)
    setResults(null)

    try {
      const response = await searchCode({
        query,
        criteria: criteria.length > 0 ? criteria : undefined,
        max_results: 5,
        language: language || undefined,
      })

      setResults(response)
    } catch (err: any) {
      console.error('Search error:', err)
      setError(
        err.response?.data?.detail ||
        err.message ||
        'Failed to search. Please make sure the backend is running.'
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="search-page">
      <div className="container">
        <div className="search-section">
          <h2 className="search-title">Search for code implementations</h2>
          <p className="search-description">
            Describe what you're looking for in natural language. CodeMind will find implementations,
            analyze them, and rank them based on your criteria.
          </p>

          <div className={`mode-banner mode-${SEARCH_MODE}`}>
            {SEARCH_MODE === 'browser' && (
              <>
                <strong>Static demo.</strong> Searching 203 bundled code snippets right in your browser
                (keyword search, no API keys). The full app adds Claude-powered ranking and explanations —{' '}
                <a href="https://github.com/KushagraKanaujia/codemind#run-the-full-app" target="_blank" rel="noreferrer">
                  run it yourself
                </a>.
              </>
            )}
            {SEARCH_MODE === 'demo' && (
              <>
                <strong>Demo mode.</strong> Uses the backend's keyless demo endpoint (canned results);
                falls back to in-browser search over the dataset if the backend isn't running.
              </>
            )}
            {SEARCH_MODE === 'live' && (
              <>
                <strong>Live mode.</strong> Results are ranked by Claude via the backend.
              </>
            )}
          </div>

          <SearchBar onSearch={handleSearch} loading={loading} query={query} onQueryChange={setQuery} />

          {error && (
            <div className="error-message">
              <span className="error-icon">⚠️</span>
              {error}
            </div>
          )}
        </div>

        {loading && (
          <div className="loading-state">
            <div className="loading-spinner"></div>
            <p>{SEARCH_MODE === 'live' ? 'Claude is analyzing code implementations...' : 'Searching...'}</p>
          </div>
        )}

        {results && !loading && (
          <SearchResults results={results} />
        )}

        {!results && !loading && !error && (
          <div className="empty-state">
            <div className="empty-icon">🔍</div>
            <h3>Start searching</h3>
            <p>Try searching for:</p>
            <ul className="examples-list">
              {EXAMPLES.map((ex) => (
                <li key={ex}>
                  <button
                    type="button"
                    className="example-button"
                    onClick={() => {
                      setQuery(ex)
                      handleSearch(ex, [])
                    }}
                  >
                    "{ex}"
                  </button>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}

export default SearchPage
