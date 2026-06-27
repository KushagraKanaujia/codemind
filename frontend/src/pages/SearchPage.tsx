import { useState } from 'react'
import { searchCode, SearchResponse } from '../services/api'
import SearchBar from '../components/SearchBar'
import SearchResults from '../components/SearchResults'
import './SearchPage.css'

function SearchPage() {
  const [results, setResults] = useState<SearchResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

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

          <SearchBar onSearch={handleSearch} loading={loading} />

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
            <p>Claude is analyzing code implementations...</p>
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
              <li>"binary search algorithm"</li>
              <li>"fast sorting algorithm"</li>
              <li>"tree traversal implementation"</li>
              <li>"efficient graph search"</li>
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}

export default SearchPage
