/**
 * API service for backend communication
 */

import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface SearchQuery {
  query: string
  criteria?: string[]
  max_results?: number
  language?: string
}

export interface CodeResult {
  id: string
  code: string
  language: string
  source: string
  similarity_score: number
  explanation?: string
  score_breakdown?: Record<string, number>
  rank?: number
  ranking_reason?: string
}

export interface SearchResponse {
  query: string
  results: CodeResult[]
  total_found: number
  reasoning?: string
  took_ms?: number
  /** Where the results came from (set by the frontend). */
  mode?: SearchMode
}

/**
 * browser - in-browser keyword search over the bundled dataset (no backend, no keys)
 * demo    - backend /demo/search (canned results, no keys); falls back to browser
 * live    - backend /search/ (Claude ranking; needs API keys)
 */
export type SearchMode = 'browser' | 'demo' | 'live'

export const SEARCH_MODE: SearchMode =
  (import.meta.env.VITE_SEARCH_MODE as SearchMode) || 'demo'

/**
 * Check if running in demo mode
 */
export async function isDemoMode(): Promise<boolean> {
  try {
    const response = await api.get('/demo/info')
    return response.status === 200
  } catch {
    return false
  }
}

/**
 * Search for code. Behaviour depends on VITE_SEARCH_MODE (see SearchMode).
 */
export async function searchCode(query: SearchQuery): Promise<SearchResponse> {
  if (SEARCH_MODE === 'browser') {
    const { localSearch } = await import('./localSearch')
    return localSearch(query)
  }

  if (SEARCH_MODE === 'live') {
    const response = await api.post<SearchResponse>('/search/', query)
    return { ...response.data, mode: 'live' }
  }

  // demo: try the backend demo endpoint, fall back to in-browser search
  try {
    const response = await api.post<SearchResponse>('/demo/search', query)
    return { ...response.data, mode: 'demo' }
  } catch {
    const { localSearch } = await import('./localSearch')
    return localSearch(query)
  }
}

/**
 * Health check
 */
export async function checkHealth(): Promise<any> {
  const response = await api.get('/health')
  return response.data
}

export default api
