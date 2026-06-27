import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism'
import { SearchResponse } from '../services/api'
import './SearchResults.css'

interface SearchResultsProps {
  results: SearchResponse
}

function SearchResults({ results }: SearchResultsProps) {
  const { query, results: codeResults, total_found, reasoning, took_ms } = results

  if (!codeResults || codeResults.length === 0) {
    return (
      <div className="no-results">
        <div className="no-results-icon">🤔</div>
        <h3>No results found</h3>
        <p>Try a different search query or adjust your filters.</p>
      </div>
    )
  }

  return (
    <div className="search-results">
      <div className="results-header">
        <h3 className="results-title">
          Found {total_found} result{total_found !== 1 ? 's' : ''} for "{query}"
        </h3>
        {took_ms && (
          <span className="results-timing">
            in {took_ms.toFixed(0)}ms
          </span>
        )}
      </div>

      {reasoning && (
        <div className="reasoning-box">
          <div className="reasoning-header">
            <span className="reasoning-icon">🧠</span>
            <strong>Claude's Analysis:</strong>
          </div>
          <p className="reasoning-text">{reasoning}</p>
        </div>
      )}

      <div className="results-grid">
        {codeResults.map((result, index) => (
          <div key={result.id} className="result-card">
            <div className="result-header">
              <div className="result-rank">
                <span className="rank-badge">#{result.rank || index + 1}</span>
                <span className="language-badge">{result.language}</span>
              </div>
              <div className="result-source">{result.source}</div>
            </div>

            {result.ranking_reason && (
              <div className="ranking-reason">
                <strong>Why this rank:</strong> {result.ranking_reason}
              </div>
            )}

            <div className="code-container">
              <SyntaxHighlighter
                language={result.language}
                style={vscDarkPlus}
                customStyle={{
                  margin: 0,
                  borderRadius: '8px',
                  fontSize: '0.9rem',
                }}
              >
                {result.code}
              </SyntaxHighlighter>
            </div>

            {result.explanation && (
              <div className="explanation">
                <strong>What it does:</strong> {result.explanation}
              </div>
            )}

            {result.score_breakdown && (
              <div className="score-breakdown">
                <strong>Scores:</strong>
                <div className="scores">
                  {Object.entries(result.score_breakdown).map(([criterion, score]) => (
                    <div key={criterion} className="score-item">
                      <span className="score-criterion">{criterion}</span>
                      <div className="score-bar">
                        <div
                          className="score-fill"
                          style={{ width: `${score * 10}%` }}
                        />
                      </div>
                      <span className="score-value">{score}/10</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="result-footer">
              <span className="similarity-score">
                Similarity: {(result.similarity_score * 100).toFixed(0)}%
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default SearchResults
