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
}

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
 * Search for code using semantic search (auto-detects demo mode)
 */
export async function searchCode(query: SearchQuery): Promise<SearchResponse> {
  // Try demo endpoint first (works without API keys)
  try {
    const response = await api.post<SearchResponse>('/demo/search', query)
    return response.data
  } catch (demoError) {
    // Fall back to real search if demo fails
    const response = await api.post<SearchResponse>('/search/', query)
    return response.data
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
