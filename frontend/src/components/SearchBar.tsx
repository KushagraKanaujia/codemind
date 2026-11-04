import { useState, FormEvent } from 'react'
import './SearchBar.css'

interface SearchBarProps {
  onSearch: (query: string, criteria: string[], language?: string) => void
  loading: boolean
  query: string
  onQueryChange: (query: string) => void
}

const CRITERIA_OPTIONS = ['fast', 'readable', 'secure', 'simple', 'maintainable']
// Languages present in data/complete_dataset.json
const LANGUAGE_OPTIONS = ['python', 'javascript', 'typescript', 'java', 'cpp', 'sql', 'c', 'go', 'rust']

function SearchBar({ onSearch, loading, query, onQueryChange: setQuery }: SearchBarProps) {
  const [selectedCriteria, setSelectedCriteria] = useState<string[]>([])
  const [selectedLanguage, setSelectedLanguage] = useState('')
  const [showFilters, setShowFilters] = useState(false)

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    onSearch(query, selectedCriteria, selectedLanguage)
  }

  const toggleCriteria = (criterion: string) => {
    setSelectedCriteria(prev =>
      prev.includes(criterion)
        ? prev.filter(c => c !== criterion)
        : [...prev, criterion]
    )
  }

  return (
    <div className="search-bar">
      <form onSubmit={handleSubmit}>
        <div className="search-input-wrapper">
          <input
            type="text"
            className="search-input"
            placeholder="e.g., binary search algorithm, fast sorting, tree traversal..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={loading}
          />
          <button
            type="submit"
            className="search-button"
            disabled={loading || !query.trim()}
          >
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>

        <button
          type="button"
          className="filter-toggle"
          onClick={() => setShowFilters(!showFilters)}
        >
          {showFilters ? '▼' : '▶'} Filters
          {(selectedCriteria.length > 0 || selectedLanguage) && (
            <span className="filter-badge">
              {selectedCriteria.length + (selectedLanguage ? 1 : 0)}
            </span>
          )}
        </button>

        {showFilters && (
          <div className="filters-panel">
            <div className="filter-group">
              <label className="filter-label">Ranking Criteria:</label>
              <div className="criteria-chips">
                {CRITERIA_OPTIONS.map(criterion => (
                  <button
                    key={criterion}
                    type="button"
                    className={`chip ${selectedCriteria.includes(criterion) ? 'active' : ''}`}
                    onClick={() => toggleCriteria(criterion)}
                  >
                    {criterion}
                  </button>
                ))}
              </div>
            </div>

            <div className="filter-group">
              <label className="filter-label">Language:</label>
              <select
                className="language-select"
                value={selectedLanguage}
                onChange={(e) => setSelectedLanguage(e.target.value)}
              >
                <option value="">All languages</option>
                {LANGUAGE_OPTIONS.map(lang => (
                  <option key={lang} value={lang}>
                    {lang.charAt(0).toUpperCase() + lang.slice(1)}
                  </option>
                ))}
              </select>
            </div>
          </div>
        )}
      </form>
    </div>
  )
}

export default SearchBar
