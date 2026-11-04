/**
 * In-browser search over the bundled 203-snippet dataset (data/complete_dataset.json).
 *
 * Used by the static demo (e.g. the Netlify deploy) and as a fallback when the
 * backend is not running. It is plain full-text search (BM25-style ranking with
 * prefix + fuzzy matching via MiniSearch) - no embeddings and no Claude calls.
 */

import MiniSearch from 'minisearch'
import type { SearchQuery, SearchResponse, CodeResult } from './api'

interface Snippet {
  id: string
  code: string
  language: string
  source: string
  description: string
  tags: string[]
}

let indexPromise: Promise<MiniSearch<Snippet>> | null = null

function loadIndex(): Promise<MiniSearch<Snippet>> {
  if (!indexPromise) {
    indexPromise = import('../../../data/complete_dataset.json').then((mod) => {
      const raw = (mod.default ?? mod) as Omit<Snippet, 'id'>[]
      const docs: Snippet[] = raw.map((s, i) => ({ ...s, id: `snippet-${i + 1}` }))
      const ms = new MiniSearch<Snippet>({
        fields: ['description', 'tags', 'source', 'code'],
        storeFields: ['code', 'language', 'source', 'description', 'tags'],
        extractField: (doc, field) => {
          const v = (doc as unknown as Record<string, unknown>)[field]
          return Array.isArray(v) ? v.join(' ') : (v as string)
        },
        searchOptions: {
          boost: { description: 3, tags: 2, source: 1.5, code: 0.5 },
          prefix: true,
          fuzzy: 0.2,
          combineWith: 'OR',
        },
      })
      ms.addAll(docs)
      return ms
    })
  }
  return indexPromise
}

export async function datasetSize(): Promise<number> {
  return (await loadIndex()).documentCount
}

export async function localSearch(q: SearchQuery): Promise<SearchResponse> {
  const start = performance.now()
  const ms = await loadIndex()
  const lang = q.language?.toLowerCase()
  const hits = ms.search(q.query, {
    filter: lang ? (r) => String(r.language).toLowerCase() === lang : undefined,
  })
  const max = q.max_results ?? 5
  const top = hits[0]?.score || 1

  const results: CodeResult[] = hits.slice(0, max).map((h, i) => ({
    id: String(h.id),
    code: h.code as string,
    language: h.language as string,
    source: h.source as string,
    // Relative to the best hit, so the top match always reads 100%.
    similarity_score: h.score / top,
    explanation: h.description as string,
    rank: i + 1,
    ranking_reason: `Matched terms: ${h.terms.slice(0, 6).join(', ')}`,
  }))

  const criteriaNote = q.criteria?.length
    ? ` Criteria (${q.criteria.join(', ')}) are only applied by Claude in the full backend mode.`
    : ''

  return {
    query: q.query,
    results,
    total_found: hits.length,
    reasoning:
      `Static demo: keyword search (MiniSearch, BM25-style) over ${ms.documentCount} bundled snippets, running entirely in your browser. ` +
      `No embeddings or Claude calls are made here; explanations are the dataset's own descriptions.` +
      criteriaNote,
    took_ms: performance.now() - start,
    mode: 'browser',
  }
}
