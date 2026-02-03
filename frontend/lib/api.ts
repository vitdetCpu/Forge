const API_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'

interface ApiResponse<T> {
  data?: T
  error?: string
}

async function fetchApi<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Unknown error' }))
    throw new Error(error.error || `HTTP ${response.status}`)
  }

  return response.json()
}

export async function startSession(userId: string) {
  return fetchApi<{
    session_id: string
    daily_room_url: string
    daily_token?: string
  }>('/start-session', {
    method: 'POST',
    body: JSON.stringify({ user_id: userId }),
  })
}

export async function endSession(sessionId: string) {
  return fetchApi<{
    final_scores: Record<string, number>
    improvement: Record<string, number>
  }>('/end-session', {
    method: 'POST',
    body: JSON.stringify({ session_id: sessionId }),
  })
}

export async function getSessionStatus(sessionId: string) {
  return fetchApi<{
    current_question: string
    transcript: string
    questions_asked: number
    current_scores: Record<string, number>
  }>(`/session-status?session_id=${sessionId}`)
}

export async function getSessions(userId: string) {
  return fetchApi<{
    sessions: Array<{
      id: string
      date: string
      questions_asked: number
      average_score: number
    }>
  }>(`/sessions?user_id=${userId}`)
}

export async function getKnowledgeMap(userId: string) {
  return fetchApi<{
    topics: Record<string, number>
    history: Array<{
      session: number
      [key: string]: number
    }>
  }>(`/knowledge-map?user_id=${userId}`)
}
